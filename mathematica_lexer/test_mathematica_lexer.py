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
    
    def test_escape(self):
        code = "\\[Mu]"
        wanted = [(Error, "\\[Mu]")]
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
        code = ',;_?'
        wanted = [(Punctuation, c) for c in code]
        self.run(code, wanted)
    
    def test_operators(self):
        code = '+-*^/:=<>@~.'
        wanted = [(Operator, c) for c in code]
        self.run(code, wanted)
    
    def test_anonymous_function(self):
        code1 = '#*2 &'
        wanted1 = [(Name.Variable, '#'), (Operator, '*'), (Number.Integer, '2'),
                   (Whitespace, ' '), (Punctuation, '&')]
        self.run(code1, wanted1)
        
        code2 = '#1*2 + #2 &'
        wanted2 = [(Name.Variable, '#1'), (Operator, '*'), (Number.Integer, '2'),
                   (Whitespace, ' '), (Operator, '+'), (Whitespace, ' '),
                   (Name.Variable, '#2'), (Whitespace, ' '), (Punctuation, '&')]
        self.run(code2, wanted2)


class TestLHS(BaseTest):
    def test_assignment(self):
        code = "leftHandSide = x*3;"
        wanted = [(Name.Function, 'leftHandSide'), (Whitespace, ' '),
                  (Operator, '='), (Whitespace, ' '),
                  (Name, 'x'), (Operator,'*'), (Number.Integer, '3'),
                  (Punctuation, ';')]
        self.run(code, wanted)
    
    def test_one_argument(self):
        code = 'oneArgument[x_] := x^2;'
        wanted = [(Name.Function, 'oneArgument'), (Punctuation, '['),
                  (Name, 'x'), (Punctuation, '_'), (Punctuation, ']'),
                  (Whitespace, ' '), (Operator, ':='), (Whitespace, ' '),
                  (Name, 'x'), (Operator, '^'), (Number.Integer, '2'),
                  (Punctuation, ';')]
        self.run(code, wanted)
    
        def test_definition_after_code(self):
            code = """normal code;
leftHandSide[a_, b_] := a + b;"""
            wanted = [(Name, 'normal'), (Whitespace, ' '),
                      (Name, 'code'), (Punctuation, ';'), (Whitespace, '\n'),
                      (Name.Function, 'leftHandSide'), (Punctuation, '['),
                      (Name, 'a'), (Punctuation, '_'), (Punctuation, ','),
                      (Name, 'b'), (Punctuation, '_'), (Punctuation, ']'),
                      (Whitespace, ' '), (Operator, ':='), (Whitespace, ' '),
                      (Name, 'a'), (Whitespace, ' '),
                      (Operator, '+'), (Whitespace, ' '),
                      (Name, 'b'), (Punctuation, ';')]
            self.run(code, wanted)
    
    def test_multiple_arguments(self):
        code = 'multipleArguments[x_List, y_?NumericQ, z_] := x + y*z/2.0;'
        wanted = [(Name.Function, 'multipleArguments'), (Punctuation, '['),
                  (Name, 'x'), (Punctuation, '_'), (Name.Builtin, 'List'),
                  (Punctuation, ','), (Whitespace, ' '),
                  (Name, 'y'), (Punctuation, '_'), (Punctuation, '?'),
                  (Name.Builtin, 'NumericQ'),
                  (Punctuation, ','), (Whitespace, ' '),
                  (Name, 'z'), (Punctuation, '_'), (Punctuation, ']'),
                  (Whitespace, ' '), (Operator, ':='), (Whitespace, ' '),
                  (Name, 'x'), (Whitespace, ' '),
                  (Operator, '+'), (Whitespace, ' '),
                  (Name, 'y'), (Operator, '*'),
                  (Name, 'z'), (Operator, '/'), (Number.Float, '2.0'),
                  (Punctuation, ';')]
        self.run(code, wanted)
    
    def test_multiline_function(self):
        code = """multilineFunction[x_] := BuiltinFunction[
  {x, x^2, y}];
endOfIndent"""
        wanted = [(Name.Function, 'multilineFunction'), (Punctuation, '['),
                  (Name, 'x'), (Punctuation, '_'), (Punctuation, ']'),
                  (Whitespace, ' '), (Operator, ':='), (Whitespace, ' '),
                  (Name.Builtin, 'BuiltinFunction'), (Punctuation, '['),
                  (Whitespace, '\n  '),
                  (Punctuation, '{'), (Name, 'x'), (Punctuation, ','),
                  (Whitespace, ' '), (Name, 'x'), (Operator, '^'),
                  (Number.Integer, '2'), (Punctuation, ','), (Whitespace, ' '),
                  (Name, 'y'), (Punctuation, '}'), (Punctuation, ']'), (Punctuation, ';'),
                  (Whitespace, '\n'), (Name, 'endOfIndent')]
        self.run(code, wanted)
    
    def test_patten_match(self):
        code1 = "{a} = {b}"
        wanted1 = [(Punctuation, '{'),(Name.Function, 'a'),(Punctuation, '}'),
                   (Whitespace, ' '), (Operator, '='), (Whitespace, ' '),
                   (Punctuation, '{'),(Name, 'b'),(Punctuation, '}')]
        self.run(code1, wanted1)
    
        code2 = "{{a,b},{c,d}} = f[{{w,x},{y,z}}];"
        wanted2 = [(Punctuation, '{'), (Punctuation, '{'),
                   (Name.Function, 'a'), (Punctuation, ','), (Name.Function, 'b'),
                   (Punctuation, '}'), (Punctuation, ','), (Punctuation, '{'),
                   (Name.Function, 'c'), (Punctuation, ','), (Name.Function, 'd'),
                   (Punctuation, '}'), (Punctuation, '}'),
                   (Whitespace, ' '), (Operator, '='), (Whitespace, ' '),
                   (Name, 'f'), (Punctuation, '['),
                   (Punctuation, '{'), (Punctuation, '{'),
                   (Name, 'w'), (Punctuation, ','), (Name, 'x'),
                   (Punctuation, '}'), (Punctuation, ','), (Punctuation, '{'),
                   (Name, 'y'), (Punctuation, ','), (Name, 'z'),
                   (Punctuation, '}'), (Punctuation, '}'),
                   (Punctuation, ']'), (Punctuation, ';')]
        self.run(code2, wanted2)


if __name__ == '__main__':
    nose.main()
