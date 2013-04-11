pygments-mathematica
====================

Mathematica lexer for Pygments.

Author: Benjamin Hodgson


A lexer plugin for Pygments, to highlight Mathematica code.

Currently, this can deal with:
  * (* comments (enclosed in (* *)) - nested works too *)
  * BuiltinFunctions (assumed to be names that start with capitals letters)
  * userDefinedNames
  * "strings
  (including multiline)"
  * numbers of all shapes and sizes
  * all kinds of Mathematica special symbols: #1 & {,}[]; etc
  * all kinds of assignment. The left-hand side is highlighted as a 'function',
  which is a little hacky but it works.
    * Assignment to objects inside lists {a,b} = {c,d}

Installation
============
Make sure you have Pygments installed, and run `python setup.py install`.
You should now be able to highlight Mathematica code using `pygmentize`.

Tested on Python 3.2 and 2.7 (so it'll probably work with any version of Python 3).


Note: this is the __development__ branch. You probably want [the v1.0 tag](https://github.com/poorsod/pygments-mathematica/tree/v1.0)
