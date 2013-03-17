from pygments.lexer import RegexLexer, bygroups, include, using, this
from pygments.token import *
import re

class MathematicaLexer(RegexLexer):
    name = 'Mathematica'
    aliases = ['mathematica', 'Mathematica']
    filenames = ['*.m']
    
    tokens = {
        'root': [
            (r'\(\*', Comment, 'comment'),  # comments (* look like this *)
            (r'\s+', Whitespace),
            (r'(?s)".*?"', String),
            (r'\\\[\w*?\]', Error),
            include('numbers'),
            include('symbols'),
            include('names')
        ],
        'numbers': [
            (r'[\+\-]?[0-9]+\.[0-9]*[eE]?[\+\-]?[0-9]*', Number.Float),
            (r'[\+\-]?[0-9]+', Number.Integer)
        ],
        'symbols': [
            (r'[\+\-/*=^:<>@\?~]', Operator),
            (r'[\[\]\(\){}]', Punctuation),  # various braces
            (r'[\.,;_&]', Punctuation)
        ],
        'comment': [
            (r'[^\*\(\)]+', Comment),
            (r'\(\*', Comment, '#push'),
            (r'\*\)', Comment, '#pop'),
            (r'[\(\)\*]', Comment)  # star or brackets on their own
        ],
        'names': [
            (r'[A-Z][A-Za-z0-9]*', Name.Builtin),  # builtins start with a capital letter
            (r'^([A-Za-z0-9]+])(\s*)(:?=)(\s*)(.*?)$',
             bygroups(Name.Function, Whitespace, Operator, Whitespace, using(this))),
            (r'^([a-z][A-Za-z0-9]*)(\[?.*?\]?)(\s*)(:?=)(\s*)(.*?)$',
             bygroups(Name.Function, using(this),
                      Whitespace, Operator, Whitespace, using(this))),
            (r'[a-z][A-Za-z0-9]*', Name),  # user-defined names start with lowercase
            (r'#[0-9]*', Name.Variable)
        ]
    }


if __name__ == '__main__':
    from pygments import highlight
    from pygments.formatters import LatexFormatter
    test_code = """
normal code; (* a comment *)
(* comment (* (nested) *) *)
BuiltInFunctionCall[argument, {list,argument,-10.01e+12}];
assignment = {var, 2, "string"};

(* multiline comment
ContainingAKeyword,
assignment = {1,3,"hello"},
aFunctionDefiniton[a_,b_] := a+b *)
"""
    print(highlight(test_code, MathematicaLexer(), LatexFormatter()))
