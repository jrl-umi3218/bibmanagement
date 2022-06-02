import os
import unittest


class TestCNRSScript(unittest.TestCase):
    def test_script(self):
        dirPath = os.path.dirname(os.path.abspath(__file__))
        dataPath = os.path.join(dirPath, '../data')
        outPath = os.path.join(dirPath, '../out')
        filepath = os.path.join(dirPath, '../../scripts/cnrs-report.py')
        global_namespace = {
            "__file__": filepath,
            "__name__": "__test__",
        }
        local_namespace = {
            "dataPath"   : dataPath+'/',
            "bibFile"    : 'sample.bib',
            "journalFile": 'sample_journal.json',
            "confFile"   : 'sample_conf.json',
            "outPath"    : outPath+'/'
        }
        with open(filepath, 'rb') as file:
            exec(compile(file.read(), filepath, 'exec'), global_namespace, local_namespace)

if __name__ == '__main__':
    unittest.main()