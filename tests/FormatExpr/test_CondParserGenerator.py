from bibmanagement.FormatExpr import CondParserGenerator

def example():
    lexer, parser = CondParserGenerator.get()
    lexer.input(r"a<begin?>%ph%")
    #lexer.input(r"[azerty]")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    result = parser.parse(r"<begin?>%ph%")
    print(result.unparse())
    print('----------------------------\n')

    result = parser.parse(r"a<?-?>b")
    print(result.unparse())
    print('----------------------------\n')

    result = parser.parse(r"a<?-?>b<?-?>c")
    print(result.unparse())
    print('----------------------------\n')

if __name__ == "__main__":
    example()