'''
This is the abstract "plugin" object.

The plugin object requires an identifier. The plugin object also includes a pluginId that is assigned by the database. The identifier is the name of the file where the plugin can be found.

pluginId is an integer available for getting.
identifier is a string available for getting.
TODO: add fileName and className
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
    def __init__(self, pluginId, fileName, className):
        self.__pluginId = pluginId
        self.__fileName = fileName
        self.__className = className

        Plugin.plugins.append(self)

    '''
    public Plugin.newPlugin(identifier: string) -> Plugin

    This is used to create the class method for creating a new plugin.
    '''
    @classmethod
    def newPlugin(cls, runTaskId, runPluginId):
        className = cls.__name__
        fileName = className[0].lower() + className[1:]

        from model import Model # import statement here to avoid circular import
        plugin = Model.retrievePluginByClassName(className, runTaskId, runPluginId)

        if plugin:
            return plugin
        
        pluginId = Model.createPlugin(fileName, className, runTaskId, runPluginId)

        # check if a plugin with the given pluginId already exists to avoid duplicates and synchronization issues
        plugin = Plugin.checkPluginsForId(pluginId)
        if plugin is not None:
            return plugin

        return cls(pluginId, fileName, className)

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

    def getFileName(self):
        return self.__fileName # string

    def getClassName(self):
        return self.__className # string

    '''
    ----------------------------------------------------------------------------
    Plugin methods

    These methods are used to perform the plugin's functionality.
    ----------------------------------------------------------------------------

    public start()

    This method is used to start the plugin.
    '''
    def start(self):
        raise Exception("No startTask function defined for child task")
    
    '''
    public terminate()

    This method is used to clean up the plugin after execution.
    '''
    def terminate(self):
        raise Exception("No terminate function defined for child task")

    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the datum object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        # TODO: add fileName and className
        return f'Plugin {self.__pluginId}'

    # represent function
    def __repr__(self):
        # TODO: add fileName and className
        return f'Plugin(pluginId={self.__pluginId})'