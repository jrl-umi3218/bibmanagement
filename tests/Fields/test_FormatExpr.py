from bibmanagement.Fields import FormatExpr

def test01():
    ph = ['field1', 'field2', 'field3', 'field4', 'field5']

    def test(expr,replacements,expected):
        format = FormatExpr.FormatExpr(ph, expr)
        s = format.reduce(replacements)
        assert(s == expected)

    test('%field1% + %field2% = %field3%', ['1','2','3'], '1 + 2 = 3')
    test('%field2%[/]%field3%', ['1','2'], '1/2')
    test('%field2%[/]%field3%', ['1','#'], '1')
    test('%field2%[/]%field3%', ['#','2'], '2')

    test('%field1%[, %field2%][, ]%field3%', ['1', '2', '3'], '1, 2, 3')
    test('%field1%[, %field2%][, ]%field3%', ['1', '2', '#'], '1, 2')
    test('%field1%[, %field2%][, ]%field3%', ['1', '#', '3'], '1, 3')
    test('%field1%[, %field2%][, ]%field3%', ['#', '2', '3'], ', 2, 3')
    test('%field1%[, %field2%][, ]%field3%', ['1', '#', '#'], '1')
    test('%field1%[, %field2%][, ]%field3%', ['#', '2', '#'], ', 2')
    test('%field1%[, %field2%][, ]%field3%', ['#', '#', '3'], '3')
    test('%field1%[, %field2%][, ]%field3%', ['#', '#', '#'], '')

    test('%field1%[, ]%field2%[, ]%field3%', ['1', '2', '3'], '1, 2, 3')
    test('%field1%[, ]%field2%[, ]%field3%', ['1', '2', '#'], '1, 2')
    test('%field1%[, ]%field2%[, ]%field3%', ['1', '#', '3'], '1, 3')
    test('%field1%[, ]%field2%[, ]%field3%', ['#', '2', '3'], '2, 3')
    test('%field1%[, ]%field2%[, ]%field3%', ['1', '#', '#'], '1')
    test('%field1%[, ]%field2%[, ]%field3%', ['#', '2', '#'], '2')
    test('%field1%[, ]%field2%[, ]%field3%', ['#', '#', '3'], '3')
    test('%field1%[, ]%field2%[, ]%field3%', ['#', '#', '#'], '')

    test(r'[\[%field1%\]]', ['1'], '[1]')
    test(r'\%%field1%', ['1'], '%1')
    
    
if __name__ == "__main__":
    test01()