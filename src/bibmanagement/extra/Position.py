import datetime
import re

class PreviousDay:
        def __init__(self, val):
            self.val = val
            
        def __repr__(self):
            return 'Prev({})'.format(self.val)

class Position:
    _possibleStatus = ["trainee", 
                       "master", 
                       "PhD", 
                       "postdoc", 
                       "adjunct", 
                       "researcher", 
                       "senior researcher", 
                       "assistant professor",
                       "professor",
                       "engineer", 
                       "technical", 
                       "administrative", 
                       "other",
                       "n/a"]
    _possibleContract = ["ra", 
                         "grant", 
                         "tenure", 
                         "project", 
                         "fixed", 
                         "permanent", 
                         "visitor",
                         "other", 
                         "n/a"]
     
     
    @staticmethod
    def _processDate(date):
        if isinstance(date, datetime.date):
            return date
        elif isinstance(date, str):
            s = [x.strip() for x in re.split(r',|/|\.| |-', date)]
            if any([not x.isdigit() for x in s]):
                raise ValueError('Invalid date: {}'.format(date))
            s = [int(x) for x in s]
            if len(s) == 1 and s[0]>=1000 and s[0]<10000: #assume year only was given
                s.extend([1,1]) # add month and day
            elif len(s) == 2 and s[0]>=1000 and s[0]<10000 and s[1]>=1 and s[1]<=12: #assume year and month
                s.append(1) # add day
            if len(s) != 3:
                raise ValueError('Invalid date: {}'.format(date))
            return datetime.date(*s)
        elif isinstance(date, PreviousDay):
            return Position._processDate(date.val) - datetime.timedelta(1)
        else:
            raise ValueError('Invalid type for date: {}'.format(date))

    def __init__(self, start=datetime.date(1900,1,1), end=datetime.date(9999,12,31), status=None, 
                 contract=None, employer=None, affiliation=None, pubStart=None, pubEnd=None, **kwargs):
        self.start = Position._processDate(start)
        self.end = Position._processDate(end)
        
        if (self.start >= self.end):
            raise ValueError('Start date ({}) is after end date ({})'.format(start, end))
            
        if not status or (isinstance(status, str) and status.lower() in Position._possibleStatus):
            self.status = status
        else:
            raise ValueError('Invalid status: {}'.format(status))
            
        if not contract or (isinstance(contract, str) and contract.lower() in Position._possibleContract):
            self.contract = contract
        else:
            raise ValueError('Invalid contract: {}'.format(contract))
        
        self.employer = employer
        self.affiliation = affiliation
        self.pubStart = Position._processDate(pubStart) if pubStart else self.start
        self.pubEnd = Position._processDate(pubEnd) if pubEnd else self.end
        if (self.pubStart >= self.pubEnd):
            raise ValueError('Start date ({}) is after end date ({})'.format(self.pubStart, self.pubEnd))
            
    def coversDate(self, date):
        d = Position._processDate(date)
        return self.start <= d and d <= self.end
        
    def coversPubDate(self, date):
        d = Position._processDate(date)
        return self.pubStart <= d and d <= self.pubEnd