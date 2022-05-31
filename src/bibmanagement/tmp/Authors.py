from bibmanagement.Fields.Field import Field
from bibmanagement.Fields.Name import Name
from bibmanagement.utils.FormattedString import Single

class Authors(Field):
    """All the authors of an entry"""
    #The name(s) of the author(s) (in the case of more than one author, separated by and)
    
    _defaultFormatExpr = '{%F% %Last%}{, }{ and }{}'

    def __init__(self, authors):
        self._authors = authors

    @classmethod
    def _fromString(cls, str, e):
        authors = [Name(n.strip(), e) for n in str.split(' and ')]
        return cls(authors)
        
    def __getitem__(self, item):
        return self._authors[item]

    def _format(self, formatString, style):
        """
        formatString has the following form '{nameFormat}{sep}{endSep}{maxName}'
        where:
         - nameFormat is a format string indicating how a name should be displayed (see class Name)
         - sep is a separator between two names
         - endSep is the separator between the two last names (if both are displayed).
           Keep empty if endSep is the same as sep.
         - maxName indicates the maximum number of name displayed before 'et al.'. 
           It can be a number n or a number immediately followed by '!'. In the former case,
           n names will be displayed before 'et al.', unless there is exactly n+1 names, in
           which case all will be displayed. In the latter case, no more than n names will be
           displayed, whatever the situation.
           If maxName is empty, all names will be displayed.
        """

        l = Authors._extractBracedParts(formatString)
        if len(l) != 4:
            raise ValueError("Incorrect number of arguments")

        sep = l[1]
        endSep = l[2] if l[2] else sep

        n = len(self._authors)
        if n==1:
            return Single('author', self._authors[0].format(l[0]), style)
        
        if l[3]:
            if l[3][-1]=='!':
                maxNames = int(l[3][0:-1])
                strict = True
            else:
                maxNames = int(l[3])
                strict = False
        else:
            maxNames = len(self._authors)

        s = ""
        if n <= maxNames or n == maxNames+1 and not strict:
            for i in range(0,n-2):
                s += self._authors[i].format(l[0]) + sep
            s += self._authors[-2].format(l[0]) + endSep + self._authors[-1].format(l[0])
        else:
            for i in range(0,maxNames-1):
                s += self._authors[i].format(l[0]) + sep
            s += self._authors[maxNames-1].format(l[0]) + ' et al.'

        return Single('author',s,style)


    @staticmethod
    def _extractBracedParts(str):
        str = str.strip()
        if str[0] != '{':
            raise ValueError("Expecting string starting with {")
        k = 1
        n = len(str)
        for i in range(1,n):
            if str[i] == '{':
                k += 1
            elif str[i] == '}':
                k -= 1
            if k==0:
                if i!=n-1:
                    return [str[1:i]] + Authors._extractBracedParts(str[i+1:n])
                else:
                    return [str[1:i]]

        raise ValueError("unbalanced braces")
