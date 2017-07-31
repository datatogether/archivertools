import unittest
import archivertools
import os

class MetadataTest(unittest.TestCase):
    def test_run_id_autoincrement(self):
        '''
        tests if creating a new archiver run correctly autoincrements the run
        '''
        archiver = archivertools.Archiver('http://example.org','0000')
        archiver2 = archivertools.Archiver('http://example.org','0000')
        self.assertEqual(archiver.run_metadata.run_id, archiver2.run_metadata.run_id-1)

class URLTest(unittest.TestCase):
    def setUp(self):
        self.archiver = archivertools.Archiver('http://example.org','0000')
        self.assertIsInstance(self.archiver,archivertools.Archiver)

    def test_add_url(self):
        self.archiver.addURL('http://example.org/example')

    def test_add_duplicate_url(self):
        try:
            self.archiver.addURL('http://example.org/duplicate')
            self.archiver.addURL('http://example.org/duplicate')
        except:
            raise

class fileTest(unittest.TestCase):
    def setUp(self):
        self.archiver = archivertools.Archiver('http://example.org','0000')
        self.assertIsInstance(self.archiver,archivertools.Archiver)

    def test_add_file(self):
        with open('test.txt','w') as test_file:
            test_file.write('contents of test file\n')
        self.archiver.addFile('test.txt')
        os.remove('test.txt')

if __name__ == '__main__':
    unittest.main()
