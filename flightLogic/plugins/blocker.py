'''
This is the "blocker" plugin.

The blocker plugin is only used for testing and just reschedules itself.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Blocker(Plugin):
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
        from objects.task import Task
        from model import Model
        
        blockerTask = Task.priorityTask(300, self, [], taskId, self.getPluginId(), shouldImportOnStart=False)

        taskManager.addTask(blockerTask)
    
    def terminate(self, taskId, taskManager, taskParameters):
        pass

    def expired(self, taskManager, taskParameters):
        pass

    def test(self, taskId):
        pass