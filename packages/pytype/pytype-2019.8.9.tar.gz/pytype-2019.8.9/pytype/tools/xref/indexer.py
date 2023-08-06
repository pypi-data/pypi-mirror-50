#!/usr/bin/env python

"""Generate cross references from a project."""

from __future__ import print_function

import collections

from pytype import abstract
from pytype import analyze
from pytype import errors
from pytype import io
from pytype import load_pytd
from pytype import module_utils
from pytype.tools.traces import source
from pytype.tools.traces import traces
from pytype.tools.traces import visitor as ast_visitor

from pytype.tools.xref import utils as xref_utils
from pytype.tools.xref import kythe

from typed_ast import ast27 as ast27
from typed_ast import ast3

# A global "ast" variable that we set to ast27 or ast3 depending on the target
# python version.
#
# TODO(mdemello): Use typed_ast.convert to coerce everything into ast3
ast = None


# A mapping of offsets between a node's start position and the symbol being
# defined. e.g. in the declaration "class X" the X is at +6 from the start.
DEF_OFFSETS = {
    "ClassDef": 6,  # class X
    "FunctionDef": 4,  # def f
}


# Marker for a link to a file rather than a node within the file.
IMPORT_FILE_MARKER = "<__FILE__>"


def typename(node):
  return node.__class__.__name__


def get_id(node):
  """Construct an id based on node type."""

  c = node.__class__
  if c == ast.FunctionDef:
    return "function %s" % node.name
  elif c == ast.ClassDef:
    return "class %s" % node.name
  elif c == ast.Module:
    return "module"
  else:
    raise ValueError("Unexpected scope: %r" % node)


def qualified_method(data):
  """Fully qualify a method call with its class scope."""
  if isinstance(data, abstract.BoundFunction):
    return data.repr_names()
  else:
    return [data.name]


def get_name(node):
  """Nodes have different name attributes."""

  if isinstance(node, ast.Attribute):
    return get_name(node.value) + "." + node.attr
  elif isinstance(node, ast.arg):
    return node.arg
  elif isinstance(node, str):
    return node
  elif hasattr(node, "name"):
    return node.name
  elif hasattr(node, "id"):
    return node.id
  else:
    return "[" + typename(node) + "]"


def get_location(node):
  # TODO(mdemello): The column offset for nodes like "class A" needs to be
  # adjusted to the start of the symbol.
  return source.Location(node.lineno, node.col_offset)


def has_decorator(f, decorator):
  for d in f.decorator_list:
    if isinstance(d, ast.Name) and d.id == decorator:
      return True
  return False


def match_opcodes(opcode_traces, lineno, op_match_list):
  """Get all opcodes matching op_match_list on a given line.

  Args:
    opcode_traces: traces
    lineno: line number to get ops from.
    op_match_list: [(opcode_name, symbol|None), ...]; None matches any symbol.

  Returns:
    A list of matching opcodes.
  """
  out = []
  for op, symbol, data in opcode_traces[lineno]:
    for match_op, match_symbol in op_match_list:
      if op == match_op and match_symbol in [None, symbol]:
        out.append((op, symbol, data))
  return out


def _unwrap(data):
  assert len(data) == 1
  return data[0]


# Internal datatypes


class AttrError(Exception):
  pass


class PytypeValue(object):
  """Stores a value inferred by pytype."""

  def __init__(self, module, name, typ):
    self.module = module
    self.name = name
    self.typ = typ
    self.id = self.module + "." + self.name

  def format(self):
    return "%s { %s.%s : %s }" % (
        self.id, self.module, self.typ, self.name)

  @classmethod
  def _from_data(cls, data):
    """Construct a PytypeValue from a single datum."""

    if isinstance(data, abstract.PyTDClass):
      if data.module:
        # If we have a remote reference, return Remote rather than PytypeValue.
        return Remote(data.module, data.name, resolved=True)
      else:
        # This is a namedtuple or some other special case pytype has generated a
        # local PyTDClass for. We need special cases for them too.
        return None
    elif isinstance(data, abstract.Module):
      return Remote(data.name, IMPORT_FILE_MARKER, resolved=True)
    elif isinstance(data, abstract.InterpreterClass):
      return cls("module", data.name, "Class")
    elif isinstance(data, abstract.BoundFunction):
      # TODO(mdemello): Handle multiple class bindings.
      name = data.repr_names(callself_repr=typename)[0]
      return cls("module", name, "BoundFunction")
    else:
      # TODO(mdemello): We need to infer the module here.
      return cls("module", str(data), typename(data))

  @classmethod
  def from_data(cls, data):
    """Construct a PytypeValue from a list of data."""

    if not data:
      return None
    else:
      return [cls._from_data(x) for x in data]

  def to_signature(self):
    return self.module + "." + self.name


class Module(object):
  """Module representation."""

  def __init__(self, name):
    self.name = name

  def attr(self, attr_name):
    return Remote(self.name, attr_name, resolved=True)

  def submodule(self, attr_name):
    name = self.name + "." + attr_name
    return Remote(name, IMPORT_FILE_MARKER, resolved=True)


class Dummy(object):
  """Work around a python3 issue with calling super with kwargs."""

  def __init__(self, *args, **kwargs):
    pass


class DocString(collections.namedtuple(
    "docstring", ["text", "location", "length"])):
  """Store the text and location of a docstring."""

  @classmethod
  def from_node(cls, node):
    """If the first element in node.body is a string, create a docstring."""

    # This should only be called on ClassDef and FunctionDef
    assert isinstance(node, (ast.ClassDef, ast.FunctionDef))
    if (node.body and
        isinstance(node.body[0], ast.Expr) and
        isinstance(node.body[0].value, ast.Str)):
      doc_node = node.body[0]
      doc = doc_node.value.s
      length = len(doc)  # we want to preserve the byte length
      if isinstance(doc, bytes):
        # In target 2.7 mode we get docstrings as bytes.
        doc = doc.decode("utf-8")
      return cls(doc, get_location(doc_node), length)
    return None


class Definition(collections.namedtuple(
    "defn", ["name", "typ", "data", "scope", "target", "doc"]), Dummy):
  """A symbol definition.

  Attributes:
    name: The symbol name
    typ: The definition type (e.g. ClassDef)
    data: Pytype data from the opcode traces
    scope: The namespace id (e.g. module:class A:function f:x)
    target: The LHS of an attribute (e.g. for x.foo, target = typeof(x))
    doc: The docstring, if any, for function and class defs
    id: The id
  """

  def __init__(self, name, typ, data, scope, target, doc):
    super(Definition, self).__init__(name, typ, data, scope, target, doc)
    self.id = self.scope + "." + self.name

  def format(self):
    return self.id

  def to_signature(self):
    return self.id

  def doc_signature(self):
    """Signature for the definition's docstring."""
    return self.to_signature() + ".__doc__"

  def node_kind(self):
    # TODO(mdemello): Add more node types.
    if self.typ == "ClassDef":
      return "class"
    elif self.typ == "FunctionDef":
      return "function"
    else:
      return "variable"


class Remote(collections.namedtuple(
    "remote", ["module", "name", "resolved"]), Dummy):
  """A symbol from another module."""

  def __init__(self, module, name, resolved):
    super(Remote, self).__init__(module, name, resolved)
    self.id = self.module + "/module." + self.name

  def attr(self, attr_name):
    return Remote(self.module, self.name + "." + attr_name, self.resolved)

  def format(self):
    return self.id


class DefLocation(collections.namedtuple("defloc", ["def_id", "location"])):
  """A location of a symbol definition.

  Attributes:
    def_id: The definition id (scope + name)
    location: The location of the definition in the source code.

  Note that a single definition can have multiple locations, for symbols that
  are redefined in the code.
  """


class Reference(collections.namedtuple(
    "refr", [
        "name", "typ", "data", "scope", "ref_scope", "target", "location"])
                , Dummy):
  """A symbol holding a reference to a definition.

  Attributes:
    name: The symbol name
    typ: The symbol type (e.g. Attribute)
    data: The pytype data attached to the symbol
    scope: The namespace id (e.g. module.A.f)
    ref_scope: The namespace id of the referred symbol (if we can determine it)
    target: The LHS of an attribute (e.g. for x.foo, target = typeof(x))
    location: The line and column of the symbol in the source code
    id: The id
  """

  def __init__(self, name, typ, data, scope, ref_scope, target, location):
    super(Reference, self).__init__(
        name, typ, data, scope, ref_scope, target, location)
    self.id = self.scope + "." + self.name

  def format(self):
    return self.id


class Funcall(object):
  """Representation of a function call."""

  def __init__(self, name, func, location):
    self.name = name
    self.func = func
    self.location = location


class Env(object):
  """A collection of namespaced symbols."""

  def __init__(self, scope, parent, cls):
    """Initialize an environment.

    Arguments:
      scope: The namespace key (e.g. module:class A:function f)
      parent: The env of the directly enclosing namespace
      cls: The class currently being defined
           (None if we are not in a class definition)

    Other attributes defined:
      env: The dictionary holding the symbol table for this environment
      attrs: Attributes defined on the current class
      self_var: The `self` variable in method definitions
    """

    self.scope = scope
    self.parent = parent
    self.cls = cls
    self.env = {}
    self.attrs = None
    self.self_var = parent and parent.self_var

  def lookup(self, symbol):
    if symbol in self.env:
      return (self, self.env[symbol])
    elif self.parent:
      return self.parent.lookup(symbol)
    else:
      return (None, None)

  def __getitem__(self, symbol):
    return self.lookup(symbol)[1]

  def __setitem__(self, symbol, value):
    self.env[symbol] = value

  def is_self_attr(self, node):
    return (
        self.self_var and
        isinstance(node, ast.Attribute) and
        isinstance(node.value, ast.Name) and
        node.value.id == self.self_var.name)

  def getattr(self, attr):
    if self.attrs is not None and attr in self.attrs:
      return self.attrs[attr]
    elif self.cls and self.cls.scope != self.scope:
      return self.cls.getattr(attr)
    else:
      raise AttrError("called getattr in non-class context")

  def setattr(self, attr, value):
    if self.attrs is not None:
      self.attrs[attr] = value
    elif self.cls is not None:
      return self.cls.setattr(attr, value)
    else:
      raise AttrError("called setattr in non-class context")


# pylint: disable=invalid-name
# pylint: disable=missing-docstring
#
# Visitors use generated method names that don't follow the pylint spec.
# Also names like visit_Name are self-documenting and do not need docstrings.


class ScopedVisitor(ast_visitor.BaseVisitor):
  """An AST node visitor that keeps track of scopes and environments.

  A "scope" is the abstract namespace (represented by a string key that tracks
  the nested path of namespaces from the module root, e.g. module:class A:f).
  An "environment" holds data for the current scope. self.envs is not
  hierarchical, it's just a flat mapping of scope keys to environments.
  """

  # TODO(b/138541525): Remove these unnecessary class attributes.
  stack = None  # type: list
  class_ids = None  # type: list
  envs = None  # type: dict
  module_name = None  # type: str

  # TODO(mdemello): Is the two-level visitor hierarchy really buying us
  # anything by way of maintainability or readability?

  def __init__(self, module_name):
    super(ScopedVisitor, self).__init__(ast)
    self.stack = []
    self.class_ids = []
    self.envs = {}
    self.module_name = module_name

  def get_id(self, node):
    """Construct an id based on node type."""

    c = node.__class__
    if c == ast.FunctionDef:
      return node.name
    elif c == ast.ClassDef:
      return node.name
    elif c == ast.Module:
      return self.module_name
    else:
      raise Exception("Unexpected scope: %r" % node)

  def iprint(self, x):
    """Print messages indented by scope level, for debugging."""
    print("  " * len(self.stack), x)

  def scope_id(self):
    return ".".join(self.get_id(x) for x in self.stack)

  @property
  def current_class(self):
    if self.class_ids:
      return self.envs[self.class_ids[-1]]
    return None

  @property
  def current_env(self):
    current_scope = self.scope_id()
    return self.envs[current_scope]

  def add_scope(self, node, is_class=False):
    if self.stack:
      parent = self.current_env
    else:
      parent = None
    self.stack.append(node)
    new_scope = self.scope_id()
    new_env = Env(scope=new_scope, parent=parent,
                  cls=self.current_class)
    if is_class:
      new_env.attrs = {}
    self.envs[new_scope] = new_env
    return new_env

  def enter_ClassDef(self, node):
    new_env = self.add_scope(node, is_class=True)
    self.class_ids.append(self.scope_id())
    # We need to set the env's cls to the new class, not the enclosing one.
    new_env.cls = self.current_class

  def leave_ClassDef(self, _):
    self.class_ids.pop()

  def enter_FunctionDef(self, node):
    self.add_scope(node)

  def enter_Module(self, node):
    self.add_scope(node)

  def leave(self, node):
    """If the node has introduced a new scope, we need to pop it off."""
    super(ScopedVisitor, self).leave(node)
    if node == self.stack[-1]:
      self.stack.pop()


class IndexVisitor(traces.MatchAstVisitor, ScopedVisitor):
  """Visitor that generates indexes."""

  def __init__(self, src, module_name, kythe_):
    super(IndexVisitor, self).__init__(src, module_name)
    self.defs = {}
    self.locs = collections.defaultdict(list)
    self.refs = []
    self.modules = {}
    self.source = src
    self.traces = src.traces
    self.typemap = {}
    self.classmap = {}
    self.calls = []
    self.kythe = kythe_

  def _get_location(self, node, args):
    """Get a more accurate node location."""

    loc = None

    if isinstance(node, ast.ClassDef):
      # For class and function definitions, search for the string
      #   (class|def) <name>
      # between the start of the AST node and the start of the body. Handles the
      # offset for decorated functions/classes.
      body_start = node.body[0].lineno
      text = "class %s" % args["name"]
      loc = self.source.find_first_text(node.lineno, body_start, text)
    elif isinstance(node, ast.FunctionDef):
      body_start = node.body[0].lineno
      text = "def %s" % args["name"]
      loc = self.source.find_first_text(node.lineno, body_start, text)

    if loc is None:
      loc = get_location(node)

    return loc

  def _get_node_name(self, node):
    if isinstance(node, str):
      # We replace nodes with their names after visiting them.
      return node
    try:
      return super(IndexVisitor, self)._get_node_name(node)
    except NotImplementedError:
      return typename(node)

  def make_def(self, node, **kwargs):
    """Make a definition from a node."""

    if isinstance(node, ast.Name):
      t = typename(node.ctx)
    elif isinstance(node, ast.arg):
      t = "Param"
    else:
      t = typename(node)
    args = {
        "name": get_name(node),
        "scope": self.scope_id(),
        "typ": t,
        "data": None,
        "target": None,
        "doc": None,
    }
    args.update(kwargs)
    defn = Definition(**args)
    line, col = self._get_location(node, args)
    assert line is not None
    defloc = DefLocation(defn.id, source.Location(line, col))
    return (defn, defloc)

  def make_ref(self, node, **kwargs):
    """Make a reference from a node."""

    assert "data" in kwargs  # required kwarg
    args = {
        "name": get_name(node),
        "scope": self.scope_id(),
        "ref_scope": None,
        "typ": typename(node),
        "location": get_location(node),
        "target": None,
    }
    args.update(kwargs)
    return Reference(**args)

  def add_local_def(self, node, **kwargs):
    defn, defloc = self.make_def(node, **kwargs)
    if defn.id not in self.defs:
      self.defs[defn.id] = defn
    self.locs[defn.id].append(defloc)
    self.envs[defn.scope][defn.name] = defn
    return defn

  def add_global_def(self, node, **kwargs):
    kwargs.update({"scope": "module"})
    return self.add_local_def(node, **kwargs)

  def add_local_ref(self, node, **kwargs):
    kwargs.update({"ref_scope": self.scope_id()})
    ref = self.make_ref(node, **kwargs)
    self.refs.append(ref)
    return ref

  def add_closure_ref(self, node, **kwargs):
    """Look for node.name up the chain of scopes."""
    name = get_name(node)
    env, _ = self.current_env.lookup(name)
    if env:
      kwargs.update({"ref_scope": env.scope})
    else:
      # This should never happen! If python has generated a LOAD_DEREF bytecode
      # then we do have the name defined in a parent scope. However, in the
      # interests of not crashing the indexer, fall back to the current scope.
      # TODO(mdemello): We need error logs.
      pass
    ref = self.make_ref(node, **kwargs)
    self.refs.append(ref)
    return ref

  def add_global_ref(self, node, **kwargs):
    kwargs.update({"ref_scope": "module"})
    return self.add_local_ref(node, **kwargs)

  def add_call(self, node, name, func):
    self.calls.append(Funcall(name, func, get_location(node)))

  def add_attr(self, node):
    defn, _ = self.make_def(node)
    self.defs[defn.id] = defn
    env = self.envs[self.scope_id()]
    if env.is_self_attr(node):
      self.envs[self.scope_id()].setattr(node.attr, defn)

  def enter_ClassDef(self, node):
    # TODO(mdemello): For decorated classes, the node's lineno starts at the
    # first decorator, and therefore does not match the opcode's lineno.
    # Likewise, when a class definition spans multiple lines, the AST node
    # starts on the first line but the BUILD_CLASS opcode starts on the last
    # one. Fix when we incorporate asttokens.
    class_name = get_name(node)

    # Python2
    ops = match_opcodes(self.traces, node.lineno, [("BUILD_CLASS", class_name)])
    d = None
    if ops:
      _, _, data = ops[0]
      d = _unwrap(data)
    else:
      # Python3
      ops = match_opcodes(self.traces, node.lineno, [
          ("LOAD_BUILD_CLASS", None),
          ("STORE_NAME", class_name)
      ])
      if len(ops) == 2:
        _, _, data = ops[1]
        d = _unwrap(data)
    assert d, "Did not get pytype data for class %s" % class_name
    defn = self.add_local_def(node, data=data, doc=DocString.from_node(node))
    self.classmap[d[0]] = defn
    super(IndexVisitor, self).enter_ClassDef(node)

  def enter_FunctionDef(self, node):
    ops = match_opcodes(self.traces, node.lineno, [
        ("MAKE_FUNCTION", None),  # py2 has no symbol, py3 has node.name
        ("LOAD_CLOSURE", None)  # Nested functions
    ])
    if ops:
      _, _, data = ops[0]
    else:
      # TODO(mdemello): Add an assert; this should not happen but I would rather
      # not break grok indexing if it does.
      data = None
    fn_def = self.add_local_def(node, data=data, doc=DocString.from_node(node))
    env = self.add_scope(node)
    # TODO(mdemello): Get pytype data for params
    params = [self.add_local_def(v) for v in node.args.args]
    for i, param in enumerate(params):
      self.kythe.add_edge(
          source=self.kythe.vname(fn_def.to_signature()),
          edge_name="param.%d" % i,
          target=self.kythe.vname(param.to_signature()))
    if env.cls:
      if (not has_decorator(node, "classmethod") and
          not has_decorator(node, "staticmethod")):
        # Don't crash if we have buggy code like
        # class A(): def f(): ...
        if params:
          env.self_var = params[0]

  def visit_Name(self, node):
    # We ignore the location returned by match() because we'll recompute the
    # same location anyways.
    # We use pytype trace data to distinguish between local and global
    # variables.
    for unused_loc, (op, symbol, data) in self.match(node):
      d = _unwrap(data)
      if op == "LOAD_GLOBAL":
        ref = self.add_global_ref(node, name=symbol, data=data)
        self.typemap[ref.id] = d
        break
      elif op in ["LOAD_FAST", "LOAD_NAME"]:
        ref = self.add_local_ref(node, name=symbol, data=data)
        self.typemap[ref.id] = d
        break
      elif op in ["LOAD_DEREF"]:
        ref = self.add_closure_ref(node, name=symbol, data=data)
        self.typemap[ref.id] = d
        break
      elif op == "STORE_GLOBAL":
        defn = self.add_global_def(node, name=symbol, data=data)
        self.typemap[defn.id] = d
        break
      elif op in ["STORE_FAST", "STORE_NAME", "STORE_DEREF"]:
        defn = self.add_local_def(node, name=symbol, data=data)
        self.typemap[defn.id] = d
        break
    return node.id

  def visit_Call(self, node):
    name = self._get_node_name(node)
    seen = set()
    for _, (_, _, data) in self.match(node):
      for d in data:
        if d is None:
          continue
        for d1 in d:
          for f in qualified_method(d1):
            if f not in seen:
              self.add_call(node, name, f)
              seen.add(f)
    return name

  def visit_Assign(self, node):
    for v in node.targets:
      if isinstance(v, ast.Attribute):
        self.add_attr(v)

  def visit_Attribute(self, node):
    node_str = self._get_node_name(node)
    # match() returns the location of the attribute, whereas the indexer needs
    # the location of the value on which the attribute is accessed, in order to
    # link function calls. We'll manually adjust the location later.
    for unused_loc, (op, unused_symbol, data) in self.match(node):
      if op == "LOAD_ATTR":
        ref = self.add_local_ref(
            node,
            target=node.value,
            name=node_str,
            data=data)
        if len(data) == 2:
          _, rhs = data
          self.typemap[ref.id] = rhs
        break
      elif op == "STORE_ATTR":
        defn = self.add_local_def(node)
        if self.current_class:
          # We only support attr definitions within a class definition.
          self.current_env.setattr(node.attr, defn)
        break
    return node_str

  def visit_Subscript(self, node):
    return node.value

  def visit_DictComp(self, _node):
    return "<expr>"

  def visit_ListComp(self, _node):
    return "<expr>"

  def process_import(self, node):
    """Common code for Import and ImportFrom."""

    # Only record modules that pytype has resolved in self.modules
    def is_resolved(data):
      return data and isinstance(data[0], abstract.Module)

    def add_import_ref(name, data, loc):
      self.add_global_ref(
          node, name=name, data=data, location=loc, typ="Import")

    for loc, (op, symbol, data) in self.match(node):
      d = self.add_local_def(node, name=symbol)
      defloc = self.locs[d.id][-1]

      # tweak the definition location slightly
      line, _ = loc
      text = self.source.line(line)
      c = text.find("import ")
      new_loc = source.Location(line, c) if c > -1 else loc
      self.locs[d.id][-1] = DefLocation(defloc.def_id, new_loc)

      if not is_resolved(_unwrap(data)):
        continue
      elif op == "STORE_NAME":
        # for |import x.y as z| or |from x import y as z| we want {z: x.y}
        self.modules[d.id] = _unwrap(data)[0].full_name
        add_import_ref(name=symbol, data=data, loc=loc)
      elif op == "IMPORT_NAME":
        # |import x.y| puts both {x: x} and {x.y: x.y} in modules
        add_import_ref(name=symbol, data=data, loc=loc)
        for mod in module_utils.get_all_prefixes(symbol):
          # TODO(mdemello): Create references for every element.
          self.modules[d.scope + "." + mod] = mod

  def visit_Import(self, node):
    self.process_import(node)

  def visit_ImportFrom(self, node):
    self.process_import(node)


# pylint: enable=invalid-name
# pylint: enable=missing-docstring


class Indexer(object):
  """Runs the indexer visitor and collects its results."""

  def __init__(self,
               src,
               loader,
               module_name,
               kythe_args=None):
    self.source = src
    self.loader = loader
    self.resolved_modules = loader.get_resolved_modules()
    self.imports = xref_utils.process_imports_map(loader.imports_map)
    self.module_name = module_name
    self.traces = src.traces
    self.kythe = kythe.Kythe(src, kythe_args)
    self.defs = None
    self.locs = None
    self.refs = None
    self.envs = None
    self.modules = None
    self.typemap = None
    self.classmap = None
    self.calls = None
    self.links = []

    # Optionally preserve the pytype vm so we can access the types later
    self.vm = None

  def index(self, code_ast):
    """Index an AST corresponding to self.source."""

    v = IndexVisitor(self.source, self.module_name, self.kythe)
    v.visit(code_ast)
    self.defs = v.defs
    self.locs = v.locs
    self.refs = v.refs
    self.envs = v.envs
    self.modules = v.modules
    self.typemap = v.typemap
    self.classmap = v.classmap
    self.calls = v.calls

  def get_def_offsets(self, defloc):
    """Get the byte offsets for a definition."""

    defn = self.defs[defloc.def_id]
    typ = defn.typ
    if typ == "Attribute":
      start, end = self._get_attr_bounds(defn.name, defloc.location)
    else:
      start = self.source.get_offset(defloc.location)
      if typ in DEF_OFFSETS:
        start += DEF_OFFSETS[typ]
      if typ == "Import" or typ == "ImportFrom":
        # We link an import def to the word "import"
        end = start + len("import")
      else:
        end = start + len(defn.name)
    return (start, end)

  def get_doc_offsets(self, doc):
    """Get the byte offsets for a docstring."""

    start = self.source.get_offset(doc.location)
    end = start + doc.length
    return (start, end)

  def finalize(self):
    """Postprocess the information gathered by the tree visitor.

    Note that these functions need to be run in order; some of them depend on
    information generated by previous ones.
    """

    links = self._lookup_refs()
    self.links = links
    self._process_deflocs()
    self._process_links(links)
    self._process_calls(links)

  def _process_deflocs(self):
    """Generate kythe edges for definitions."""

    for def_id in self.locs:
      defn = self.defs[def_id]
      for defloc in self.locs[def_id]:
        defn = self.defs[defloc.def_id]
        defn_vname = self.kythe.vname(defn.to_signature())
        start, end = self.get_def_offsets(defloc)
        anchor_vname = self.kythe.add_anchor(start, end)
        self.kythe.add_fact(
            source=defn_vname,
            fact_name="node/kind",
            fact_value=defn.node_kind())
        self.kythe.add_edge(
            source=anchor_vname,
            target=defn_vname,
            edge_name="defines/binding")

        # Emit a docstring if we have one.
        doc = defn.doc
        if doc:
          doc_vname = self.kythe.vname(defn.doc_signature())
          start, end = self.get_doc_offsets(defn.doc)
          anchor_vname = self.kythe.add_anchor(start, end)
          self.kythe.add_fact(
              source=doc_vname,
              fact_name="node/kind",
              fact_value="doc")
          self.kythe.add_fact(
              source=doc_vname,
              fact_name="text",
              fact_value=doc.text)
          self.kythe.add_edge(
              source=anchor_vname,
              target=doc_vname,
              edge_name="defines")
          self.kythe.add_edge(
              source=doc_vname,
              target=defn_vname,
              edge_name="documents")

  def _get_attr_bounds(self, name, location):
    """Calculate the anchor bounds for an attr access."""
    return self.get_anchor_bounds(
        *self.source.get_attr_location(name, location))

  def get_anchor_bounds(self, location, length):
    """Generate byte offsets from a location and length."""

    start = self.source.get_offset(location)
    end = start + length
    return (start, end)

  def get_ref_bounds(self, ref):
    if ref.typ == "Attribute":
      return self._get_attr_bounds(ref.name, ref.location)
    else:
      return self.get_anchor_bounds(ref.location, len(ref.name))

  def _make_defn_vname(self, defn):
    """Convert a definition into a kythe vname."""
    if isinstance(defn, Remote):
      remote = defn.module
      if remote in self.resolved_modules:
        if remote in self.imports:
          # The canonical path from the imports_map is the best bet for
          # module->filepath translation.
          path = self.imports[remote]
        else:
          # Fallback to the filepath of the stub file, though this is not always
          # accurate due to overrides.
          path = self.resolved_modules[remote].filename
        path = xref_utils.get_module_filepath(path)
        if defn.name == IMPORT_FILE_MARKER:
          sig = kythe.FILE_ANCHOR_SIGNATURE
        else:
          sig = "module." + defn.name
        if path.startswith("pytd:"):
          return self.kythe.builtin_vname(
              sig, "pytd:" + self.resolved_modules[remote].module_name)
        else:
          return self.kythe.vname(sig, path)
      else:
        # Don't generate vnames for unresolved modules.
        return None
    else:
      return self.kythe.vname(defn.to_signature())

  def _process_links(self, links):
    """Generate kythe edges for references."""

    for ref, defn in links:
      if not isinstance(defn, (Definition, Remote, Module)):
        # TODO(mdemello): Fixes needed for chained method calls.
        continue
      start, end = self.get_ref_bounds(ref)
      vname = self.kythe.add_anchor(start, end)
      target = self._make_defn_vname(defn)
      if target:
        self.kythe.add_edge(
            source=vname,
            target=target,
            edge_name="ref")

  def _process_calls(self, links):
    """Generate kythe edges for function calls.

    Checks if a function call corresponds to a resolved reference, and generates
    a ref/call to that references's source definition if so.

    Args:
      links: A list of (reference, definition) tuples.
    """

    link_map = collections.defaultdict(list)
    for ref, defn in links:
      link_map[ref.location].append((ref, defn))

    for call in self.calls:
      call_links = link_map[call.location]
      call_ref = None
      call_defn = None
      for ref, d in call_links:
        if ref.name == call.name:
          call_ref = ref
          call_defn = d
          break
      if call_defn:
        target = self._make_defn_vname(call_defn)
        if target:
          start, end = self.get_ref_bounds(call_ref)
          anchor_vname = self.kythe.anchor_vname(start, end)
          self.kythe.add_edge(
              source=anchor_vname,
              target=target,
              edge_name="ref/call")
          # The call is a child of the enclosing function/class (this lets us
          # generate call graphs).
          if ref.scope != "module":
            parent_defn = self.defs.get(call_ref.scope)
            if parent_defn:
              # TODO(mdemello): log the 'else' case; it should never happen.
              self.kythe.add_edge(
                  source=anchor_vname,
                  target=self.kythe.vname(parent_defn.to_signature()),
                  edge_name="childof")
            else:
              assert False, ref

  def _lookup_remote_symbol(self, ref, defn):
    """Try to look up a definition in an imported module."""

    if defn.id in self.modules:
      remote = self.modules[defn.id]
      resolved = True
    elif defn.typ in ["Import", "ImportFrom"]:
      # Allow unresolved modules too.
      remote = defn.name
      resolved = False
    else:
      return None
    name = ref.name
    if name.startswith(remote):
      name = name[(len(remote) + 1):]
    return Remote(module=remote, name=name, resolved=resolved)

  def _lookup_class_attr(self, name, attr):
    """Look up a class attribute in the environment."""

    env = self.envs["module"]
    if name not in env.env:
      return None
    d = env.env[name]
    class_env = self.envs[d.id]
    _, defn = class_env.lookup(attr)
    return defn

  def _get_attribute_class(self, obj):
    """Look up the class of an attribute target."""

    if isinstance(obj, abstract.Module):
      return Module(obj.name)
    elif isinstance(obj, abstract.InterpreterClass):
      return self.classmap.get(obj)
    elif isinstance(obj, abstract.PyTDClass):
      if obj.module:
        return Remote(obj.module, obj.name, resolved=True)
      else:
        # Corner case: a namedtuple in the MRO of a class will generate a
        # PyTDClass even though it's in the current module.
        # TODO(mdemello): We need special handling for namedtuples to generate
        # and populate a class.
        return None
    else:
      return None

  def _get_mro(self, obj):
    if isinstance(obj, abstract.InterpreterClass):
      return obj.mro
    elif isinstance(obj, abstract.Instance):
      return obj.cls.mro
    else:
      return []

  def _is_pytype_module(self, obj):
    return isinstance(obj, abstract.Module)

  def _lookup_attribute_by_type(self, r, attr_name):
    """Look up an attribute using pytype annotations."""

    lhs, rhs = r.data
    links = []
    for l in lhs:
      if self._is_pytype_module(l):
        lookup = [l]
      else:
        lookup = self._get_mro(l)
      for pytype_cls in lookup:
        cls = self._get_attribute_class(pytype_cls)
        if cls:
          if isinstance(cls, Definition):
            env = self.envs[cls.id]
            _, attr_value = env.lookup(attr_name)
            if not attr_value and isinstance(l, abstract.Instance):
              try:
                attr_value = env.getattr(attr_name)
              except AttrError:
                # We will walk up the MRO if we can't find anything.
                continue
            if attr_value:
              links.append((r, attr_value))
              break
          elif isinstance(cls, Module):
            # Probably extra-cautious about rhs not being a single binding, but
            # better to check than crash here.
            if len(rhs) == 1 and self._is_pytype_module(rhs[0]):
              # e.g. import x.y; a = x.y
              links.append((r, cls.submodule(attr_name)))
            else:
              links.append((r, cls.attr(attr_name)))
            break
          elif isinstance(cls, Remote):
            links.append((r, cls.attr(attr_name)))
            break
    return links

  def _lookup_refs(self):
    """Look up references to generate links."""

    links = []

    for r in self.refs:
      if r.typ == "Attribute":
        attr_name = r.name.split(".")[-1]
        defs = self._lookup_attribute_by_type(r, attr_name)
        if defs:
          links.extend(defs)
          continue
        else:
          env = self.envs[r.scope]
          env, defn = env.lookup(r.target)
          if defn:
            # See if this is a definition from an imported module first.
            remote = self._lookup_remote_symbol(r, defn)
            if remote:
              links.append((r, remote))
            else:
              # See if we can figure out the class of a bound attribute from the
              # typemap.
              typ = self.typemap.get(defn.id)
              if typ:
                for x in PytypeValue.from_data(typ):
                  if isinstance(x, Remote):
                    links.append((r, x.attr(attr_name)))
                  elif x.typ == "Class":
                    d = self._lookup_class_attr(x.name, attr_name)
                    if d:
                      links.append((r, d))
                    else:
                      # Fall back to <module>.<name>
                      links.append((r, x))
                  else:
                    links.append((r, x))
              else:
                links.append((r, defn))
      elif r.typ == "Import":
        if r.name in self.resolved_modules:
          module = r.name
        else:
          module = _unwrap(r.data)[0].full_name
        remote = Remote(module=module, name=IMPORT_FILE_MARKER, resolved=True)
        links.append((r, remote))
      else:
        try:
          env, defn = self.envs[r.scope].lookup(r.name)
        except KeyError:
          env, defn = None, None

        if defn:
          links.append((r, defn))
        else:
          data = PytypeValue.from_data(_unwrap(r.data))
          if data:
            for x in data:
              links.append((r, x))

    return links


class PytypeError(Exception):
  """Wrap exceptions raised by the indexer."""


class VmTrace(source.AbstractTrace):

  def __repr__(self):
    types_repr = tuple(t and [typename(x) for x in t] for t in self.types)
    return "%s %s" % (super(VmTrace, self).__repr__(), types_repr)


def process_file(options, source_text=None, kythe_args=None,
                 preserve_pytype_vm=False):
  """Process a single file and return cross references.

  Args:
    options: A dictionary of pytype options.
    source_text: Optional text of the file; will be read from the file pointed
      to by options.input if not supplied.
    kythe_args: Extra args for generating the kythe index
    preserve_pytype_vm: Preserve the pytype vm in the indexer

  Returns:
    The Indexer object used for indexing.

  Raises:
    PytypeError if pytype fails.
  """
  # We bind the global ast variable in this function.
  global ast

  errorlog = errors.ErrorLog()
  loader = load_pytd.create_loader(options)
  src = source_text or io.read_source_file(options.input)
  vm = analyze.CallTracer(
      errorlog=errorlog,
      options=options,
      generate_unknowns=options.protocols,
      store_all_calls=False,
      loader=loader)
  with io.wrap_pytype_exceptions(PytypeError, filename=options.input):
    analyze.infer_types(
        src=src,
        filename=options.input,
        errorlog=errorlog,
        options=options,
        loader=loader,
        tracer_vm=vm)

  major, minor = options.python_version
  if major == 2:
    # python2.7 is the only supported py2 version.
    ast_root_node = ast27.parse(src, options.input)
    ast = ast27
  else:
    ast_root_node = ast3.parse(src, options.input, feature_version=minor)
    ast = ast3

  # TODO(mdemello): Get from args
  module_name = "module"
  src_code = source.Code(src, vm.opcode_traces, VmTrace, filename=options.input)
  ix = Indexer(src_code, vm.loader, module_name, kythe_args)
  ix.index(ast_root_node)
  ix.finalize()
  if preserve_pytype_vm:
    ix.vm = vm
  return ix
