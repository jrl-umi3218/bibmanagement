from bibmanagement.check import Names
from bibmanagement.Biblio import Biblio
from .. import testEntries
import logging
import unittest

class TestNames(unittest.TestCase):
    def test(self):
        entries = testEntries()
        entries[1]['author'] = 'O., Chou and A., Lai'
        bib = Biblio(entries)
        
        logger = logging.getLogger('bibmanagement.check.Names')
        oldLevel = logger.level
        logger.setLevel(logging.INFO)
        mh = logging.handlers.MemoryHandler(100)
        logger.addHandler(mh)
        
        Names.all(bib)
        
        self.assertEqual(len(mh.buffer), 13)
        self.assertEqual(mh.buffer[0].entry.id, 'einstein:nfs:1974')
        self.assertEqual(mh.buffer[0].type, 'possible_typo')
        self.assertEqual(mh.buffer[1].entry.id, 'chou:laryngol:1927')
        self.assertEqual(mh.buffer[1].type, 'possible_name_switch')
        self.assertEqual(mh.buffer[3].entry.id, 'chou:fat:1927')
        self.assertEqual(mh.buffer[3].type, 'possible_abbr')
        
        
        logger.setLevel(oldLevel)

if __name__ == '__main__':
    unittest.main()