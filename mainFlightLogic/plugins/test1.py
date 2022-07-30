'''
This is the "test1" plugin.

The test1 plugin is only for testing and logs that it has run.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Test1(Plugin):
    def __init__(self, pluginId, fileName, className):
        super().__init__(pluginId, fileName, className, self)

    @classmethod
    def newPlugin(cls, runTaskId, runPluginId):
        plugin = super().newPlugin(cls, 'test1', 'Test1', runTaskId, runPluginId)
        return plugin

    '''
    ----------------------------------------------------------------------------
    Plugin methods

    These methods are used to perform the plugin's functionality.
    ----------------------------------------------------------------------------

    public start()

    This method is used to start the plugin.
    '''
    def start(self, taskId, taskManager):
        Log.newLog("Test 1 plugin started", taskId, self.getPluginId(), 100)

        from objects.task import Task
        from plugins.test2 import Test2
        test2Plugin = Test2.newPlugin(taskId, self.getPluginId())

        from objects.task import Task
        from model import Model

        test2Task = Task.newTaskFromPlugin(200, test2Plugin, -1, -1, Model.createTimeStamp(), -1, -1, -1, True, taskId, self.getPluginId())
        taskManager.addTask(test2Task)

        test2Task2 = Task.newTaskFromPlugin(200, test2Plugin, -1, -1, Model.createTimeStamp(), Model.createTimeStamp() + 6, -1, -1, True, taskId, self.getPluginId())
        taskManager.addTask(test2Task2)

        test2Task3 = Task.newTaskFromPlugin(200, test2Plugin, -1, -1, Model.createTimeStamp(), Model.createTimeStamp() + 5, -1, -1, True, taskId, self.getPluginId())
        taskManager.addTask(test2Task3)
    
    def terminate(self, taskId):
        pass