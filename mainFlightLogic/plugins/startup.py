'''
This is the "startup" plugin.

The startup plugin is run when the satellite starts up. It is the first task and schedules all the other tasks that should run immediately after the satellite starts.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Startup(Plugin):
    def __init__(self, pluginId, fileName, className):
        super().__init__(pluginId, fileName, className, self)

    @classmethod
    def newPlugin(cls, runTaskId, runPluginId):
        return super().newPlugin(cls, 'startup', 'Startup', runTaskId, runPluginId)

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
        test1Task = Task.newTaskFromPlugin(100, test1Plugin, -1, -1, Model.createTimeStamp(), -1, -1, -1, True, taskId, self.getPluginId())

        taskManager.addTask(test1Task)

        from plugins.heartbeat import Heartbeat
        heartbeatPlugin = Heartbeat.newPlugin(taskId, self.getPluginId())
        heartbeatTask = Task.newTaskFromPlugin(10, heartbeatPlugin, -1, -1, Model.createTimeStamp(), Model.createTimeStamp(), -1, -1, True, taskId, self.getPluginId())

        taskManager.addTask(heartbeatTask)

        from plugins.test2 import Test2
        test2Plugin = Test2.newPlugin(taskId, self.getPluginId())
        test2Task = Task.newTaskFromPlugin(200, test2Plugin, -1, -1, Model.createTimeStamp(), -1, -1, -1, True, taskId, self.getPluginId())

        taskManager.addTask(test2Task)
    
    def terminate(self, taskId):
        pass