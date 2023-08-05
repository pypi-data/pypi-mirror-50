// A Bison parser, made by GNU Bison 3.0.4.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// Take the name prefix into account.
#define yylex   pytypelex

// First part of user declarations.

#line 39 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:404

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

#include "parser.tab.hh"

// User implementation prologue.

#line 53 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:412
// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:413

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 81 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:413


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (/*CONSTCOND*/ false)
# endif


// Suppress unused-variable warnings by "using" E.
#define YYUSE(E) ((void) (E))

// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << std::endl;                  \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yystack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE(Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void>(0)
# define YY_STACK_PRINT()                static_cast<void>(0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:479
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:479

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr = "";
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              // Fall through.
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }


  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
    :
#if PYTYPEDEBUG
      yydebug_ (false),
      yycdebug_ (&std::cerr),
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}


  /*---------------.
  | Symbol types.  |
  `---------------*/

  inline
  parser::syntax_error::syntax_error (const location_type& l, const std::string& m)
    : std::runtime_error (m)
    , location (l)
  {}

  // basic_symbol.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol ()
    : value ()
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& other)
    : Base (other)
    , value ()
    , location (other.location)
  {
    value = other.value;
  }


  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const semantic_type& v, const location_type& l)
    : Base (t)
    , value (v)
    , location (l)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const location_type& l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::~basic_symbol ()
  {
    clear ();
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::clear ()
  {
    Base::clear ();
  }

  template <typename Base>
  inline
  bool
  parser::basic_symbol<Base>::empty () const
  {
    return Base::type_get () == empty_symbol;
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move(s);
    value = s.value;
    location = s.location;
  }

  // by_type.
  inline
  parser::by_type::by_type ()
    : type (empty_symbol)
  {}

  inline
  parser::by_type::by_type (const by_type& other)
    : type (other.type)
  {}

  inline
  parser::by_type::by_type (token_type t)
    : type (yytranslate_ (t))
  {}

  inline
  void
  parser::by_type::clear ()
  {
    type = empty_symbol;
  }

  inline
  void
  parser::by_type::move (by_type& that)
  {
    type = that.type;
    that.clear ();
  }

  inline
  int
  parser::by_type::type_get () const
  {
    return type;
  }


  // by_state.
  inline
  parser::by_state::by_state ()
    : state (empty_state)
  {}

  inline
  parser::by_state::by_state (const by_state& other)
    : state (other.state)
  {}

  inline
  void
  parser::by_state::clear ()
  {
    state = empty_state;
  }

  inline
  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  inline
  parser::by_state::by_state (state_type s)
    : state (s)
  {}

  inline
  parser::symbol_number_type
  parser::by_state::type_get () const
  {
    if (state == empty_state)
      return empty_symbol;
    else
      return yystos_[state];
  }

  inline
  parser::stack_symbol_type::stack_symbol_type ()
  {}


  inline
  parser::stack_symbol_type::stack_symbol_type (state_type s, symbol_type& that)
    : super_type (s, that.location)
  {
    value = that.value;
    // that is emptied.
    that.type = empty_symbol;
  }

  inline
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }


  template <typename Base>
  inline
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.type_get ())
    {
            case 3: // NAME

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 421 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 4: // NUMBER

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 5: // LEXERROR

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 435 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 49: // start

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 442 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 50: // unit

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 449 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 51: // alldefs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 456 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 53: // classdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 463 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 54: // class_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 55: // parents

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 477 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 56: // parent_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 484 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 57: // parent

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 58: // maybe_class_funcs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 59: // class_funcs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 505 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 60: // funcdefs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 61: // if_stmt

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 519 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 62: // if_and_elifs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 526 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 63: // class_if_stmt

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 64: // class_if_and_elifs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 540 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 65: // if_cond

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 547 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 66: // elif_cond

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 67: // else_cond

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 561 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 68: // condition

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 568 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 69: // version_tuple

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 575 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 70: // condition_op

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.str)); }
#line 582 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 71: // constantdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 72: // importdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 73: // import_items

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 603 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 74: // import_item

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 610 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 75: // import_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 617 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 76: // from_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 77: // from_items

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 631 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 78: // from_item

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 79: // alias_or_constant

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 645 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 80: // typevardef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 81: // typevar_args

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 659 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 82: // typevar_kwargs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 83: // typevar_kwarg

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 673 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 84: // funcdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 85: // funcname

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 86: // decorators

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 694 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 87: // decorator

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 701 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 88: // maybe_async

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 708 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 89: // params

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 715 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 90: // param_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 91: // param

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 729 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 92: // param_type

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 93: // param_default

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 743 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 94: // param_star_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 750 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 95: // return

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 757 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 97: // maybe_body

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 99: // body

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 771 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 100: // body_stmt

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 778 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 101: // type_parameters

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 785 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 102: // type_parameter

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 792 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 103: // type

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 799 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 104: // named_tuple_fields

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 105: // named_tuple_field_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 813 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 106: // named_tuple_field

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 108: // coll_named_tuple_fields

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 109: // coll_named_tuple_field_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 834 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 110: // coll_named_tuple_field

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 841 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 111: // maybe_type_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 848 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 112: // type_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 855 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 113: // type_tuple_elements

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 862 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 114: // type_tuple_literal

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 869 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 115: // dotted_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 876 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 116: // getitem_key

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 883 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 117: // maybe_number

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 890 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;


      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo,
                                     const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    symbol_number_type yytype = yysym.type_get ();
    // Avoid a (spurious) G++ 4.8 warning about "array subscript is
    // below array bounds".
    if (yysym.empty ())
      std::abort ();
    yyo << (yytype < yyntokens_ ? "token" : "nterm")
        << ' ' << yytname_[yytype] << " ("
        << yysym.location << ": ";
    YYUSE (yytype);
    yyo << ')';
  }
#endif

  inline
  void
  parser::yypush_ (const char* m, state_type s, symbol_type& sym)
  {
    stack_symbol_type t (s, sym);
    yypush_ (m, t);
  }

  inline
  void
  parser::yypush_ (const char* m, stack_symbol_type& s)
  {
    if (m)
      YY_SYMBOL_PRINT (m, s);
    yystack_.push (s);
  }

  inline
  void
  parser::yypop_ (unsigned int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  inline parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - yyntokens_] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - yyntokens_];
  }

  inline bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  inline bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::parse ()
  {
    // State.
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

    // FIXME: This shoud be completely indented.  It is not yet to
    // avoid gratuitous conflicts when merging into the master branch.
    try
      {
    YYCDEBUG << "Starting parse" << std::endl;


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, yyla);

    // A new symbol was pushed on the stack.
  yynewstate:
    YYCDEBUG << "Entering state " << yystack_[0].state << std::endl;

    // Accept?
    if (yystack_[0].state == yyfinal_)
      goto yyacceptlab;

    goto yybackup;

    // Backup.
  yybackup:

    // Try to take a decision without lookahead.
    yyn = yypact_[yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token: ";
        try
          {
            yyla.type = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
        catch (const syntax_error& yyexc)
          {
            error (yyexc);
            goto yyerrlab1;
          }
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.type_get ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.type_get ())
      goto yydefault;

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", yyn, yyla);
    goto yynewstate;

  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;

  /*-----------------------------.
  | yyreduce -- Do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_(yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Compute the default @$.
      {
        slice<stack_symbol_type, stack_type> slice (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, slice, yylen);
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
      try
        {
          switch (yyn)
            {
  case 2:
#line 133 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1129 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 3:
#line 134 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1135 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 5:
#line 142 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1141 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 6:
#line 143 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1147 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 7:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1153 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 8:
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1164 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 9:
#line 151 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1170 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 10:
#line 152 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1176 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 11:
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1186 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 12:
#line 158 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1192 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 15:
#line 169 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNN)", (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1201 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 16:
#line 176 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1214 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 17:
#line 187 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1220 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 18:
#line 188 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1226 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 19:
#line 189 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1232 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 20:
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1238 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 21:
#line 194 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1244 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 22:
#line 198 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1250 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 23:
#line 199 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1256 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 24:
#line 203 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1262 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 25:
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1268 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 26:
#line 205 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1274 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 27:
#line 209 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1280 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 29:
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1286 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 30:
#line 215 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1296 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 31:
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1302 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 32:
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1312 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 33:
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1318 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 34:
#line 227 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1324 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 35:
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1332 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 37:
#line 240 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1340 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 38:
#line 244 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1348 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 39:
#line 263 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1356 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 41:
#line 271 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1364 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 42:
#line 275 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1372 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 43:
#line 287 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1378 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 44:
#line 291 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1384 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 45:
#line 295 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1390 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 46:
#line 299 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 47:
#line 302 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1406 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 48:
#line 305 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1414 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 49:
#line 308 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1422 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 50:
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 51:
#line 312 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 52:
#line 313 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 53:
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 54:
#line 319 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 55:
#line 320 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1460 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 56:
#line 326 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<"; }
#line 1466 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 57:
#line 327 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">"; }
#line 1472 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 58:
#line 328 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<="; }
#line 1478 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 59:
#line 329 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">="; }
#line 1484 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 60:
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "=="; }
#line 1490 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 61:
#line 331 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "!="; }
#line 1496 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 62:
#line 335 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1505 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 63:
#line 339 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kByteString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1514 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 64:
#line 343 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kUnicodeString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1523 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 65:
#line 347 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1532 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 66:
#line 351 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1541 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 67:
#line 355 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1550 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 68:
#line 359 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1559 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 69:
#line 363 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1568 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 70:
#line 370 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1577 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 71:
#line 374 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1586 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 72:
#line 378 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1597 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 73:
#line 384 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1608 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 74:
#line 393 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1614 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 75:
#line 394 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1620 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 77:
#line 398 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1626 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 79:
#line 404 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1635 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 81:
#line 412 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1641 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 82:
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1647 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 83:
#line 417 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1653 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 84:
#line 418 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1659 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 86:
#line 423 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1667 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 87:
#line 426 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1675 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 88:
#line 429 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1683 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 89:
#line 432 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1691 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 90:
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1697 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 91:
#line 439 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1703 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 92:
#line 443 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1712 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 93:
#line 450 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1718 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 94:
#line 451 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1724 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 95:
#line 452 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1730 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 96:
#line 453 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 97:
#line 457 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1742 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 98:
#line 458 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1748 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 99:
#line 462 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1754 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 100:
#line 466 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[8].value.obj), (yystack_[7].value.obj), (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      //
      // TODO(dbaum): Consider making this smarter and only ignoring decorators
      // when they are empty.  Making decorators non-nullable and having two
      // productions for funcdef would be a reasonable solution.
      yylhs.location.begin = yystack_[6].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1773 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 101:
#line 483 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1779 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 102:
#line 484 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1785 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 103:
#line 488 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1791 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 104:
#line 489 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1797 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 105:
#line 493 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1803 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 106:
#line 497 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_True; }
#line 1809 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 107:
#line 498 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_False; }
#line 1815 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 108:
#line 502 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1821 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 109:
#line 503 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 110:
#line 515 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1833 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 111:
#line 516 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1839 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 112:
#line 520 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1845 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 113:
#line 521 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1851 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 114:
#line 522 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1857 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 115:
#line 523 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1863 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 116:
#line 527 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1869 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 117:
#line 528 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1875 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 118:
#line 532 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1881 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 119:
#line 533 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1887 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 120:
#line 534 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1893 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 121:
#line 535 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1899 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 122:
#line 539 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1905 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 123:
#line 540 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1911 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 124:
#line 544 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1917 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 125:
#line 545 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1923 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 126:
#line 549 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_DecRef((yystack_[0].value.obj)); }
#line 1929 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 127:
#line 553 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1935 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 128:
#line 554 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1941 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 129:
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1947 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 137:
#line 569 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1953 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 138:
#line 570 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1959 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 139:
#line 574 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1965 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 140:
#line 575 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1971 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 141:
#line 576 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1977 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 142:
#line 580 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1983 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 143:
#line 581 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1989 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 144:
#line 585 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1995 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 145:
#line 586 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2001 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 146:
#line 590 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2010 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 147:
#line 594 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2019 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 148:
#line 598 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // This rule is needed for Callable[[...], ...]
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2029 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 149:
#line 603 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2038 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 150:
#line 607 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2047 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 151:
#line 611 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2053 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 152:
#line 612 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2059 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 153:
#line 613 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2065 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 154:
#line 614 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2071 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 155:
#line 615 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2077 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 156:
#line 619 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2083 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 157:
#line 620 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 158:
#line 624 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2095 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 159:
#line 625 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2101 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 160:
#line 629 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2107 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 163:
#line 638 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2113 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 164:
#line 639 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2119 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 165:
#line 643 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2127 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 166:
#line 646 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2133 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 167:
#line 650 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2139 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 168:
#line 653 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2145 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 169:
#line 654 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2151 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 170:
#line 658 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2157 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 171:
#line 659 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2163 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 172:
#line 666 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2169 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 173:
#line 667 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2175 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 174:
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2184 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 175:
#line 681 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2193 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 176:
#line 687 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2202 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 177:
#line 694 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2208 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 178:
#line 695 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 179:
#line 709 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 180:
#line 710 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2240 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 181:
#line 715 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2250 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 182:
#line 723 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2256 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 183:
#line 724 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = NULL; }
#line 2262 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;


#line 2266 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
            default:
              break;
            }
        }
      catch (const syntax_error& yyexc)
        {
          error (yyexc);
          YYERROR;
        }
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;
      YY_STACK_PRINT ();

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, yylhs);
    }
    goto yynewstate;

  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        error (yyla.location, yysyntax_error_ (yystack_[0].state, yyla));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.type_get () == yyeof_)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:

    /* Pacify compilers like GCC when the user code never invokes
       YYERROR and the label yyerrorlab therefore never appears in user
       code.  */
    if (false)
      goto yyerrorlab;
    yyerror_range[1].location = yystack_[yylen - 1].location;
    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    goto yyerrlab1;

  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    {
      stack_symbol_type error_token;
      for (;;)
        {
          yyn = yypact_[yystack_[0].state];
          if (!yy_pact_value_is_default_ (yyn))
            {
              yyn += yyterror_;
              if (0 <= yyn && yyn <= yylast_ && yycheck_[yyn] == yyterror_)
                {
                  yyn = yytable_[yyn];
                  if (0 < yyn)
                    break;
                }
            }

          // Pop the current state because it cannot handle the error token.
          if (yystack_.size () == 1)
            YYABORT;

          yyerror_range[1].location = yystack_[0].location;
          yy_destroy_ ("Error: popping", yystack_[0]);
          yypop_ ();
          YY_STACK_PRINT ();
        }

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = yyn;
      yypush_ ("Shifting", error_token);
    }
    goto yynewstate;

    // Accept.
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;

    // Abort.
  yyabortlab:
    yyresult = 1;
    goto yyreturn;

  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack"
                 << std::endl;
        // Do not try to display the values of the reclaimed symbols,
        // as their printer might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what());
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (state_type yystate, const symbol_type& yyla) const
  {
    // Number of reported tokens (one for the "unexpected", one per
    // "expected").
    size_t yycount = 0;
    // Its maximum.
    enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
    // Arguments of yyformat.
    char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];

    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state
         merging (from LALR or IELR) and default reductions corrupt the
         expected token list.  However, the list is correct for
         canonical LR with one exception: it will still contain any
         token that will not be accepted due to an error action in a
         later state.
    */
    if (!yyla.empty ())
      {
        int yytoken = yyla.type_get ();
        yyarg[yycount++] = yytname_[yytoken];
        int yyn = yypact_[yystate];
        if (!yy_pact_value_is_default_ (yyn))
          {
            /* Start YYX at -YYN if negative to avoid negative indexes in
               YYCHECK.  In other words, skip the first -YYN actions for
               this state because they are default actions.  */
            int yyxbegin = yyn < 0 ? -yyn : 0;
            // Stay within bounds of both yycheck and yytname.
            int yychecklim = yylast_ - yyn + 1;
            int yyxend = yychecklim < yyntokens_ ? yychecklim : yyntokens_;
            for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
              if (yycheck_[yyx + yyn] == yyx && yyx != yyterror_
                  && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
                {
                  if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                    {
                      yycount = 1;
                      break;
                    }
                  else
                    yyarg[yycount++] = yytname_[yyx];
                }
          }
      }

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
        YYCASE_(0, YY_("syntax error"));
        YYCASE_(1, YY_("syntax error, unexpected %s"));
        YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    size_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += yytnamerr_ (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short int parser::yypact_ninf_ = -297;

  const short int parser::yytable_ninf_ = -183;

  const short int
  parser::yypact_[] =
  {
      -7,  -297,    73,    87,   361,   135,  -297,  -297,   -14,   142,
      86,   163,    41,  -297,  -297,   231,   145,  -297,  -297,  -297,
    -297,  -297,    55,  -297,   224,   151,  -297,   154,  -297,    86,
     330,   312,    89,  -297,    80,    27,   168,   157,  -297,    86,
     189,   241,   179,  -297,   163,  -297,   271,  -297,   261,   268,
     224,   224,  -297,   147,   175,  -297,   278,   284,  -297,  -297,
     224,   187,  -297,    12,   286,   307,    86,    86,  -297,  -297,
    -297,  -297,   323,  -297,  -297,   329,    92,   344,   163,  -297,
    -297,   350,    34,    32,  -297,    34,   330,   340,   349,  -297,
      49,   120,   364,   370,   311,   338,   294,   341,   224,   224,
     356,  -297,   202,   378,   224,   131,   345,  -297,   343,  -297,
     325,  -297,   338,   352,  -297,   372,  -297,   351,   346,   353,
    -297,  -297,   385,  -297,  -297,  -297,  -297,   373,  -297,  -297,
    -297,   111,  -297,   352,   354,  -297,    34,    42,   352,  -297,
    -297,   275,  -297,  -297,  -297,   355,   357,   358,  -297,  -297,
     224,  -297,   380,  -297,   352,  -297,   359,  -297,   338,   360,
     313,   211,   224,   362,   224,  -297,   233,   248,   332,   390,
     363,   397,   328,  -297,   111,   352,  -297,   285,   292,  -297,
      17,   365,   366,   338,  -297,   202,   367,   247,   374,  -297,
    -297,   338,   338,  -297,   338,  -297,  -297,  -297,   232,  -297,
     352,    10,  -297,   368,   112,  -297,  -297,    47,  -297,  -297,
    -297,  -297,   369,  -297,    15,   375,   371,  -297,   369,    93,
     376,    50,   377,  -297,  -297,   379,   381,  -297,   382,  -297,
       5,   386,   254,  -297,  -297,  -297,  -297,   390,   333,  -297,
    -297,   224,   383,  -297,   399,   384,   238,  -297,  -297,   407,
    -297,   387,  -297,  -297,  -297,  -297,   388,  -297,  -297,   224,
     412,   247,   391,  -297,   295,  -297,  -297,   231,   389,  -297,
    -297,  -297,  -297,  -297,   413,   338,    95,  -297,  -297,   224,
     392,    17,   393,   394,   395,   420,   396,   338,   379,  -297,
     381,  -297,   173,   398,   400,   403,   401,  -297,  -297,  -297,
     338,   317,  -297,  -297,  -297,   224,  -297,  -297,  -297,  -297,
     405,   410,  -297,  -297,   164,   304,   352,   190,  -297,  -297,
     282,   402,   224,   414,   144,  -297,   415,   215,  -297,  -297,
    -297,   406,   299,   306,  -297,   224,   198,  -297,  -297,  -297,
    -297,   186,   416,  -297,  -297,  -297,   338,   411,  -297,  -297,
    -297
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   104,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    36,     0,     5,     7,     8,
      10,     6,   107,     3,     0,     0,    16,    19,   177,     0,
      43,     0,    14,    75,    76,     0,     0,    78,    45,     0,
       0,     0,     0,   106,     0,   103,     0,   155,     0,     0,
       0,   169,   154,    14,   146,    62,     0,    66,    63,    64,
       0,    91,    65,     0,     0,     0,     0,     0,    60,    61,
      58,    59,   183,    56,    57,     0,     0,     0,     0,    70,
      13,     0,     0,     0,    79,     0,    44,     0,     0,    12,
      14,     0,     0,     0,     0,   171,     0,   162,     0,     0,
       0,    68,     0,     0,     0,     0,   162,   176,   177,    18,
       0,    21,    22,    14,    52,    51,    50,   179,     0,     0,
     178,    46,     0,    47,   126,    74,    77,    85,    86,    87,
      88,     0,    89,    14,    80,    84,     0,     0,    14,    12,
      12,   104,   105,   101,   102,     0,     0,     0,   151,   148,
     161,   168,   153,   152,    14,   145,   162,   143,   144,    93,
      14,     0,   161,     0,     0,    17,     0,     0,     0,   183,
       0,     0,     0,    72,     0,    14,    71,   104,   104,    37,
     109,     0,     0,   170,    69,   161,     0,     0,     0,    67,
     175,   173,   172,   174,    23,    20,   184,   185,    34,    15,
      14,     0,   182,   180,     0,    90,    81,     0,    83,    73,
      38,    35,   117,   115,   113,     0,   162,   111,   117,     0,
       0,     0,     0,   142,   147,   177,    95,    98,    94,    92,
      34,     0,   104,    27,    24,    48,    49,   183,     0,    53,
      82,     0,   121,   122,     0,   125,    14,   108,   114,     0,
     157,   162,   159,   149,   167,   164,   162,   166,   150,     0,
       0,     0,     0,    25,     0,    33,    32,    40,     0,    29,
      30,    31,   181,    54,     0,   116,     0,   112,   123,     0,
     136,     0,     0,   161,     0,   161,     0,    99,     0,    97,
      96,    26,     0,     0,     0,     0,     0,   118,   119,   120,
     124,     0,   100,   129,   110,     0,   158,   156,   165,   163,
       0,     0,    34,    55,     0,     0,   130,   162,    34,    34,
     104,     0,     0,     0,     0,   138,     0,     0,   132,   131,
     161,     0,   104,   104,    41,     0,   140,   135,   128,   137,
     134,     0,     0,   160,    42,    39,   139,     0,   127,   133,
     141
  };

  const short int
  parser::yypgoto_[] =
  {
    -297,  -297,   427,   -82,   -50,  -230,  -297,  -297,  -297,   263,
    -297,   210,  -296,  -297,  -297,  -297,  -297,  -226,   180,   182,
      91,   249,   274,  -224,  -297,  -297,   404,   439,   -72,   321,
     -59,  -220,  -297,  -297,   192,   194,  -215,  -297,  -297,  -297,
    -297,  -297,  -297,   174,   239,  -297,  -297,  -297,   -42,  -297,
    -297,   129,  -160,  -297,   273,   -24,  -297,  -297,   176,  -105,
    -297,  -297,   177,  -297,   276,  -297,  -297,    -1,  -297,  -165,
    -162
  };

  const short int
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    79,    13,    27,    64,   110,   111,
     199,   231,   232,    14,    15,   266,   267,    16,    40,    41,
      30,   123,    76,    17,    18,    32,    33,    84,   133,   134,
     135,    19,    20,   188,   226,   227,    21,   145,    22,    45,
      46,   215,   216,   217,   242,   277,   218,   280,    80,   302,
     303,   324,   325,   156,   157,    61,   220,   251,   252,   151,
     222,   256,   257,    96,    97,   106,    62,    54,   118,   119,
     233
  };

  const short int
  parser::yytable_[] =
  {
      53,   163,   265,   101,   203,   200,   268,   141,   269,    31,
      34,    37,   270,   138,   235,   108,   320,   271,   243,   196,
     212,    24,   332,   333,     1,    25,    94,    95,    31,   197,
      28,    47,    48,    49,    37,    28,   105,   127,    31,   112,
     142,   213,    82,    90,    28,    28,   122,   136,    50,   109,
     127,   186,    51,   254,   128,   129,   130,   177,   178,    52,
     244,    43,   214,   167,   175,    31,    31,   128,   129,   130,
     131,    83,   272,     6,   152,   153,   137,    34,   158,   132,
     160,    77,    37,   173,   240,    35,   137,     7,   176,    28,
     265,   255,   132,    75,   268,   121,   269,    81,   297,   298,
     270,    44,   265,   265,   184,   271,   268,   268,   269,   269,
     189,   247,   270,   270,   127,   208,   238,   271,   271,   299,
      65,    77,    29,   143,    75,   209,   183,    78,   122,   249,
      86,   128,   129,   130,   250,    23,    37,   191,   192,   316,
     194,   144,   112,    98,    99,    26,   284,   321,   208,   239,
     234,   286,   326,   328,    28,    55,   132,   115,   116,    98,
      99,   158,   322,    95,   339,   342,    28,   321,   148,   161,
      47,    48,    49,    56,   338,    57,    28,    55,   196,    77,
      42,   339,   322,    85,    58,    59,   100,    60,   197,   321,
      63,    51,    47,    48,    49,   323,   281,    57,    52,    98,
      99,    75,    98,    99,   322,    28,    58,    59,    89,    60,
      98,    99,   331,    51,    28,   102,   348,   275,   321,    75,
      52,    47,    48,    49,    87,   107,   155,    28,   330,   196,
      47,    48,    49,   322,   347,   287,   108,   183,    50,   197,
      38,    39,    51,    47,    48,    49,   196,    50,   190,    52,
     225,    51,    47,    48,    49,   300,   197,   264,    52,   315,
      50,     9,   196,   230,    51,    10,    47,    48,    49,    50,
      77,    52,   197,    51,   329,  -161,    88,   198,     8,    91,
      52,   317,     9,    50,   -28,   264,    10,    51,     8,     9,
      11,    12,     9,    10,    52,     8,    10,    92,   336,     9,
      11,    12,   264,    10,    93,   179,     9,    11,    12,   264,
      10,   346,   334,     9,   103,   210,   104,    10,   196,    66,
      67,   113,   211,    98,    99,    98,    99,   117,   197,   344,
      24,   196,   120,   327,   292,   149,   345,    68,    69,    70,
      71,   197,    66,    67,   114,    77,   314,   124,   148,    77,
      98,    99,    72,   126,    73,    74,    75,    68,    69,    70,
      71,    -4,   165,   166,     8,   206,   207,   146,     9,   139,
     273,   274,    10,   147,    73,    74,    11,    12,   140,   150,
     154,   159,   164,   162,    77,    67,  -182,   168,   169,   170,
     171,   180,   174,    99,   202,   181,   182,   185,   187,   193,
     205,   204,   278,   237,   241,   219,   221,   279,   224,   246,
     282,   229,   245,   253,   258,   288,   263,   296,   259,   260,
     261,   291,   276,   254,   295,   283,   285,   301,     5,   195,
     249,   305,   312,   310,   318,   311,   307,   309,   313,   319,
     262,   335,   201,   343,   337,   340,   349,   293,   350,   294,
     236,    36,   172,   290,   289,   304,   341,   248,   223,   306,
       0,     0,   308,   228,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,   125
  };

  const short int
  parser::yycheck_[] =
  {
      24,   106,   232,    53,   169,   167,   232,    89,   232,    10,
      11,    12,   232,    85,     4,     3,   312,   232,     3,    14,
       3,    35,   318,   319,    31,    39,    50,    51,    29,    24,
       3,    19,    20,    21,    35,     3,    60,     3,    39,    63,
      90,    24,    15,    44,     3,     3,    36,    15,    36,    37,
       3,   156,    40,     3,    20,    21,    22,   139,   140,    47,
      45,     6,    45,   113,   136,    66,    67,    20,    21,    22,
      36,    44,   237,     0,    98,    99,    44,    78,   102,    45,
     104,    32,    83,   133,    37,    44,    44,     0,   138,     3,
     320,    41,    45,    44,   320,     3,   320,    17,     3,     4,
     320,    46,   332,   333,   154,   320,   332,   333,   332,   333,
     160,   216,   332,   333,     3,   174,     4,   332,   333,    24,
      29,    32,    36,     3,    44,   175,   150,    38,    36,    36,
      39,    20,    21,    22,    41,     0,   137,   161,   162,   301,
     164,    21,   166,    12,    13,     3,   251,     3,   207,    37,
     200,   256,   314,   315,     3,     4,    45,    66,    67,    12,
      13,   185,    18,   187,   324,   327,     3,     3,    37,    38,
      19,    20,    21,    22,    30,    24,     3,     4,    14,    32,
      35,   341,    18,    15,    33,    34,    39,    36,    24,     3,
      36,    40,    19,    20,    21,    31,   246,    24,    47,    12,
      13,    44,    12,    13,    18,     3,    33,    34,    29,    36,
      12,    13,   317,    40,     3,    40,    30,   241,     3,    44,
      47,    19,    20,    21,    35,    38,    24,     3,    38,    14,
      19,    20,    21,    18,    36,   259,     3,   261,    36,    24,
       9,    10,    40,    19,    20,    21,    14,    36,    37,    47,
       3,    40,    19,    20,    21,   279,    24,     3,    47,   301,
      36,     7,    14,    31,    40,    11,    19,    20,    21,    36,
      32,    47,    24,    40,   316,    37,    35,    29,     3,     8,
      47,   305,     7,    36,    30,     3,    11,    40,     3,     7,
      15,    16,     7,    11,    47,     3,    11,    36,   322,     7,
      15,    16,     3,    11,    36,    30,     7,    15,    16,     3,
      11,   335,    30,     7,    36,    30,    32,    11,    14,    12,
      13,    35,    30,    12,    13,    12,    13,     4,    24,    30,
      35,    14,     3,    29,    39,    41,    30,    25,    26,    27,
      28,    24,    12,    13,    37,    32,    29,     3,    37,    32,
      12,    13,    40,     3,    42,    43,    44,    25,    26,    27,
      28,     0,    37,    38,     3,    37,    38,     3,     7,    29,
      37,    38,    11,     3,    42,    43,    15,    16,    29,    38,
      24,     3,    39,    38,    32,    13,    35,    41,    35,     4,
      17,    36,    38,    13,     4,    38,    38,    38,    38,    37,
       3,    38,     3,    35,    35,    40,    40,    23,    41,    38,
       3,    37,    37,    37,    37,     3,    30,     4,    39,    38,
      38,    30,    39,     3,    35,    38,    38,    35,     1,   166,
      36,    38,    29,    35,    29,    35,    41,    41,    37,    29,
     230,    39,   168,    37,    30,    30,    30,   267,    37,   267,
     201,    12,   131,   261,   260,   281,   327,   218,   185,   283,
      -1,    -1,   285,   187,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    78
  };

  const unsigned char
  parser::yystos_[] =
  {
       0,    31,    49,    50,    51,    50,     0,     0,     3,     7,
      11,    15,    16,    53,    61,    62,    65,    71,    72,    79,
      80,    84,    86,     0,    35,    39,     3,    54,     3,    36,
      68,   115,    73,    74,   115,    44,    75,   115,     9,    10,
      66,    67,    35,     6,    46,    87,    88,    19,    20,    21,
      36,    40,    47,   103,   115,     4,    22,    24,    33,    34,
      36,   103,   114,    36,    55,    68,    12,    13,    25,    26,
      27,    28,    40,    42,    43,    44,    70,    32,    38,    52,
      96,    17,    15,    44,    75,    15,    68,    35,    35,    29,
     115,     8,    36,    36,   103,   103,   111,   112,    12,    13,
      39,    52,    40,    36,    32,   103,   113,    38,     3,    37,
      56,    57,   103,    35,    37,    68,    68,     4,   116,   117,
       3,     3,    36,    69,     3,    74,     3,     3,    20,    21,
      22,    36,    45,    76,    77,    78,    15,    44,    76,    29,
      29,    51,    52,     3,    21,    85,     3,     3,    37,    41,
      38,   107,   103,   103,    24,    24,   101,   102,   103,     3,
     103,    38,    38,   107,    39,    37,    38,    52,    41,    35,
       4,    17,    77,    52,    38,    76,    52,    51,    51,    30,
      36,    38,    38,   103,    52,    38,   107,    38,    81,    52,
      37,   103,   103,    37,   103,    57,    14,    24,    29,    58,
     118,    70,     4,   117,    38,     3,    37,    38,    78,    52,
      30,    30,     3,    24,    45,    89,    90,    91,    94,    40,
     104,    40,   108,   102,    41,     3,    82,    83,   112,    37,
      31,    59,    60,   118,    52,     4,    69,    35,     4,    37,
      37,    35,    92,     3,    45,    37,    38,   107,    92,    36,
      41,   105,   106,    37,     3,    41,   109,   110,    37,    39,
      38,    38,    59,    30,     3,    53,    63,    64,    65,    71,
      79,    84,   117,    37,    38,   103,    39,    93,     3,    23,
      95,    52,     3,    38,   107,    38,   107,   103,     3,    83,
      82,    30,    39,    66,    67,    35,     4,     3,     4,    24,
     103,    35,    97,    98,    91,    38,   106,    41,   110,    41,
      35,    35,    29,    37,    29,    96,   118,   103,    29,    29,
      60,     3,    18,    31,    99,   100,   118,    29,   118,    96,
      38,   107,    60,    60,    30,    39,   103,    30,    30,   100,
      30,    99,   118,    37,    30,    30,   103,    36,    30,    30,
      37
  };

  const unsigned char
  parser::yyr1_[] =
  {
       0,    48,    49,    49,    50,    51,    51,    51,    51,    51,
      51,    51,    51,    52,    52,    53,    54,    55,    55,    55,
      56,    56,    57,    57,    58,    58,    58,    59,    59,    60,
      60,    60,    60,    60,    60,    61,    61,    62,    62,    63,
      63,    64,    64,    65,    66,    67,    68,    68,    68,    68,
      68,    68,    68,    69,    69,    69,    70,    70,    70,    70,
      70,    70,    71,    71,    71,    71,    71,    71,    71,    71,
      72,    72,    72,    72,    73,    73,    74,    74,    75,    75,
      76,    76,    76,    77,    77,    78,    78,    78,    78,    78,
      78,    79,    80,    81,    81,    81,    81,    82,    82,    83,
      84,    85,    85,    86,    86,    87,    88,    88,    89,    89,
      90,    90,    91,    91,    91,    91,    92,    92,    93,    93,
      93,    93,    94,    94,    95,    95,    96,    97,    97,    97,
      98,    98,    98,    98,    98,    98,    98,    99,    99,   100,
     100,   100,   101,   101,   102,   102,   103,   103,   103,   103,
     103,   103,   103,   103,   103,   103,   104,   104,   105,   105,
     106,   107,   107,   108,   108,   109,   109,   110,   111,   111,
     112,   112,   113,   113,   114,   114,   114,   115,   115,   116,
     116,   116,   117,   117,   118,   118
  };

  const unsigned char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     6,     1,     3,     2,     0,
       3,     1,     1,     3,     2,     3,     4,     1,     1,     2,
       2,     2,     2,     2,     0,     6,     1,     5,     6,     6,
       1,     5,     6,     2,     2,     1,     3,     3,     6,     6,
       3,     3,     3,     4,     5,     7,     1,     1,     1,     1,
       1,     1,     3,     3,     3,     3,     3,     6,     4,     6,
       3,     5,     5,     6,     3,     1,     1,     3,     1,     2,
       1,     3,     4,     3,     1,     1,     1,     1,     1,     1,
       3,     3,     7,     0,     2,     2,     4,     3,     1,     3,
       9,     1,     1,     2,     0,     3,     1,     0,     2,     0,
       4,     1,     3,     1,     2,     1,     2,     0,     2,     2,
       2,     0,     2,     3,     2,     0,     2,     5,     4,     1,
       2,     3,     3,     5,     4,     4,     0,     2,     1,     3,
       2,     4,     3,     1,     1,     1,     1,     5,     3,     6,
       6,     3,     3,     3,     1,     1,     4,     2,     3,     1,
       6,     1,     0,     4,     2,     3,     1,     1,     2,     0,
       3,     1,     3,     3,     4,     4,     2,     1,     3,     1,
       3,     5,     1,     0,     1,     1
  };



  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a yyntokens_, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "$undefined", "NAME", "NUMBER", "LEXERROR",
  "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF", "OR", "AND", "PASS",
  "IMPORT", "FROM", "AS", "RAISE", "NOTHING", "NAMEDTUPLE",
  "COLL_NAMEDTUPLE", "TYPEVAR", "ARROW", "ELLIPSIS", "EQ", "NE", "LE",
  "GE", "INDENT", "DEDENT", "TRIPLEQUOTED", "TYPECOMMENT", "BYTESTRING",
  "UNICODESTRING", "':'", "'('", "')'", "','", "'='", "'['", "']'", "'<'",
  "'>'", "'.'", "'*'", "'@'", "'?'", "$accept", "start", "unit", "alldefs",
  "maybe_type_ignore", "classdef", "class_name", "parents", "parent_list",
  "parent", "maybe_class_funcs", "class_funcs", "funcdefs", "if_stmt",
  "if_and_elifs", "class_if_stmt", "class_if_and_elifs", "if_cond",
  "elif_cond", "else_cond", "condition", "version_tuple", "condition_op",
  "constantdef", "importdef", "import_items", "import_item", "import_name",
  "from_list", "from_items", "from_item", "alias_or_constant",
  "typevardef", "typevar_args", "typevar_kwargs", "typevar_kwarg",
  "funcdef", "funcname", "decorators", "decorator", "maybe_async",
  "params", "param_list", "param", "param_type", "param_default",
  "param_star_name", "return", "typeignore", "maybe_body", "empty_body",
  "body", "body_stmt", "type_parameters", "type_parameter", "type",
  "named_tuple_fields", "named_tuple_field_list", "named_tuple_field",
  "maybe_comma", "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "maybe_type_list", "type_list",
  "type_tuple_elements", "type_tuple_literal", "dotted_name",
  "getitem_key", "maybe_number", "pass_or_ellipsis", YY_NULLPTR
  };

#if PYTYPEDEBUG
  const unsigned short int
  parser::yyrline_[] =
  {
       0,   133,   133,   134,   138,   142,   143,   144,   145,   151,
     152,   153,   158,   162,   163,   169,   176,   187,   188,   189,
     193,   194,   198,   199,   203,   204,   205,   209,   210,   214,
     215,   220,   221,   226,   227,   232,   235,   240,   244,   263,
     266,   271,   275,   287,   291,   295,   299,   302,   305,   308,
     311,   312,   313,   318,   319,   320,   326,   327,   328,   329,
     330,   331,   335,   339,   343,   347,   351,   355,   359,   363,
     370,   374,   378,   384,   393,   394,   397,   398,   403,   404,
     411,   412,   413,   417,   418,   422,   423,   426,   429,   432,
     435,   439,   443,   450,   451,   452,   453,   457,   458,   462,
     466,   483,   484,   488,   489,   493,   497,   498,   502,   503,
     515,   516,   520,   521,   522,   523,   527,   528,   532,   533,
     534,   535,   539,   540,   544,   545,   549,   553,   554,   555,
     559,   560,   561,   562,   563,   564,   565,   569,   570,   574,
     575,   576,   580,   581,   585,   586,   590,   594,   598,   603,
     607,   611,   612,   613,   614,   615,   619,   620,   624,   625,
     629,   633,   634,   638,   639,   643,   646,   650,   653,   654,
     658,   659,   666,   667,   676,   681,   687,   694,   695,   709,
     710,   715,   723,   724,   728,   729
  };

  // Print the state stack on the debug stream.
  void
  parser::yystack_print_ ()
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << i->state;
    *yycdebug_ << std::endl;
  }

  // Report on the debug stream that the rule \a yyrule is going to be reduced.
  void
  parser::yy_reduce_print_ (int yyrule)
  {
    unsigned int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):" << std::endl;
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  // Symbol number corresponding to token number t.
  inline
  parser::token_number_type
  parser::yytranslate_ (int t)
  {
    static
    const token_number_type
    translate_table[] =
    {
     0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      36,    37,    45,     2,    38,     2,    44,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    35,     2,
      42,    39,    43,    47,    46,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    40,     2,    41,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34
    };
    const unsigned int user_token_number_max_ = 289;
    const token_number_type undef_token_ = 2;

    if (static_cast<int>(t) <= yyeof_)
      return yyeof_;
    else if (static_cast<unsigned int> (t) <= user_token_number_max_)
      return translate_table[t];
    else
      return undef_token_;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1167
} // pytype
#line 2968 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:1167
#line 732 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1168


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
