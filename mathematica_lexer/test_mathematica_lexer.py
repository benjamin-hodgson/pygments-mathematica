import nose
from nose.tools import *
from . import MathematicaLexer
from pygments.token import *
import string


class TestMathematicaLexer(object):
    def setUp(self):
        self.lexer = MathematicaLexer()
    
    def test_whitespace(self):
        for tokentype, text in self.lexer.get_tokens(string.whitespace):
            assert_equal(tokentype, Whitespace)
            for c in text:
                assert c in string.whitespace, repr(c)
    
    def test_text(self):
        code = """some normal text"""
        wanted = interleave(zip([Text, Text, Text], code.split()), (Whitespace, ' '))
        for wanted_tup, actual_tup in zip(wanted, self.lexer.get_tokens(code)):
            assert_equal(wanted_tup, actual_tup)
    
    def test_comment(self):
        code = """normal code (* comment *)"""
        wanted = [(Text, 'normal'),
                  (Whitespace, ' '),
                  (Text, 'code'),
                  (Whitespace, ' '),
                  (Comment, '(*'),
                  (Comment, ' comment '),
                  (Comment, '*)')]
        for wanted_tup, actual_tup in zip(wanted, self.lexer.get_tokens(code)):
            assert_equal(wanted_tup, actual_tup)


def interleave(l, elem):
    ret = []
    for item in l:
        ret.append(item)
        ret.append(elem)
    return ret[:-1]


if __name__ == '__main__':
    nose.main()
