class Comparator:
    '''
    Base class for filter comparator
    
    A comparator is a functor taking a single argument (which can be an iterable).
    '''
    
    def __init__(self, any=True):
        self._any = any
        
    def __call__(self, x):
        if isinstance(x, str):
            return self._run(x.lower())
        try:
            iter(x)
        except:
            return self._run(x)
        else:
            b = not self._any # if we do `or`, we need to start with False, if we do `and`, True
            for v in x:
                bi = self._run(v.lower() if isinstance(v,str) else v)
                b = b or bi if self._any else b and bi
            return b
            
    def __and__(self, other):
        return And(self, other)
        
    def __or__(self, other):
        return Or(self, other)
        
    def _run(self, x):
        raise NotImplementedError()
        
    def _initVal(self, val):
        if isinstance(val, str):
            self._val = val.lower()
            return
        try:
            iter(val)
        except:
            self._val = val
        else:
            self._val = [v.lower() if isinstance(v, str) else v for v in val]
        
class And(Comparator):
    '''And of two comparisons'''
    
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs
        super().__init__()
    
    def _run(self, x):
        return self._lhs(x) and self._rhs(x)
        
class Or(Comparator):
    '''Or of two comparisons'''
    
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs
        super().__init__()
    
    def _run(self, x):
        return self._lhs(x) or self._rhs(x)
        
class Not(Comparator):
    '''Not of a comparison'''
    
    def __init__(self, comp):
        self._comp = comp
        super().__init__()
    
    def _run(self, x):
        return not self._comp(x)
        
class EQ(Comparator):
    '''Test if the input is equal to a given value'''
    
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return x == self._val
        
class NE(Comparator):
    '''Test if the input is different from a given value'''
    
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return x != self._val
        
class GE(Comparator):
    '''Test if the input is greater than or equal to a given value'''
    
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return x >= self._val
        
class LE(Comparator):
    '''Test if the input is lower than or equal to a given value'''
    
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return x <= self._val
        
class GT(Comparator):
    '''Test if the input is greater than a given value'''
    
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return x > self._val
        
class LT(Comparator):
    '''Test if the input is lower than a given value'''
    
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return x < self._val
        
class IN(Comparator):
    '''Test if the input is in a given collection'''
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return x in self._val
        
class Contains(Comparator):
    '''Test if the input contains a given collection'''
    def __init__(self, val, any=True):
        self._initVal(val)
        super().__init__(any)
    
    def _run(self, x):
        return self._val in x
      
      
class Selector:
    '''A functor helper for implementing a selection criterion on bib entries'''
    
    def __init__(self, type=None, year=None, FY=None, author=None, lab=None, title=None, committee=None, national=None):
        '''
        The arguments specify on which criteria the selection will be done. They can be either a
        value or a functor. If a a value is given, equality to this value will be tested.
        
        Keyword arguments
        type -- the type of the entry. The comparison is made with the name of the entry type.
        year -- the year of the entry. The comparison is made with the year of publication of the entry.
        FY -- the (Japanese) fiscal year of the entry. Entries without a month will be discarded.
        author -- an author or list of authors. The comparison is made with the name of the authors in the form Firstname Lastname (case insensitive).
        lab -- the laboratory of the entry.
        title -- the title or a criterion on the title of the entry.
        committee -- whether the entry was peer-reviewed or not
        national -- whether the entry is in national or international proceeedings
        '''
        if isinstance(type, str):
            self._type = EQ(type.lower())
        else:
            self._type = type
        if isinstance(year, int):
            self._year = EQ(year)
        else:
            self._year = year
        if isinstance(FY, int):
            self._fy = lambda m, y : (m>=4 and y==FY) or (m<=3 and y==FY+1)
        else:
            if FY:
                self._fy = lambda m, y : (m>=4 and FY(y)) or (m<=3 and FY(y-1))
            else:
                self._fy = None
        if isinstance(author, str):
            self._author = IN(author)
        else:
            self._author = author
        if isinstance(lab, str):
            self._lab = EQ(lab)
        else:
            self._lab = lab
        if isinstance(title, str):
            self._title = EQ(title)
        else:
            self._title = title
        if isinstance(committee,bool):
            self._committee = EQ(committee)
        else:
            self._committee = committee
        if isinstance(national,bool):
            self._national = EQ(national)
        else:
            self._national = national
        
    def __call__(self, x):
        try:
            return self._run(x)
        except BaseException as err:
            print("dismiss {0} because {1}".format(x.id, err))
            return False
            
    def _run(self, x):
        if 'ENTRYTYPE' in x.raw():
            t = x.raw()['ENTRYTYPE'].lower()
        else:
            raise ValueError("Entry {0} has no type".format(x.id))
            
        if self._type:
            if not self._type(t):
                return False
                
        if self._year:
            y = int(str(x.format('%year%')))
            if not self._year(y):
                return False
                
        if self._fy:
            m = int(str(x.format('[%m%]%month%')))
            y = int(str(x.format('%year%')))
            if not self._fy(m,y):
                return False
            
        if self._author:
            a = str(x.format("[{%First% %Last%}{,}{,}{}]%author%")).split(',')
            if not self._author(a):
                return False
        
        if self._lab:
            l = str(x.lab).lower()
            if not self._lab(l):
                return False
                
        if self._committee:
            v = x.journal if t == 'article' else x.booktitle
            if not self._committee(v.get("committee")):
                return False
                
        if self._national:
            v = x.journal if t == 'article' else x.booktitle
            if not self._national(v.get("national")):
                return False
                
        return True