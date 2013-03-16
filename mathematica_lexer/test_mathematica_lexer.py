import nose
from nose.tools import *
from .mathematica_lexer import MathematicaLexer
from pygments.token import *
import string


class BaseTest(object):
    def run(self, code, wanted):
        assert_equal(wanted + [(Whitespace, '\n')], list(self.lexer.get_tokens(code)))
    
    def setUp(self):
        self.lexer = MathematicaLexer()


class TestWhitespace(BaseTest):
    def test_whitespace(self):
        for tokentype, text in self.lexer.get_tokens(string.whitespace):
            assert_equal(tokentype, Whitespace)
            for c in text:
                assert c in string.whitespace, repr(c)


class TestNames(BaseTest):    
    def test_text(self):
        code = """some normal text"""
        wanted = [(Name, 'some'), (Whitespace, ' '),
                  (Name, 'normal'), (Whitespace, ' '),
                  (Name, 'text')]
        self.run(code, wanted)
    
    def test_builtins(self):
        code = "BuiltinFunction"
        wanted = [(Name.Builtin, 'BuiltinFunction')]
        self.run(code, wanted)


class TestComments(BaseTest):
    def test_comment(self):
        code = """normal code (* comment *)"""
        wanted = [(Name, 'normal'), (Whitespace, ' '),
                  (Name, 'code'), (Whitespace, ' '),
                  (Comment, '(*'),
                  (Comment, ' comment '),
                  (Comment, '*)')]
        self.run(code, wanted)
    
    def test_nested_comment(self):
        code = """(* nested (* comment *) test *)"""
        wanted = [(Comment, '(*'), (Comment, ' nested '),
                  (Comment, '(*'), (Comment, ' comment '), (Comment, '*)'),
                  (Comment, ' test '), (Comment, '*)')]
        self.run(code, wanted)
    
    def test_multiline_comment(self):
        code = """(* multiline
(* and nested *)
comment *)"""
        wanted = [(Comment, '(*'), (Comment, ' multiline\n'),
                  (Comment, '(*'), (Comment, ' and nested '), (Comment, '*)'),
                  (Comment, '\ncomment '), (Comment, '*)')]
        self.run(code, wanted)


class TestStrings(BaseTest):
    def test_string(self):
        code = '''normal code "string"'''
        wanted = [(Name, 'normal'), (Whitespace, ' '),
                  (Name, 'code'), (Whitespace, ' '),
                  (String, '"string"')]
        self.run(code, wanted)
    
    def test_multiline_string(self):
        code = '''"multiline
string"'''
        wanted = [(String, '"multiline\nstring"')]
        self.run(code, wanted)


class TestNumbers(BaseTest):
    def test_integers(self):
        code = "123 -56"
        wanted = [(Number.Integer, '123'), (Whitespace, ' '),
                  (Number.Integer, '-56')]
        self.run(code, wanted)
    
    def test_floats(self):
        code = "1. -2. 3.4 -5.6 7.8e9 -10.11E-12"
        wanted = [(Number.Float, '1.'), (Whitespace, ' '),
                  (Number.Float, '-2.'), (Whitespace, ' '),
                  (Number.Float, '3.4'), (Whitespace, ' '),
                  (Number.Float, '-5.6'), (Whitespace, ' '),
                  (Number.Float, '7.8e9'), (Whitespace, ' '),
                  (Number.Float, '-10.11E-12')]
        self.run(code, wanted)


class TestSymbols(BaseTest):
    def test_braces(self):
        code = "{}[]()"
        wanted = [(Punctuation, c) for c in code]
        self.run(code, wanted)
    
    def test_punctuation(self):
        code = ',;_'
        wanted = [(Punctuation, c) for c in code]
        self.run(code, wanted)
    
    def test_operators(self):
        code = '+-*^/:=<>@~?'
        wanted = [(Operator, c) for c in code]
        self.run(code, wanted)


class TestLHS(BaseTest):
    def test_assignment(self):
        code = "leftHandSide = x*3"
        wanted = [(Name.Function, 'leftHandSide'), (Whitespace, ' '),
                  (Operator, '='), (Whitespace, ' '),
                  (Name, 'x'), (Operator,'*'), (Number.Integer, '3')]
        self.run(code, wanted)
    
    def test_one_argument(self):
        code = 'oneArgument[x_] := x^2'
        wanted = [(Name.Function, 'oneArgument'), (Punctuation, '['),
                  (Name.Variable, 'x'), (Punctuation, '_'), (Punctuation, ']'),
                  (Whitespace, ' '), (Operator, ':='), (Whitespace, ' '),
                  (Name.Variable, 'x'), (Operator, '^'), (Number.Integer, '2')]
        self.run(code, wanted)
    
    def test_multiple_arguments(self):
        code = 'multipleArguments[x_, y_, z_] := x + y*z/2.0'
        wanted = [(Name.Function, 'multipleArguments'), (Punctuation, '['),
                  (Name.Variable, 'x'),(Punctuation, '_'), (Whitespace, ' '),
                  (Name.Variable, 'y'),(Punctuation, '_'), (Whitespace, ' '),
                  (Name.Variable, 'z'),(Punctuation, '_'), (Punctuation, ']'),
                  (Whitespace, ' '), (Operator, ':='), (Whitespace, ' ')
                  (Name.Variable, 'x'), (Whitespace, ' '),
                  (Operator, '+'), (Whitespace, ' '),
                  (Name.Variable, 'y'), (Operator, '*'),
                  (Name.Variable, 'z'), (Operator, '/'), (Number.Float, '2.0')]
        self.run(code, wanted)


if __name__ == '__main__':
    nose.main()
