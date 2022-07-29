'''
This is the abstract "plugin" object.

The plugin object requires an identifier. The plugin object also includes a pluginId that is assigned by the database. The identifier is a human understandable identifier for reporting purposes and to help make code using the plugin more readable.

pluginId is an integer available for getting.
identifier is a string available for getting.
'''

from objects.log import Log

class Plugin:
    # class variables
    plugins = [] # a list of all instantiated plugins

    '''
    ----------------------------------------------------------------------------
    Constructors

    These methods are used to instantiate new plugins.
    ----------------------------------------------------------------------------

    default constructor - never use this outside of the class, use the class methods instead
    '''
    def __init__(self, pluginId, identifier):
        self.__pluginId = pluginId
        self.__identifier = identifier

        Plugin.plugins.append(self)

    '''
    public Plugin.newPlugin(identifier: string) -> Plugin

    This is used to create the class method for creating a new plugin.
    '''
    def newPlugin(cls, identifier, pluginParameters, runTaskId, runPluginId):
        from model import Model # import statement here to avoid circular import
        pluginId = Model.retrievePluginByIdentifier(identifier, runTaskId, runPluginId)

        if not pluginId:
            pluginId = Model.createPlugin(identifier, runTaskId, runPluginId)

        Log.newLog(f'{identifier} plugin instantiated as plugin {pluginId}', runTaskId, runPluginId, 100)

        # check if a plugin with the given pluginId already exists to avoid duplicates and synchronization issues
        plugin = Plugin.checkPluginsForId(pluginId)
        if plugin is not None:
            return plugin

        return cls(pluginId, identifier, pluginParameters)

    '''
    public Plugin.pluginWithId(pluginId: integer, identifier: string) -> Plugin

    This is the class method for creating a new plugin object for a plugin that has already been created in the database. If a plugin with the given pluginId already exists, it will be returned instead of creating a new plugin object to avoid synchronization issues. Otherwise, a new plugin object will be created.
    '''
    @classmethod
    def pluginWithId(cls, pluginId, identifier):
        # check if a plugin with the given pluginId already exists to avoid duplicates and synchronization issues
        plugin = cls.checkPluginsForId(pluginId)
        if plugin is not None:
            return plugin

        return cls(pluginId, identifier)

    '''
    private static Plugin.checkPluginsForId(pluginId: integer) -> Plugin | None

    Checks to see if a plugin with a given pluginId has already been created. If it has, it will be returned.
    '''
    @staticmethod
    def checkPluginsForId(pluginId):
        for plugin in Plugin.plugins:
            if plugin.getPluginId() == pluginId:
                return plugin
        return None

    '''
    ----------------------------------------------------------------------------
    Getters

    These methods are used to access the values of the plugin object.
    ----------------------------------------------------------------------------
    '''
    def getPluginId(self):
        return self.__pluginId # integer

    def getIdentifier(self):
        return self.__identifier # string
    
    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the datum object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        return f'Plugin {self.__pluginId} identified as {self.__identifier}'

    # represent function
    def __repr__(self):
        return f'Plugin(pluginId={self.__pluginId}, identifier={self.__identifier})'