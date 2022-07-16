from taskManager import taskManager
import unittest

class TestStringMethods(unittest.TestCase):
    def test_TaskManager(self):
        infoString = open("Task_folder/systemInfo.txt", "r").read()
        infoDiction = dict(x.split(":") for x in infoString.split("\n"))
        tm = taskManager()
        self.assertEqual(self.__discovered_plugins, infoDiction["Plugin_count"])

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()