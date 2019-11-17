'''
Written by : Venkata Khande
Test all the functions written in the other file
'''

import unittest
from HW09_Venkata_Khande import Pack

filePath = 'testingFiles'  


class TestPack(unittest.TestCase):
    """ Unit testing File Generators """

    def test_student(self):
        """ Testing student information extracted"""
        test_path = Pack(filePath)
        self.assertEqual(list(test_path.studentInfo.keys()), ["10103","11658"])


    def test_instructor(self):
        """ Testing Instructor information extracted"""
        test_path = Pack(filePath)
        self.assertEqual(list(test_path.insructorsInfo.keys()), ["98765", "98764"])

    def test_major(self):
        test_path = Pack(filePath)
        self.assertEqual(list(test_path.majorsData.keys()), ["SFEN", "SYEN"])
    

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
