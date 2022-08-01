'''
This is the abstract "plugin" object.

The plugin object requires an identifier. The plugin object also includes a pluginId that is assigned by the database. The identifier is the name of the file where the plugin can be found.

pluginId is an integer available for getting.
fileName is a string available for getting.
className is a string available for getting.
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
        Log.newDebug(f'Initializing plugin with id {pluginId}', 0, 0)

        self.__pluginId = pluginId
        self.__fileName = fileName
        self.__className = className

        Plugin.plugins.append(self)

        Log.newDebug(f'{self} initialized', 0, 0)

    '''
    public Plugin.newPlugin(identifier: string) -> Plugin

    This is used to create the class method for creating a new plugin.
    '''
    @classmethod
    def newPlugin(cls, runTaskId, runPluginId):
        Log.newDebug(f'Plugin.newPlugin() called', runTaskId, runPluginId)

        className = cls.__name__
        fileName = className[0].lower() + className[1:]

        Log.newDebug(f'Creating new plugin with class name {className} and file name {fileName}', runTaskId, runPluginId)

        Log.newDebug(f'Checking for plugin with class name {className} and file name {fileName} in the model', runTaskId, runPluginId)
        from model import Model # import statement here to avoid circular import
        plugin = Model.retrievePluginByClassName(className, runTaskId, runPluginId)

        if plugin:
            Log.newDebug(f'Plugin with class name {className} and file name {fileName} found in the model', runTaskId, runPluginId)
            return plugin
        
        pluginId = Model.createPlugin(fileName, className, runTaskId, runPluginId)

        Log.newDebug(f'Creating new plugin with id {pluginId}... checking if plugin with id already exists', runTaskId, runPluginId)
        # check if a plugin with the given pluginId already exists to avoid duplicates and synchronization issues
        plugin = Plugin.checkPluginsForId(pluginId)
        if plugin is not None:
            Log.newDebug(f'Plugin with id {pluginId} already exists... returning', runTaskId, runPluginId)
            return plugin
        
        Log.newDebug(f'Creating new plugin with id {pluginId}', runTaskId, runPluginId)
        return cls(pluginId, fileName, className)

    '''
    public Plugin.pluginFromClassName(className: string) -> Plugin

    This is the class method for instantiating a plugin from a class name.
    '''
    @classmethod
    def pluginFromClassName(cls, className, runTaskId, runPluginId):
        Log.newDebug(f'Plugin.pluginFromClassName() called for className: {className}', runTaskId, runPluginId)
        plugin = cls.checkPluginsForClassName(className)
        if plugin is not None:
            Log.newDebug(f'Plugin with class name {className} already instantiated... returning', runTaskId, runPluginId)
            return plugin

        Log.newDebug(f'Plugin with class name {className} not instantiated... looking in the model', runTaskId, runPluginId)
        from model import Model
        plugin = Model.retrievePluginByClassName(className, runTaskId, runPluginId)
        if plugin:
            Log.newDebug(f'Plugin with class name {className} found in the model... returning', runTaskId, runPluginId)
            return plugin
        
        Log.newDebug(f'Plugin with class name {className} not found in the model... discovering all plugins', runTaskId, runPluginId)
        from plugins.discoverPlugins import DiscoverPlugins
        DiscoverPlugins.discoverPlugins(runTaskId, runPluginId)

        Log.newDebug(f'Checking for plugin with class name {className} in the newly instantiated plugins', runTaskId, runPluginId)
        plugin = cls.checkPluginsForClassName(className)
        if plugin is not None:
            Log.newDebug(f'Plugin with class name {className} found in the newly instantiated plugins... returning', runTaskId, runPluginId)
            return plugin
        
        Log.newError(f'Plugin with class name {className} does not exist', runTaskId, runPluginId)
        return None

    '''
    public Plugin.pluginWithId(pluginId: integer, identifier: string) -> Plugin

    This is the class method for creating a new plugin object for a plugin that has already been created in the database. If a plugin with the given pluginId already exists, it will be returned instead of creating a new plugin object to avoid synchronization issues. Otherwise, a new plugin object will be created.
    '''
    @classmethod
    def pluginWithId(cls, pluginId, fileName, className):
        Log.newDebug(f'Plugin.pluginWithId() called for pluginId: {pluginId}', 0, 0)
        # check if a plugin with the given pluginId already exists to avoid duplicates and synchronization issues
        plugin = cls.checkPluginsForId(pluginId)
        if plugin is not None:
            Log.newDebug(f'Plugin with id {pluginId} already exists... returning', 0, 0)
            return plugin

        Log.newDebug(f'Plugin with id {pluginId} not instantiated... creating new plugin object', 0, 0)
        return cls(pluginId, fileName, className)

    '''
    public static Plugin.checkPluginsForId(pluginId: integer) -> Plugin | None

    Checks to see if a plugin with a given pluginId has already been created. If it has, it will be returned.
    '''
    @staticmethod
    def checkPluginsForId(pluginId):
        for plugin in Plugin.plugins:
            if plugin.getPluginId() == pluginId:
                return plugin
        return None
    
    '''
    public static Plugin.checkPluginsForClassName(className: string) -> Plugin | None

    Checks to see if a plugin with a given classname has already been created. If it has, it will be returned.
    '''
    @staticmethod
    def checkPluginsForClassName(className):
        for plugin in Plugin.plugins:
            if plugin.getClassName() == className:
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
    def start(self, taskId, taskManager, taskParameters):
        Log.newError("No startTask function defined for child task", taskId, self.__pluginId)
    
    '''
    public terminate()

    This method is used to clean up the plugin after execution.
    '''
    def terminate(self, taskId, taskManager, taskParameters):
        Log.newError("No terminate function defined for child task", taskId, self.__pluginId)

    '''
    public timeSensitivityPassed()

    This method is called if the task is removed from the priority queue because it has waited too long to run.
    '''
    def expired(self, taskManager, taskParameters):
        Log.newError("No expired function defined for child task", 0, self.__pluginId)

    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the datum object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        return f'Plugin {self.__pluginId} at {self.__fileName} called {self.__className}'

    # represent function
    def __repr__(self):
        return f'Plugin(pluginId={self.__pluginId}, fileName={self.__fileName}, className={self.__className})'