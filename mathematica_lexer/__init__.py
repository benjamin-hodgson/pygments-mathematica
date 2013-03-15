from pygments.lexer import RegexLexer, bygroups
from pygments.token import *
import re

class MathematicaLexer(RegexLexer):
    name = 'Mathematica'
    aliases = ['mathematica', 'Mathematica']
    filenames = ['*.m']
    
    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'\(\*', Comment, 'comment'),  # comments (* look like this *)
            (r'".*?"', String),
            #(r'(\[)\s*([a-z][A-Za-z0-9]*_)\s*(\])', bygroups(Text, Name.Variable, Text)),
            (r'[A-Z][A-Za-z0-9]*', Name.Builtin),  # builtins start with a capital letter
            (r'[a-z][A-Za-z0-9]*', Name),  # user-defined names start with lowercase
            (r'[\+\-]?[0-9]+\.?[0-9]*[eE]?[\+\-]?[0-9]*', Number.Float),
            (r'[\+\-]?[0-9]+', Number.Integer),
            (r'[\+\-/*=^:<>@\?~]', Operator),
            (r'[\[\](){}]', Punctuation),  # various braces
            (r'[,;\.]', Punctuation),
            (r'_', Punctuation)
        ],
        'comment': [
            (r'[^\*\(\)]+', Comment),
            (r'\(\*', Comment, '#push'),
            (r'\*\)', Comment, '#pop'),
            (r'[\(\)\*]', Comment)  # star or brackets on their own
        ]
    }

if __name__ == '__main__':
    from pygments import highlight
    from pygments.formatters import LatexFormatter
    test_code = """
         normal code; (* a comment *)
         (* comment (* (nested) *) *)
         BuiltInFunctionCall[argument, {list,argument,-10.01e+12}];
         functionDefinition[x_]
         functionDefinition[a_,b_] := a^2 + b^2;
         assignment = {var, 2, "string"};
         
         (* multiline comment
         ContainingAKeyword,
         assignment = {1,3,"hello"},
         aFunctionDefiniton[a_,b_] := a+b *)
         """
    print(highlight(test_code, MathematicaLexer(), LatexFormatter()))
