import nose
from nose.tools import *
from . import MathematicaLexer
from pygments.token import *
import string


class BaseMathematicaLexerTest(object):
    def run(self, code, wanted):
        assert_equal(wanted, list(self.lexer.get_tokens(code)))
    
    def setUp(self):
        self.lexer = MathematicaLexer()


class TestText(BaseMathematicaLexerTest):
    def test_whitespace(self):
        for tokentype, text in self.lexer.get_tokens(string.whitespace):
            assert_equal(tokentype, Whitespace)
            for c in text:
                assert c in string.whitespace, repr(c)
    
    def test_text(self):
        code = """some normal text"""
        wanted = [(Text, 'some'), (Whitespace, ' '),
                  (Text, 'normal'), (Whitespace, ' '),
                  (Text, 'text'), (Whitespace, '\n')]
        self.run(code, wanted)
    
    def test_builtins(self):
        code = "BuiltinFunction"
        wanted = [(Name.Builtin, 'BuiltinFunction'), (Whitespace, '\n')]
        self.run(code, wanted)


class TestComments(BaseMathematicaLexerTest):
    def test_comment(self):
        code = """normal code (* comment *)"""
        wanted = [(Text, 'normal'), (Whitespace, ' '),
                  (Text, 'code'), (Whitespace, ' '),
                  (Comment, '(*'),
                  (Comment, ' comment '),
                  (Comment, '*)'), (Whitespace, '\n')]
        self.run(code, wanted)
    
    def test_nested_comment(self):
        code = """(* nested (* comment *) test *)"""
        wanted = [(Comment, '(*'), (Comment, ' nested '),
                  (Comment, '(*'), (Comment, ' comment '), (Comment, '*)'),
                  (Comment, ' test '), (Comment, '*)'), (Whitespace, '\n')]
        self.run(code, wanted)
    
    def test_multiline_comment(self):
        code = """(* multiline
(* and nested *)
comment *)"""
        wanted = [(Comment, '(*'), (Comment, ' multiline\n'),
                  (Comment, '(*'), (Comment, ' and nested '), (Comment, '*)'),
                  (Comment, '\ncomment '), (Comment, '*)'), (Whitespace, '\n')]
        self.run(code, wanted)


class TestStrings(BaseMathematicaLexerTest):
    def test_string(self):
        code = '''normal code "string"'''
        wanted = [(Text, 'normal'), (Whitespace, ' '),
                  (Text, 'code'), (Whitespace, ' '),
                  (String, '"string"'), (Whitespace, '\n')]
        self.run(code, wanted)
    
    def test_multiline_string(self):
        code = '''"multiline
string"'''
        wanted = [(String, '"multiline\nstring"'), (Whitespace, '\n')]
        self.run(code, wanted)


class TestNumbers(BaseMathematicaLexerTest):
    def test_integers(self):
        code = "123 -56"
        wanted = [(Number.Integer, '123'), (Whitespace, ' '),
                  (Number.Integer, '-56'), (Whitespace, '\n')]
        self.run(code, wanted)
    
    def test_floats(self):
        code = "1. -2. 3.4 -5.6 7.8e9 -10.11E-12"
        wanted = [(Number.Float, '1.'), (Whitespace, ' '),
                  (Number.Float, '-2.'), (Whitespace, ' '),
                  (Number.Float, '3.4'), (Whitespace, ' '),
                  (Number.Float, '-5.6'), (Whitespace, ' '),
                  (Number.Float, '7.8e9'), (Whitespace, ' '),
                  (Number.Float, '-10.11E-12'), (Whitespace, '\n')]
        self.run(code, wanted)


class TestSymbols(BaseMathematicaLexerTest):
    def test_braces(self):
        code = "{}[]()"
        wanted = [(Punctuation, c) for c in code] + [(Whitespace, '\n')]
        self.run(code, wanted)
    
    def test_punctuation(self):
        code = ',;'
        wanted = [(Punctuation, c) for c in code] + [(Whitespace, '\n')]
        self.run(code, wanted)
    
    def test_operators(self):
        code = '+-*^/:=<>@~?'
        wanted = [(Operator, c) for c in code] + [(Whitespace, '\n')]
        self.run(code, wanted)


if __name__ == '__main__':
    nose.main()
