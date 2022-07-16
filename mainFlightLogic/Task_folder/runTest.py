from taskManager import taskManager
import unittest

class TestStringMethods(unittest.TestCase):
    def test_TaskManager(self):
        file = open("Task_folder/systemInfo.txt", "r")
        infoString = file.read()
        file.close()
        infoDiction = dict(x.split(":") for x in infoString.split("\n"))
        tm = taskManager()
        self.assertEqual(int(infoDiction["Plugin_count"]), len(tm.getPlugins()))
        self.assertEqual(len(tm.getPlugins()), len(tm.getTasks()))

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