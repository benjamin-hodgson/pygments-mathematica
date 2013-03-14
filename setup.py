"""
Mathematica Pygments Lexer
"""
from setuptools import setup
 
setup(
    name='Mathematica Pygments Lexer',
    version='0.1.0',
    description="Mathematica Lexer for Pygments",
    author='Benjamin Hodgson',
    packages=['mathematica_lexer'],
    entry_points='''[pygments.lexers]
mathematicalexer = mathematica_lexer:MathematicaLexer
'''
)
