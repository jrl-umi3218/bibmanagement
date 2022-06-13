# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.log import SelectionFilter
import logging
import sys
        
class PackageLogger(logging.Logger):
    def __init__(self, name):
        super(PackageLogger, self).__init__(name)
        self.descendant = []
        
    def addDescendant(self, d):
        self.descendant.append(d)
        for f in self.filters:
            if not f in d.filters:
                d.addFilter(f)
                
    def addFilter(self, f):
        super(PackageLogger, self).addFilter(f)
        for d in self.descendant:
            d.addFilter(f)
    
    def removeFilter(self, f):
        super(PackageLogger, self).removeFilter(f)
        for d in self.descendant:
            d.removeFilter(f)    
    
# Create a customized main logger for the package.
# The goal is to have a SelectionFilter shared accros this logger and all its
# sub-logger.
# We do this because filters at the logger level are not inherited. 
logging_class = logging.getLoggerClass()                # store the current logger factory for later
logging._acquireLock()                                  # use the global logging lock for thread safety
try:
    logging.setLoggerClass(PackageLogger)               # temporarily change the logger factory
    packageLogger = logging.getLogger('bibmanagement')
    logging.setLoggerClass(logging_class)               # be nice, revert the logger factory change
finally:
    logging._releaseLock()

f = SelectionFilter.SelectionFilter()
f.name = 'main'
packageLogger.addFilter(f)

if 'unittest' in sys.modules:
    packageLogger.setLevel(logging.ERROR)
else:
    packageLogger.setLevel(logging.INFO)
