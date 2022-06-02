from bibmanagement.log import SelectionFilter
from bibmanagement.log import SelectionHandler
import logging
import warnings
import yaml

class Logger(logging.Logger):
    '''
    A specialized logger which overloads the debug, info, warning, error and
    critical method of classical loggers to add two arguments:
     - entry: the bibmanagement.Entry instance (if any) about which the logging
       is done
     - type: the name of the log type. It is linked to the message to be logged
     by the Logger._msg table. As such, it replaces the msg argument that is
     passed to a classical log method call.
     
     The other arguments are the same as with a classical log method.
    '''
    
    def __init__(self, name):
        super(Logger, self).__init__(name)
        
    def debug(self, entry, type, *args, **kwargs):
        super(Logger, self).debug(Logger._msg(entry, type), *args, extra = Logger._extra(entry, type), **kwargs)
        
    def info(self, entry, type, *args, **kwargs):
        super(Logger, self).info(Logger._msg(entry, type), *args, extra = Logger._extra(entry, type), **kwargs)
        
    def warning(self, entry, type, *args, **kwargs):
        super(Logger, self).warning(Logger._msg(entry, type), *args, extra = Logger._extra(entry, type), **kwargs)
        
    def error(self, entry, type, *args, **kwargs):
        super(Logger, self).error(Logger._msg(entry, type), *args, extra = Logger._extra(entry, type), **kwargs)
        
    def critical(self, entry, type, *args, **kwargs):
        super(Logger, self).critical(Logger._msg(entry, type), *args, extra = Logger._extra(entry, type), **kwargs)
    
    @staticmethod
    def _msg(entry, type):
        return ('[{}] '.format(entry.id) if entry else '') + Logger.__msg[type]
    
    @staticmethod
    def _extra(entry, type):
        if not type:
            raise ValueError('No type was specified in logging call')
        if (entry):
            return {'entry': entry, 'type': type}
        else:
            return {'type': type}
            
    
    __msg = {'chained_crossref'        : 'crossref %s in this entry contains another crossref. The second one is not processed.',
             'dismiss'                 : 'dismiss %s because %s',
             'more_than_3_name'        : 'Name with more than 3 components: %s.',
             'non_integer'             : 'Non-integer number %s passed to %s.',
             'not_in_data'             : 'Cannot find %s in data for %s, using default name instead.',
             'not_in_vector'           : 'Cannot find %s in vector list, using default name instead.',
             'numeric_value_expected'  : "Expected single numeric value, got %s instead.",
             'pub_already_present'     : 'Publication vector %s is already present in the list. Its data will be overwritten.',
             'unexpected_page_format'  : 'Unexpected page format %s.',
             'unrecognized_field_name' : 'Unrecognized field name %s.',
             'generic'                 : '%s'}
    

def getBibLogger(name):
    '''Create a logger and link it to the package main logger'''
    parent = logging.getLogger('bibmanagement')
    
    logging_class = logging.getLoggerClass()  # store the current logger factory for later
    logging._acquireLock()                    # use the global logging lock for thread safety
    try:
        logging.setLoggerClass(Logger)        # temporarily change the logger factory
        logger = logging.getLogger(name)
        logging.setLoggerClass(logging_class) # be nice, revert the logger factory change
        
        parent.addDescendant(logger)
        
        return logger

    finally:
        logging._releaseLock()

def addLogConditions(yamlFile):
    '''Add filters on package log based on te content of yamlFile'''
    packageLogger = logging.getLogger('bibmanagement')
    assert(getattr(packageLogger.filters[0], 'name') == 'main')
    packageLogger.filters[0].addConditionsFromFile(yamlFile)
    
def writeSelectionConditions(yamlFile, discard, exceptions):
    '''Write filter conditions, to be used by the package logger in the future'''
    yamlDict = {'discard':[d.toDict() for d in discard], 'except': [e.toDict() for e in exceptions]}
    with open(yamlFile, 'w') as file:
        print('writing to {} ... '.format(yamlFile))
        yaml.dump(yamlDict, file)
        print('Done')
        
def setupSelectHandler(addConsole=True):
    '''
    Add a SelectionHandler to the package logger. Since doing so will remove
    the default handler outputing to the console, this also add by default a
    StreamHandler.
    '''
    packageLogger = logging.getLogger('bibmanagement')
    sh = SelectionHandler.SelectionHandler()
    sh.name = 'main'
    packageLogger.addHandler(sh)
    
    if addConsole:
        ch = logging.StreamHandler()
        packageLogger.addHandler(ch)
    
def startLogSelection(yamlFile):
    '''
    Start an interactive session to chose which log message to keep or to
    ignore. The previously used ignore list and the choice of this interactive
    session are then saved into yamlFile.
    '''
    packageLogger = logging.getLogger('bibmanagement')
    sh = None
    for h in packageLogger.handlers:
        if getattr(h, 'name') == 'main':
            sh = h
            break
            
    if not sh:
        warnings.warns('No SelectionHandler attached to package logger.\nPlease use bibmanagement.log.setupSelectHandler() to configure the process properly.')
        return
        
    if not (getattr(packageLogger.filters[0], 'name') == 'main'):
        warnings.warns('Unable to find the SelectionFilter automatically attached to the package logger.')
        return
    
    f = packageLogger.filters[0]
    
    cond = sh.interactiveProcess()
    discard = f.discardConditions + cond
    writeSelectionConditions(yamlFile, discard, f.exceptConditions)
    
def setup(ignoreFile=None, useSelectHandler=True, useConsole=True, removeDuplicates=True):
    '''Setup the log facilities for the package.'''
    if ignoreFile:
        addLogConditions(ignoreFile)
    if useSelectHandler:
        setupSelectHandler(useConsole)
    packageLogger = logging.getLogger('bibmanagement')
    assert(getattr(packageLogger.filters[0], 'name') == 'main')
    packageLogger.filters[0].removeDuplicates = removeDuplicates
    