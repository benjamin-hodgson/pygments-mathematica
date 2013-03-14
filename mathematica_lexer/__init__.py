from pygments.lexer import RegexLexer, bygroups
from pygments.token import *
import re

class MathematicaLexer(RegexLexer):
    name = 'Mathematica'
    aliases = ['mathematica', 'Mathematica']
    filenames = ['*.m']
    flags = re.MULTILINE | re.DOTALL
    
    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'\(\*.*?\*\)', Comment.Multiline),  # comments (* look like this *)
            (r'".*?"', String),
            #(r'(\[)\s*([a-z][A-Za-z0-9]*_)\s*(\])', bygroups(Text, Name.Variable, Text)),
            (r'[A-Z][A-Za-z0-9]*', Name.Builtin),  # builtins start with a capital letter
            (r'[a-z][A-Za-z0-9]*', Name),  # user-defined names start with lowercase
            (r'[\{\}]', Literal),  # list braces
            (r'[\+\-]?[0-9]+\.?[0-9]*[eE]?[\+\-]?[0-9]*', Number.Float),
            (r'[\+\-/*=^(:=)<>@\?~]', Operator),
            (r'[\[\]]', Punctuation),  # function braces
            (r'[,;\.]', Punctuation),
            (r'_', Punctuation)
            ]
        }

if __name__ == '__main__':
    from pygments import highlight
    from pygments.formatters import LatexFormatter
    test_code = """
         normal code; (* comment *)
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
