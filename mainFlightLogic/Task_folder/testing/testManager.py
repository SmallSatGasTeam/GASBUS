import unittest
from taskManager import taskManager

class testManager(unittest.TestCase):
    def test_TaskManager(self):
        file = open("testing/systemInfo.txt", "r")
        infoString = file.read()
        file.close()
        infoDiction = dict(x.split(":") for x in infoString.split("\n"))
        tm = taskManager()
        self.assertEqual(int(infoDiction["Plugin_count"]), len(tm.getPlugins()))
        self.assertEqual(len(tm.getPlugins()), len(tm.getTasks()))