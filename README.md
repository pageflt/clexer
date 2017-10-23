# clexer

## What is this?
Basic lexical analyser for C99 code.

## How do I use it?

```python
#!/usr/bin/python
from clexer import C99Lexer

lexer = C99Lexer()
print lexer.tokenize("static unsigned int foo = bar++;")
```

You should get your tokens in a list of the following format:

```
[('KW_STATIC', 'static'), ('KW_UNSIGNED', 'unsigned'), ('KW_INT', 'int'), ('IDENTIFIER', 'foo'), ('OP_ASSIGN', '='), ('IDENTIFIER', 'bar'), ('OP_INC', '++'), ('SYM_SEMICOLON', ';')]
```
Language symbols are prefixed with `SYM_`, operators are prefixed with `OP_`, keywords are prefixed with `KW_`. Keep in mind that context-dependent tokens (`&`, `*`, `+`, `-`) are prefixed with `SYM_`.

If you want the whitespace characters preserved in your tokens list, set `keep_whitespaces` in the object constructor:

```python
lexer = C99Lexer(keep_whitespaces=True)
```
