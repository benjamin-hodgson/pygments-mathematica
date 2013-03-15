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


class TestComments(BaseMathematicaLexerTest):
    def test_comment(self):
        code = """normal code (* comment *)"""
        wanted = [(Text, 'normal'), (Whitespace, ' '),
                  (Text, 'code'), (Whitespace, ' '),
                  (Comment, '(*'),
                  (Comment, ' comment '),
                  (Comment, '*)'), (Whitespace, '\n')]
        self.run(code, wanted)




if __name__ == '__main__':
    nose.main()
