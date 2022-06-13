# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.log.SelectionFilter import Condition
import logging

class SelectionHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super(SelectionHandler, self).__init__(level)
        self.memory = []
        
    def emit(self, record):
        self.memory.append(record)
        
    def interactiveProcess(self):
        conditions = []
        for r in self.memory:
            print('\n', self.format(r))
            while True:
                s = input('(k)eep   (i)gnore   ignore (t)ype   ignore (e)ntry\n').lower()
                if s in 'kite':
                    break
            
            e = getattr(r, 'entry', None)
            if s == 'i':
                c = Condition((e.id if e else None), getattr(r, 'type'))
            elif s == 't':
                c = Condition(None, getattr(r, 'type'))
            elif s == 'e':
                c = Condition((e.id if e else None))
            else:
                c = None
                
            if c:
                conditions.append(c)
        
        self.memory = []
        return conditions