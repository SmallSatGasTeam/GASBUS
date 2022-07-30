'''
This is the "startup" plugin.

The startup plugin is run when the satellite starts up. It is the first task and schedules all the other tasks that should run immediately after the satellite starts.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Startup(Plugin):
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
        Log.newLog("Startup plugin started", taskId, self.getPluginId(), 100)

        # Adding tasks for testing purposes

        from objects.task import Task
        from plugins.test1 import Test1
        test1Plugin = Test1.newPlugin(taskId, self.getPluginId())

        from objects.task import Task
        from model import Model
        test1Task = Task.priorityTask(100, test1Plugin, [], taskId, self.getPluginId())

        taskManager.addTask(test1Task)

        from plugins.heartbeat import Heartbeat
        heartbeatPlugin = Heartbeat.newPlugin(taskId, self.getPluginId())
        heartbeatTask = Task.priorityTask(10, heartbeatPlugin, [], taskId, self.getPluginId())

        taskManager.addTask(heartbeatTask)

        from plugins.test2 import Test2
        test2Plugin = Test2.newPlugin(taskId, self.getPluginId())
        test2Task = Task.priorityTask(200, test2Plugin, [], taskId, self.getPluginId())

        taskManager.addTask(test2Task)
    
    def terminate(self, taskId):
        pass