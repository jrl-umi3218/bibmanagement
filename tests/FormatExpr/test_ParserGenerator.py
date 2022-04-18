from bibmanagement.FormatExpr import ParserGenerator

def example():
    lexer, parser = ParserGenerator.get()
    lexer.input(r"{%ph% and [azerty[\]]%another%{a|b}]%qh%} \\<?, ?> %rh%")
    #lexer.input(r"[azerty]")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

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

    result = parser.parse(r"z{%ph% and [azerty[\]]%another%{a|b}]%qh%} %rh%?d")
    print(result.eval(env))
    print('----------------------------\n')
    
    result = parser.parse(r"%ph%{{%ph%?%qh%}?, }%qh%{{%ph%%qh%}?%rh%}?, %rh%")
    print(result.eval(env))
    print('----------------------------\n')

if __name__ == "__main__":
    example()
