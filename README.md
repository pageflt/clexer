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
[('STATIC', 'static'), ('UNSIGNED', 'unsigned'), ('INT', 'int'), ('IDENTIFIER', 'foo'), ('ASSIGN', '='), ('IDENTIFIER', 'bar'), ('INC', '++'), ('SEMICOLON', ';')]
```

If you want the whitespace characters preserved in your tokens list, set `keep_whitespaces` in the object constructor:

```python
lexer = C99Lexer(keep_whitespaces=True)
```
