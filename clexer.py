#!/usr/bin/env python
#
# Basic lexical analyzer for C99. Usage:
#
# >>> lexer = C99Lexer()
# >>> lexer.tokenize("static unsigned int foo = bar++;")
#
# Dimitris Karagkasidis <t.pagef.lt@gmail.com>
# https://github.com/pageflt/clexer

import re
import sys

class C99Lexer():
    _c99_desc = [
        # Comments
        ("\/\*.*?\*\/",     "COMMENT"),
        ("\/\/.*$",         "CPP_COMMENT"),
        ("\/\*.*?$",        "MULTILINE_COMMENT_START"),
        ("^.*?\*\/",        "MULTILINE_COMMENT_END"),
        # 3-character operators
        ("\<\<\=",          "OP_BITWISE_LSHIFT_ASSIGN"),
        ("\>\>\=",          "OP_BITWISE_RSHIFT_ASSIGN"),
        # 2-character operators
        ("\=\=",            "OP_EQUALS"),
        ("\!\=",            "OP_NOT_EQUALS"),
        ("\+\=",            "OP_ADD_ASSIGN"),
        ("\-\=",            "OP_SUB_ASSIGN"),
        ("\*\=",            "OP_MUL_ASSIGN"),
        ("\/\=",            "OP_DIV_ASSIGN"),
        ("\%\=",            "OP_MOD_ASSIGN"),
        ("\&\=",            "OP_AND_ASSIGN"),
        ("\|\=",            "OP_OR_ASSIGN"),
        ("\^\=",            "OP_BITWISE_XOR_ASSIGN"),
        ("\>\=",            "OP_GT_EQUAL"),
        ("\<\=",            "OP_LT_EQUAL"),
        ("\-\>",            "OP_STRUCT_DEREF"),
        ("\<\<",            "OP_BITWISE_LSHIFT"),
        ("\>\>",            "OP_BITWISE_RSHIFT"),
        ("\&\&",            "OP_LOGICAL_AND"),
        ("\|\|",            "OP_LOGICAL_OR"),
        ("\+\+",            "OP_INC"),
        ("\-\-",            "OP_DEC"),
        # single-character operators and symbols
        ("\{",              "SYM_LCB"),
        ("\}",              "SYM_RCB"),
        ("\(",              "SYM_LP"),
        ("\)",              "SYM_RP"),
        ("\[",              "SYM_LB"),
        ("\]",              "SYM_RB"),
        ("\&",              "SYM_AMPERSAND"),
        ("\|",              "OP_BITWISE_OR"),
        ("\!",              "OP_LOGICAL_NOT"),
        ("\~",              "OP_BITWISE_NOT"),
        ("\^",              "OP_BITWISE_XOR"),
        ("\.",              "OP_STRUCT_REF"),
        ("\?",              "OP_TERNARY"),
        ("\:",              "SYM_COLON"),
        ("\;",              "SYM_SEMICOLON"),
        ("\,",              "SYM_COMMA"),
        ("\=",              "OP_ASSIGN"),
        ("\>",              "OP_GT"),
        ("\<",              "OP_LT"),
        ("\+",              "SYM_PLUS"),
        ("\-",              "SYM_MINUS"),
        ("\*",              "SYM_STAR"),
        ("\/",              "OP_DIV"),
        ("\%",              "OP_MOD"),
        # C99 keywords
        ("auto",            "KW_AUTO"),
        ("break",           "KW_BREAK"),
        ("case",            "KW_CASE"),
        ("char",            "KW_CHAR"),
        ("const",           "KW_CONST"),
        ("continue",        "KW_CONTINUE"),
        ("default",         "KW_DEFAULT"),
        ("do",              "KW_DO"),
        ("double",          "KW_DOUBLE"),
        ("else",            "KW_ELSE"),
        ("enum",            "KW_ENUM"),
        ("extern",          "KW_EXTERN"),
        ("float",           "KW_FLOAT"),
        ("for",             "KW_FOR"),
        ("goto",            "KW_GOTO"),
        ("if",              "KW_IF"),
        ("inline",          "KW_INLINE"),
        ("int",             "KW_INT"),
        ("long",            "KW_LONG"),
        ("register",        "KW_REGISTER"),
        ("restrict",        "KW_RESTRICT"),
        ("return",          "KW_RETURN"),
        ("short",           "KW_SHORT"),
        ("signed",          "KW_SIGNED"),
        ("sizeof",          "KW_SIZEOF"),
        ("static",          "KW_STATIC"),
        ("struct",          "KW_STRUCT"),
        ("switch",          "KW_SWITCH"),
        ("typedef",         "KW_TYPEDEF"),
        ("union",           "KW_UNION"),
        ("unsigned",        "KW_UNSIGNED"),
        ("void",            "KW_VOID"),
        ("volatile",        "KW_VOLATILE"),
        ("while",           "KW_WHILE"),
        ("_Bool",           "KW_BOOL"),
        ("_Complex",        "KW_COMPLEX"),
        ("_Imaginary",      "KW_IMAGINARY"),
        # Labels
        ("[a-zA-Z_]+\w*?\:","LABEL"),
        # Macros
        ("#define\s.*?$",   "M_DEFINE"),
        ("#undef\s.*?$",    "M_UNDEF"),
        ("#include\s.*?$",  "M_INCLUDE"),
        ("#ifdef\s.*?$",    "M_IFDEF"),
        ("#ifndef\s.*?$",   "M_IFNDEF"),
        ("#endif\s.*?$",    "M_ENDIF"),
        ("#if\s.*?$",       "M_IF"),
        ("#elif\s.*?$",     "M_ELIF"),
        # Constants
        ("\d+",             "NUMERIC_CONSTANT"),
        ("[\'\"].*?[\'\"]", "STRING_CONSTANT"),
        # Identifiers
        ("[a-zA-Z0-9_]+",   "IDENTIFIER"),
        # Whitespace characters (space, tab, newline)
        ("\s+",             "WHITESPACE"),
    ]

    def __init__(self, keep_whitespaces=False):
        self._keep_ws = keep_whitespaces

        re_list = []
        for e in self._c99_desc:
            re_list.append("(?P<%s>%s)" % (e[1], e[0]))
        self.re_tokenizer = re.compile("|".join(re_list))


    def tokenize(self, line):
        position = 0
        tokens = []
        while (position <= len(line)):
            r = self.re_tokenizer.match(line, position)
            if r:
                if r.lastgroup == "WHITESPACE" and not self._keep_ws:
                    pass
                else:
                    tokens.append((r.lastgroup, r.group(r.lastgroup)))
                position = r.end()
            else:
                break

        return tokens

