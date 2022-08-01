'''
This is the "test2" plugin.

The test2 plugin is only for testing and logs that it has run.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Test2(Plugin):
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
        Log.newInfo("Test 2 plugin started", taskId, self.getPluginId())
    
    def terminate(self, taskId):
        pass