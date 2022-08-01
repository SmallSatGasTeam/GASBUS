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
    def start(self, taskId, taskManager, taskParameters):
        Log.newInfo(f'Test 2 plugin started with priority {taskParameters[0]} and run {taskParameters[1]}', taskId, self.getPluginId())
    
    def terminate(self, taskId, taskManager, taskParameters):
        pass
    
    def expired(self, taskManager, taskParameters):
        pass
