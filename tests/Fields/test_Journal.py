from bibmanagement.fields import Journal
import unittest
import os

class TestJournal(unittest.TestCase):
    def test1(self):
        dirpath = os.path.dirname(os.path.abspath(__file__))
        Journal.Journal.readVectorList(dirpath+'/../data/sample_journal.json')
            
        v = Journal.Journal.getVector('Autonomous Robots')
        self.assertEqual(v['abbr'], 'AURO')
        
        v = Journal.Journal.getVector('Int. J. Robot. Res.')
        self.assertEqual(v['abbr'], 'IJRR')
        
        v = Journal.Journal.getVector('INT J ROBOT RES')
        self.assertEqual(v['abbr'], 'IJRR')
        
        v = Journal.Journal.getVector('IJRR')
        self.assertEqual(v['abbr'], 'IJRR')
        
        v = Journal.Journal.getVector('International Journal of Robotics Research')
        self.assertEqual(v['abbr'], 'IJRR')
        
        v = Journal.Journal.getVector('Imaginary Journal')
        self.assertFalse(v)
        
        
        with self.assertRaises(ValueError):
            Journal.Journal.readVectorList(dirpath+'/../data/sample_journal_bad.json')
            
        Journal.Journal.resetVectorList()
        self.assertFalse(Journal.Journal._vectorList)

if __name__ == '__main__':
    unittest.main()