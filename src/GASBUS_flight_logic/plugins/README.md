# Plugins

The plugin is the basic unit of functionality in Flight Logic. Any functionality that is implemented on the satellite unique to this specific satellite should be encapsulated within a plugin.

For information on the relationship between tasks and plugins and how to instantiate an instance of a plugin, see the [Flight Logic README](../README.md#plugins-and-tasks).

## Creating a new Plugin

When naming your plugin, the only requirement is that the name of the file with the plugin is the same as the class of the plugin, just with a lowercase letter at the front. For example, the "example" plugin would have a file name of "example.py" and the class would be called "Example".

Plugins are easy to create. Here is the basic format.

    '''
    This is the "example" plugin.

    The example plugin is made to be an example of how to create a plugin
    '''

    from plugins.plugin import Plugin
    from objects.log import Log

    class Example(Plugin):
        def __init__(self, pluginId, fileName, className):
            super().__init__(pluginId, fileName, className)

        '''
        ----------------------------------------------------------------------------
        Plugin methods

        These methods are used to perform the plugin's functionality.
        ----------------------------------------------------------------------------

        public start(taskId: integer, taskManager: taskManager, taskParameters: any[])

        This method is used to start the plugin.
        '''
        def start(self, taskId, taskManager, taskParameters):
            pass

        '''
        public terminate(taskId: integer, taskManager: taskManager, taskParameters: any[])

        This method is called when the plugin is being terminated.
        '''
        def terminate(self, taskId, taskManager, taskParameters):
            pass

        '''
        public expired(taskManager: taskManager, taskParameters: any[])

        This method is called if the plugin expires before it has a chance to run.
        '''
        def expired(self, taskManager, taskParameters):
            pass

        '''
        public test(taskId: integer):

        This method is used to test the plugin.
        '''
        def test(self, taskId):
            pass

As we can see, most of the common plugin functionality is inherited from the Plugin class. This means that we can focus on the unique functionality when developing our plugins.

## Plugin Properties

Each plugin has several identifying characteristics that are stored as properties. These help the model and task manager keep track of which plugin is which and when each is running.

**pluginId**: An integer available for getting. The pluginId is a sequentially assigned identification assigned to each plugin when it is first set up in the database.

**fileName**: A string available for getting. The fileName tells the model where to look for the plugin.

**className**: A string available for getting. The className tells the model what class to call when instantiating the plugin.

## Plugin Methods

Along with the getters inherited from the parent plugin class, each plugin is required to implement several plugin methods.

**start(self, taskId, taskManager, taskParameters)**

The start method will be called by the encapsulating task when the plugin is started. This is where the functionality of the plugin should be put.

**terminate(self, taskId, taskManager, taskParameters)**

The terminate method will be called by the encapsulating task when the plugin is being terminated. This is where the plugin should clean itself up if necessary or do any processes that must be done after the main functionality of the plugin has run.

**expired(self, taskManager, taskParameters)**

The expired method will be called by the encapsulating task if the task hits its expiration time before it has an opportunity to run. The expired method could create a new task with higher priority that runs the plugin or it could log the plugins inability to run.
