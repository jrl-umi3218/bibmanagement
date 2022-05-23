import logging

class Logger(logging.Logger):
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
            
    
    __msg = {'dismiss'                 : 'dismiss %s because %s',
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
    '''Create a logger and add to it the filters of the package main logger'''
    parent = logging.getLogger('bibmanagement')
    
    logging_class = logging.getLoggerClass()  # store the current logger factory for later
    logging._acquireLock()                    # use the global logging lock for thread safety
    try:
        logging.setLoggerClass(Logger)        # temporarily change the logger factory
        logger = logging.getLogger(name)
        logging.setLoggerClass(logging_class) # be nice, revert the logger factory change
        
        for f in parent.filters:
            if not f in logger.filters:
                logger.addFilter(f)
        
        return logger

    finally:
        logging._releaseLock()
