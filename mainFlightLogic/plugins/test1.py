'''
This is the "test1" plugin.

The test1 plugin is only for testing and logs that it has run.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Test1(Plugin):
    def __init__(self, pluginId, fileName, className):
        super().__init__(pluginId, fileName, className)

    '''
    ----------------------------------------------------------------------------
    Plugin methods

    These methods are used to perform the plugin's functionality.
    ----------------------------------------------------------------------------

    public start()

    This method is used to start the plugin.
    '''
    def start(self, taskId, taskManager):
        Log.newInfo("Test 1 plugin started", taskId, self.getPluginId())

        from objects.task import Task
        from plugins.test2 import Test2
        test2Plugin = Test2.newPlugin(taskId, self.getPluginId())

        from objects.task import Task
        from model import Model

        test2Task = Task.priorityTask(200, test2Plugin, [], taskId, self.getPluginId())
        taskManager.addTask(test2Task)

        test2Task2 = Task.scheduleTaskDelta(200, test2Plugin, 6, 10, [], taskId, self.getPluginId())
        taskManager.addTask(test2Task2)

        test2Task3 = Task.scheduleTaskDelta(200, test2Plugin, 5, 10, [], taskId, self.getPluginId())
        taskManager.addTask(test2Task3)
    
    def terminate(self, taskId):
        pass