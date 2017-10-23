#!/usr/bin/env python
#
# Basic lexical analyzer for C99. Usage:
#
# >>> lexer = C99Lexer()
# >>> lexer.tokenize("static unsigned int foo = bar++;")
# [('STATIC', 'static'), ('UNSIGNED', 'unsigned'), ('INT', 'int'),
#  ('IDENTIFIER', 'foo'), ('ASSIGN', '='), ('IDENTIFIER', 'bar'),
#  ('INC', '++'), ('SEMICOLON', ';')]
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
        ("\<\<\=",          "BITWISE_LSHIFT_ASSIGN"),
        ("\>\>\=",          "BITWISE_RSHIFT_ASSIGN"),
        # 2-character operators
        ("\=\=",            "EQUALS"),
        ("\!\=",            "NOT_EQUALS"),
        ("\+\=",            "ADD_ASSIGN"),
        ("\-\=",            "SUB_ASSIGN"),
        ("\*\=",            "MUL_ASSIGN"),
        ("\/\=",            "DIV_ASSIGN"),
        ("\%\=",            "MOD_ASSIGN"),
        ("\&\=",            "AND_ASSIGN"),
        ("\|\=",            "OR_ASSIGN"),
        ("\^\=",            "BITWISE_XOR_ASSIGN"),
        ("\>\=",            "GT_EQUAL"),
        ("\<\=",            "LT_EQUAL"),
        ("\-\>",            "STRUCT_DEREF"),
        ("\<\<",            "BITWISE_LSHIFT"),
        ("\>\>",            "BITWISE_RSHIFT"),
        ("\&\&",            "LOGICAL_AND"),
        ("\|\|",            "LOGICAL_OR"),
        ("\+\+",            "INC"),
        ("\-\-",            "DEC"),
        # single-character operators and symbols
        ("\{",              "LCB"),
        ("\}",              "RCB"),
        ("\(",              "LP"),
        ("\)",              "RP"),
        ("\[",              "LB"),
        ("\]",              "RB"),
        ("\&",              "AMPERSAND"),
        ("\|",              "BITWISE_OR"),
        ("\!",              "LOGICAL_NOT"),
        ("\~",              "BITWISE_NOT"),
        ("\^",              "BITWISE_XOR"),
        ("\.",              "STRUCT_REF"),
        ("\?",              "TERNARY"),
        ("\:",              "COLON"),
        ("\;",              "SEMICOLON"),
        ("\,",              "COMMA"),
        ("\=",              "ASSIGN"),
        ("\>",              "GT"),
        ("\<",              "LT"),
        ("\+",              "PLUS"),
        ("\-",              "MINUS"),
        ("\*",              "STAR"),
        ("\/",              "DIV"),
        ("\%",              "MOD"),
        # C99 keywords
        ("auto",            "AUTO"),
        ("break",           "BREAK"),
        ("case",            "CASE"),
        ("char",            "CHAR"),
        ("const",           "CONST"),
        ("continue",        "CONTINUE"),
        ("default",         "DEFAULT"),
        ("do",              "DO"),
        ("double",          "DOUBLE"),
        ("else",            "ELSE"),
        ("enum",            "ENUM"),
        ("extern",          "EXTERN"),
        ("float",           "FLOAT"),
        ("for",             "FOR"),
        ("goto",            "GOTO"),
        ("if",              "IF"),
        ("inline",          "INLINE"),
        ("int",             "INT"),
        ("long",            "LONG"),
        ("register",        "REGISTER"),
        ("restrict",        "RESTRICT"),
        ("return",          "RETURN"),
        ("short",           "SHORT"),
        ("signed",          "SIGNED"),
        ("sizeof",          "SIZEOF"),
        ("static",          "STATIC"),
        ("struct",          "STRUCT"),
        ("switch",          "SWITCH"),
        ("typedef",         "TYPEDEF"),
        ("union",           "UNION"),
        ("unsigned",        "UNSIGNED"),
        ("void",            "VOID"),
        ("volatile",        "VOLATILE"),
        ("while",           "WHILE"),
        ("_Bool",           "BOOL"),
        ("_Complex",        "COMPLEX"),
        ("_Imaginary",      "IMAGINARY"),
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

