'''
This is the "discoverPlugins" plugin.

The discover plugins plugin goes through the plugins folder and looks for any new plugins that have been added. It then 
'''

from plugins.plugin import Plugin
from objects.log import Log

class DiscoverPlugins(Plugin):
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
        Log.newInfo("Discover task plugin started", taskId, self.getPluginId())
        self.discoverPlugins(taskId, self.getPluginId())
    
    def terminate(self, taskId):
        pass

    '''
    public static discoverPlugins(self, taskId, pluginId)

    This method is used to discover new plugins, add them to the database, and instantiate them.
    '''
    @staticmethod
    def discoverPlugins(taskId, pluginId):
        import os
        noImport = ['discoverPlugins.py', 'plugin.py']
        for module in os.listdir(os.path.dirname(__file__)):
            if not((module in noImport) or module[-3:] != '.py'):
                fileName = module[0:-3]
                className = module[0].upper() + module[1:-3]

                from model import Model
                Model.retrieveOrCreatePlugin(fileName, className, taskId, pluginId)