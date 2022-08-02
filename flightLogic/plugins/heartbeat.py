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
    def start(self, taskId, taskManager, taskParameters):
        heartbeatSetting = taskParameters[0]

        heartbeatSettingName = "low"
        if heartbeatSetting:
            heartbeatSettingName = "high"
        
        Log.newInfo(f'Toggle heartbeat {heartbeatSettingName}', taskId, self.getPluginId())

        from objects.task import Task
        
        heartbeatTask = Task.scheduleTaskDelta(10, self, 4, [(not heartbeatSetting)], taskId, self.getPluginId(), expirationDelta=4, shouldImportOnStart=False)

        taskManager.addTask(heartbeatTask)
    
    def terminate(self, taskId, taskManager, taskParameters):
        pass

    def expired(self, taskManager, taskParameters):
        pass