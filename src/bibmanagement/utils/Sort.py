# Copyright 2019-2022 CNRS-AIST JRL

class MixComp:
    '''A class for comparing tuples with a mix of lower and greater comparison'''

    def __init__(self, order):
        '''
        Order must be a list of either \'<\' or \'>\'.
        The i-th element of this list specifies how to compare the i-th elements of two tuples/lists
        
        For example if comp = MixComp([\'>\', \'<\', \'<\'])
         - comp((1,2,3), (2,2,3)) returns False (1 is not greater than 2)
         - comp((1,2,3), (0,2,3)) returns True  (1 is greater than 0)
         - comp((1,2,3), (1,3,3)) returns True  (1 equals 1 and 2 is lower than 3)
         - comp((1,2,3), (1,1,3)) returns False (1 equals 1 and 2 is not lower than 1) 
         - comp((1,2,3), (1,2,4)) returns True (1 equals 1, 2 equals 2 and 3 is lower than 4)
         - comp((1,2,3), (1,2,2)) returns True  (1 equals 1, 2 equals 2 and 3 is not lower than 2)
         - comp((1,2,3), (1,2,3)) returns False (1 equals 1, 2 equals 2 and 3 is not lower than 3)
        '''
        self._order = []
        for o in order:
            if o=='<':
                self._order.append(True)
            elif o=='>':
                self._order.append(False)
            else:
                raise ValueError(o + ' is not a valid ordering')
        self._n = len(order)

    def __call__(self, x, y):
        u = [x] if type(x) not in (tuple, list) else x
        v = [y] if type(y) not in (tuple, list) else y
        assert(len(u)==len(v))
        assert(len(u)==self._n)
        return self._comp(u,v)

    def _comp(self,x,y):
        for (o,u,v) in zip(self._order, x, y):
            if o:
                if u < v:
                    return True
                elif u > v:
                    return False
                #else, go on and compare the next values
            else:
                if u > v:
                    return True
                elif u < v:
                    return False
                #else, go on and compare the next values
        return False


class MixCompKey:
    '''
    A value with a MixComp comparator.
    The comparator is used to implement the \'lower than\' operator
    '''
    def __init__(self, val, comp):
        self._val = val
        self._comp = comp

    def __lt__(self, other):
        return self._comp(self._val, other._val)