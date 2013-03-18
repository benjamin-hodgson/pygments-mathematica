from pygments.lexer import RegexLexer, bygroups, include, using, this
from pygments.token import *
import re

class MathematicaLexer(RegexLexer):
    name = 'Mathematica'
    aliases = ['mathematica', 'Mathematica']
    filenames = ['*.m']
    
    def definition(lexer, match):
        # r'^([A-Za-z0-9]+)(\[?.*?\]?)(\s*)(:?=)(\s*)(.*?)$'
        yield match.start(1), Name.Function, match.group(1)
        
        args = []
        
        if match.group(2):
            posn = match.start(2)
            yield posn, Punctuation, '['
            posn += 1
            
            args = [arg + ',' for arg in match.group(2)[1:-1].split(',')]
            args[-1] = args[-1][:-1]  # drop the trailing comma
            for arg in args:
                argmatch = re.match(r'(\s*)([a-z][A-Za-z0-9]*)(_\??)([A-Za-z0-9]*)(,?)', arg)
                for t, v in zip((Whitespace, Name.Variable, Punctuation, None, Punctuation),
                                argmatch.groups()):
                    if v:
                        if t is None:
                            t = Name.Builtin if v[0].isupper() else Name
                        yield posn, t, v
                        posn += len(t)
            
            yield match.end(2) - 1, Punctuation, ']'
            
            args = [arg.partition('_')[0].strip() for arg in args]
            # now args is plain arguments, eg ['x', 'y'] not ['x_,', ' y_List']
        
        if match.group(3):
            yield match.start(3), Whitespace, match.group(3)
        
        yield match.start(4), Operator, match.group(4)
        
        if match.group(5):
            yield match.start(5), Whitespace, match.group(5)
        
        posn = match.start(6)
        for i, t, v in lexer.get_tokens_unprocessed(match.group()[posn:]):
            if v in args:
                yield i + posn, Name.Variable, v
            else:
                yield i + posn, t, v
    
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
            (r'[\+\-/*=^:<>@~]', Operator),
            (r'[\[\]\(\){}]', Punctuation),  # various braces
            (r'[\.,;_&\?]', Punctuation)
        ],
        'comment': [
            (r'[^\*\(\)]+', Comment),
            (r'\(\*', Comment, '#push'),
            (r'\*\)', Comment, '#pop'),
            (r'[\(\)\*]', Comment)  # star or brackets on their own
        ],
        'names': [
            (r'[A-Z][A-Za-z0-9]*', Name.Builtin),  # builtins start with a capital letter
            (r'^([A-Za-z0-9]+)(\[?.*?\]?)(\s*)(:?=)(\s*)(.*?)$',
             definition),
             #bygroups(Name.Function, using(this), Whitespace, Operator, Whitespace,
             #         using(this))),
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
functionDefiniton[a_, b_List] := a+b

(* multiline comment
ContainingAKeyword,
assignment = {1,3,"hello"} *)
"""
    print(highlight(test_code, MathematicaLexer(), LatexFormatter()))
