'''
This is the "heartbeat" plugin.

The heartbeat plugin runs every 4 seconds and toggles the hearbeat pin from high to low.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Heartbeat(Plugin):
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
        Log.newLog("Toggle heartbeat", taskId, self.getPluginId(), 100)

        from objects.task import Task
        from model import Model
        newHeartbeatTask = Task.newTaskFromPlugin(10, self, -1, -1, Model.createTimeStamp(), Model.createTimeStamp() + 4, -1, -1, True, taskId, self.getPluginId())

        taskManager.addTask(newHeartbeatTask)
    
    def terminate(self, taskId):
        pass