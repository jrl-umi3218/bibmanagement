import yaml

class Condition:
    '''A functor used to check if a log record is meeting some conditions.'''
    
    def __init__(self, bibId=None, type=None, level=None, loggerName=None):
        '''
        Create a set of conditions that all need to be met.
        If an entry is set to None, it means that there is no condition for
        the corresponding field of the record.
        If an entry is set to '', it means that the record should not have the
        corresponding field.
        
        Parameters
        ----------
        bibId : str
            bibtex id of an entry. Checked against record.entry.id if it exists.
        type : str
            type of the log. Checked against record.type if it exists.
        level : str
            level name of the log record
        loggerName :
            name of the logger which emitted the record
        '''
        self.bibId = bibId.lower() if bibId else None
        self.type = type.lower() if type else None
        self.level = level.lower() if level else None
        self.loggerName = loggerName.split('.') if loggerName else None
        
    def __call__(self, record):
        '''
        Check if a log record satisfies the conditions.
        '''
        e = getattr(record, 'entry', None)
        return ((not self.bibId or (e.id if e else '') == self.bibId)
            and (not self.type or getattr(record, 'type', '') == self.type)
            and (not self.level or record.levelname.lower() == self.level)
            and (not self.loggerName or record.name.split('.')[1:] == self.loggerName))
        
    @staticmethod
    def conditions(bibId=None, type=None, level=None, loggerName=None):
        '''
        Create a list of all the possible combination of condition, based on
        the given arguments that can be list.
        
        For example, 
        c = Condition.conditions(['id1, id2'], None, 'warning', ['log1', 'log2', 'log3'])
        is equivalent to
        c = [Condition('id1', None, 'warning', 'log1'),
             Condition('id1', None, 'warning', 'log2'),
             Condition('id1', None, 'warning', 'log3'),
             Condition('id2', None, 'warning', 'log1'),
             Condition('id2', None, 'warning', 'log2'),
             Condition('id2', None, 'warning', 'log3')]
        '''
        return Condition._iterateInputs(0, bibId, type, level, loggerName)
        
    @staticmethod
    def _iterateInputs(i, *args):
        '''Subfunction for Condition.conditions'''
        if i == len(args):
            return [Condition(*args)]
        else:
            if args[i]:
                if isinstance(args[i], str):
                    return Condition._iterateInputs(i+1, *args)
                else:
                    try:
                        cds = []
                        for a in args[i]:
                            cds.extend(Condition._iterateInputs(i+1, *[*args[0:i], a, *args[i+1:]]))
                        return cds
                    except TypeError:
                        return Condition._iterateInputs(i+1, *args)
            else:
                return Condition._iterateInputs(i+1, *args)
                
    def toDict(self):
        return {k:v for (k,v) in self.__dict__.items() if v}
            
        
class SelectionFilter:
    '''
    A filter-like object for logging.
    
    Filtering is based on 2 lists of Condition:
     - a list of discard conditions
     - a list of exception conditions
    
    A record is kept if it does not meet any discard conditions or it statisfies
    an exception condition.
    A record is discarded if it meets a discard condition and it does not
    satisfy any exception conditions.
    '''
    
    def __init__(self, discardConditions=[], exceptConditions=[], removeDuplicates=False):
        self.discardConditions = discardConditions
        self.exceptConditions = exceptConditions
        self.duplicates = []  # a list of pair (condition, arguments)
        self.removeDuplicates = removeDuplicates
        
    def filter(self, record):
        ret = self._filter(record)
        if self.removeDuplicates and ret:
            for d in self.duplicates:
                if d[0](record) and d[1] == record.args:
                    return False
            e = getattr(record, 'entry', None)
            self.duplicates.append((Condition((e.id if e else None), getattr(record, 'type'), record.levelname, '.'.join(record.name.split('.')[1:])), record.args))
            return True
        else:
            return ret
            
    def _filter(self, record):
        discard = False
        for c in self.discardConditions:
            if c(record):
                discard = True
                break
                
        if discard:
            for c in self.exceptConditions:
                if c(record):
                    return True
            return False
        else:
            return True
            
    def addConditionsFromFile(self, filepath):
        ''' Read '''
        with open(filepath, 'r') as file:
            cond = yaml.safe_load(file)

        for d in cond.get('discard', []):
            cds = Condition.conditions(d.get('bibId'), d.get('type'), d.get('level'), d.get('loggerName'))
            self.discardConditions.extend(cds)

        for e in cond.get('except', []):
            cds = Condition.conditions(e.get('bibId'), e.get('type'), e.get('level'), e.get('loggerName'))
            self.discardConditions.extend(cds)
        