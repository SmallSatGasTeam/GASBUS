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
        Log.newInfo("Startup plugin started", taskId, self.getPluginId())

        # Adding tasks for testing purposes

        test1Plugin = Plugin.pluginFromClassName("Test1", taskId, self.getPluginId())

        from objects.task import Task
        from model import Model
        test1Task = Task.priorityTask(100, test1Plugin, [], taskId, self.getPluginId())

        taskManager.addTask(test1Task)

        test2Plugin = Plugin.pluginFromClassName("Test2", taskId, self.getPluginId())
        test2Task = Task.priorityTask(200, test2Plugin, [], taskId, self.getPluginId())

        taskManager.addTask(test2Task)

        # Setting up the heartbeat

        heartbeatPlugin = Plugin.pluginFromClassName("Heartbeat", taskId, self.getPluginId())
        heartbeatTask = Task.priorityTask(10, heartbeatPlugin, [], taskId, self.getPluginId())

        taskManager.addTask(heartbeatTask)

        # Testing the time sensitivity using the blocker plugin

        # blockerPlugin = Plugin.pluginFromClassName("Blocker", taskId, self.getPluginId())
        # blockerTask = Task.priorityTask(300, blockerPlugin, [], taskId, self.getPluginId(), shouldImportOnStart=False)

        # taskManager.addTask(blockerTask)

        # test3Plugin = Plugin.pluginFromClassName("Test3", taskId, self.getPluginId())
        # test3Task = Task.scheduleTaskDelta(400, test3Plugin, 1, 1, [], taskId, self.getPluginId(), shouldImportOnStart=False)
        # taskManager.addTask(test3Task)
    
    def terminate(self, taskId):
        pass