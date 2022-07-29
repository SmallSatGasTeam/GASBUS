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
    
    def terminate(self, taskId):
        pass