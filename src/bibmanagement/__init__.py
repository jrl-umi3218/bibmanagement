from bibmanagement.log import SelectionFilter
import logging
import sys

packageLogger = logging.getLogger('bibmanagement')
packageLogger.addFilter(SelectionFilter.SelectionFilter())

if 'unittest' in sys.modules:
    packageLogger.setLevel(logging.ERROR)
