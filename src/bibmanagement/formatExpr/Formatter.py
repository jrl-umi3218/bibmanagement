from bibmanagement.formatExpr import Parser

class Env:
    def __init__(self):
        self.defaultFormat = {}
        self.defaultStyle = {}

class Formatter:
    def __init__(self):
        self._parser = Parser.Parser()
        self._env = Env()

    def run(self, entry, formatExpr):
        self._env.data = entry
        return self._parser.run(formatExpr, self._env)

class FixedFormatter:
    def __init__(self, formatExpr):
        parser = Parser.Parser()
        self._env = Env()
        self._parsedExpr = parser.parseFormatExpr(formatExpr)

    def run(self, entry):
        self._env.data = entry
        return self._parsedExpr.eval(self._env)