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
    def start(self, taskId, taskManager, taskParameters):
        Log.newInfo("Test 1 plugin started", taskId, self.getPluginId())

        from objects.task import Task
        from plugins.test2 import Test2
        test2Plugin = Test2.newPlugin(taskId, self.getPluginId())

        from objects.task import Task
        from model import Model

        # Test 2 immediate
        test2Task = Task.priorityTask(200, test2Plugin, [200, 'immediate'], taskId, self.getPluginId())
        taskManager.addTask(test2Task)

        # Test 2 delayed 7 seconds
        test2Task2 = Task.scheduleTaskDelta(200, test2Plugin, 7, [200, '7 seconds'], taskId, self.getPluginId())
        taskManager.addTask(test2Task2)

        # Test 2 delayed 6 seconds
        test2Task3 = Task.scheduleTaskDelta(200, test2Plugin, 6, [200, '6 seconds'], taskId, self.getPluginId())
        taskManager.addTask(test2Task3)

        # Test 2 delayed 5 seconds
        test2Task4 = Task.scheduleTaskDelta(200, test2Plugin, 5, [200, '5 seconds'], taskId, self.getPluginId())
        taskManager.addTask(test2Task4)

        # Test 2 delayed 8 seconds
        test2Task5 = Task.scheduleTaskDelta(200, test2Plugin, 8, [200, '8 seconds'], taskId, self.getPluginId())
        taskManager.addTask(test2Task5)

        # Test 2 delayed 20 seconds
        test2Task6 = Task.scheduleTaskDelta(200, test2Plugin, 20, [200, '20 seconds'], taskId, self.getPluginId())
        taskManager.addTask(test2Task6)
    
    def terminate(self, taskId, taskManager, taskParameters):
        pass

    def expired(self, taskManager, taskParameters):
        pass

    def test(self, taskId):
        pass