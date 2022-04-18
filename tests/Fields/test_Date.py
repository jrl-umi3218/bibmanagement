from bibmanagement.Fields import Date

def test01():
    import random
    chars = [' ', ' ', ' ', 'd', 'm', 'y']
    accepted = Date._acceptedFormat()
    def generatePattern():
        """ Generate a random pattern """
        useRange = random.random()>=0.5
        s1 = ''
        s = ''
        for i in range(0,4):
            s1 = s1 + random.choice(chars)
        if useRange:
            s2 = ''
            for i in range(0,4):
                s2 = s2 + random.choice(chars)
            s = (s1+'-'+s2).replace(' ', '')
        else:
            s = s1.replace(' ', '')
        return (s, s in accepted)

    days1 = {'1':True, '15': True, '07': True, '0': False}
    days2=  {'19': True, '21': True, '27': True, '123':False}
    months1 = {'January':True, 'february':True, 'mar': True, 'Apr': True, 'Decemberq': False, 'other': False}
    months2 = {'May': True, 'Jun.':True, 'jul.':True, 'aug': True, 'Sept':False, 'Octobre':False,  'november':True}
    years1 = {'1687':True, '889': False, '1902,': True, '1982': True}
    years2 = {'2014': True, '3201': False, '2899': True, '2006,': True}
    sep = {'-': True, '-': True, '-': True, '--' : True, '---': False, '&': False}
    map1 = {'d':days1, 'm':months1, 'y':years1, '-':sep}
    map2 = {'d':days2, 'm':months2, 'y':years2, '-':sep}

    for i in range(0,100000):
        p, shouldWork = generatePattern()
        string = ''
        after = False  #before or after dash
        for c in p:
            if c == '-':
                after = True
            if after:
                s,b = random.choice([*map2[c].items()])
            else:
                s,b = random.choice([*map1[c].items()])
            string = string + s + ' '
            shouldWork = shouldWork and b

        try:
            d = Date.Date(string)
            if not shouldWork:
                print('Fails to catch error for \n  ' + string)
        except:
            if shouldWork:
                print('Unexpected failure\n  ' + string)


def test02():
    input = [1, 2, 3, 4, 5, 6, 7, 8, 9,  10 , 11, 12, 13, 14, 20, 21, 22, 23, 24]
    ans = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '20th', '21st', '22nd', '23rd', '24th']
    for i,a in zip(input, ans):
        if a != Date.Date._makeOrdinal(i):
            print('Unexpected output for ' + str(i))

if __name__ == "__main__":
    test01()
    test02()
