# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.formatExpr import CondParserGenerator
from bibmanagement.formatExpr import ParserGenerator

class Parser:
    def __init__(self):
        self._firstLex, self._firstPass = CondParserGenerator.get()
        self._secondLex, self._secondPass = ParserGenerator.get()

    def parseFormatExpr(self, expr):
        res1 = self._firstPass.parse(expr, lexer=self._firstLex)
        e1 = res1.unparse()
        while (self._firstLex.maxDepth>1):
            res1 = self._firstPass.parse(e1, lexer=self._firstLex)
            e1 = res1.unparse()

        return self._secondPass.parse(e1, lexer=self._secondLex)

    def run(self, expr, env):
        p = self.parseFormatExpr(expr)
        e = p.eval(env)

        return e
