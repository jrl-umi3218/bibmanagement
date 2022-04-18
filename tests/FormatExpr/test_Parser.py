from bibmanagement.FormatExpr.Parser import Parser

if __name__ == "__main__":
    class DummyField:
        def __init__(self, val):
            self.val = val

        def format(self, fmt, st):
            return self.val

    class Env: pass

    env = Env()
    env.data = {'ph' : DummyField('a'), 'qh' : DummyField(''), 'rh' : DummyField('c')}
    env.defaultFormat = {}
    env.defaultStyle = {}

    p = Parser()
    r = p.run(r"%ph%<?, {-}<?%ph%>?>%qh%<?, ?>%qh%<~@?>%rh%", env)
    print(r)
