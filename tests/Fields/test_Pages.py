from bibmanagement.Fields import Pages

def test01():
    p1 = Pages.Pages.fromString('10--15')
    p2 = Pages.Pages(3)
    
    assert(str(p1.format('%page% %f%[--]%l%')) == 'pages 10--15')
    assert(str(p2.format('%page% %f%[--]%l%')) == 'page 3')
    assert(str(p1.format('%p% %f%[ - ]%l%')) == 'pp. 10 - 15')
    assert(str(p2.format('%p% %f%[-]%l%')) == 'p. 3')
    
if __name__ == "__main__":
    test01()