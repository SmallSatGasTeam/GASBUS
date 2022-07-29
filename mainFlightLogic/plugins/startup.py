'''
This is the "startup" plugin.

The startup plugin is run when the satellite starts up. It is the first task and schedules all the other tasks that should run immediately after the satellite starts.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Startup(Plugin):
    def __init__(self, pluginId, identifier, pluginParameters):
        super().__init__(pluginId, identifier)
        self.__taskManager = pluginParameters[0]

    @classmethod
    def newPlugin(cls, taskManager, runTaskId, runPluginId):
        return super().newPlugin(cls, 'startup', [taskManager], runTaskId, runPluginId)

    '''
    ----------------------------------------------------------------------------
    Plugin methods

    These methods are used to perform the plugin's functionality.
    ----------------------------------------------------------------------------

    public start()

    This method is used to start the plugin.
    '''
    def start(self, taskId, taskParameters):
        Log.newLog("Startup plugin started", taskId, self.getPluginId(), 100)

        from objects.task import Task
        from plugins.test1 import Test1
        test1Plugin = Test1.newPlugin(taskId, self.getPluginId())

        from objects.task import Task
        from model import Model
        test1Task = Task.newTaskFromPlugin(100, test1Plugin, -1, -1, Model.createTimeStamp(), -1, -1, -1, True, taskId, self.getPluginId())

        self.__taskManager.addTask(test1Task)
    
    def terminate(self, taskId):
        pass