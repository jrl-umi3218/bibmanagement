import FormatExpr.CondParserGenerator as CondParserGenerator
import FormatExpr.ParserGenerator as ParserGenerator

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

if __name__ == "__main__":
    class DummyField:
        def __init__(self, val):
            self.val = val

        def format(self, fmt):
            return self.val

    class Env: pass

    env = Env()
    env.data = {'ph' : DummyField('a'), 'qh' : DummyField(''), 'rh' : DummyField('c')}
    env.defaultFormat = {}
    env.defaultStyle = {}

    p = Parser()
    r = p.run(r"%ph%<?, {-}<?%ph%>?>%qh%<?, ?>%qh%<~@?>%rh%", env)
    print(r)
