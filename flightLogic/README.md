# Flight Logic

Flight logic is the software that runs on the GASBUS satellite.

## Task Manager

The task manager is in charge of scheduling and running tasks. It is constantly running. All functionality of the satellite is organized into tasks which are then prioritized and scheduled through the task manager.

### Usage

To start the task manager, just call the taskManager.py from the command line.

    python3 taskManager.py

After doing that:

- The task manager will create the priority and scheduled task queues
- The model will create the database (if necessary) and prepare it for storing data
- The task manager will schedule a task implementing the startup plugin
- The discoverPlugins will run logging all plugins into the database for further use
- The startup plugin will call all other plugins that should be performed on startup
- The startup plugin will start the heartbeat

### Creating Plugins and Tasks

The primary unit that provides functionality is the plugin. Plugins aren't called directly, but rather are encapsulated in tasks and then scheduled in the task manager. The reason for this is to allow the tasks to implement all of the functionality related to scheduling and for the plugin to focus primarily on the unique functionality for which the plugin is created.

For information on creating plugins, see the [Plugins README](plugins/README.md#creating-a-new-plugin).

The process for instantiating a new plugin is simple:

    from plugins.plugin import Plugin
    newPlugin = Plugin.pluginFromClassName("[name of plugin]", runningTaskId, runningPluginId)

If the desired plugin hasn't already been instantiated, this will call the discoverPlugins function to find and instantiate it. The proper plugin child class will then be returned.

After creating the plugin object, to schedule the plugin, it must be encapsulated within a task. There are three ways to do this.

1.  Add the task directly to the priority queue.

        from objects.task import Task
        newTask = Task.priorityTask(priority, newPlugin, pluginParameters, runningTaskId, runningPluginId, ?expirationTime, ?expirationDelta, ?shouldImportOnStartup)

2.  Schedule the task for a certain number of seconds (called the delta) in the future compared to the current time.

        from objects.task import Task
        newTask = Task.scheduleTaskDelta(priority, newPlugin, delta, pluginParameters, runningTaskId, runningPluginId, ?expirationTime, ?expirationDelta, ?shouldImportOnStartup)

3.  Schedule the task for a specific date and time in the future.

        from objects.task import Task
        newTask = Task.scheduleTaskTimeStamp(priority, newPlugin, scheduledRunTime, pluginParameters, runningTaskId, runningPluginId, ?expirationTime, ?expirationDelta, ?shouldImportOnStartup)

After creating a task, it must then be added to the task manager. The task manager should be passed to each plugin. Add the task passing the new task to the addTask() function.

    taskManager.addTask(newTask)

The task will now run after its scheduled time after all higher priority tasks have run.

## Model

The model is Flight Logic's connection to all persistent data. It is responsible for creating and maintaining the database. The model class contains only static methods and is not meant to be instantiated.

### Usage

To use the model, import it and then call the method that accomplishes the desired function.

    from model import Model
    Model.createTask(priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, runTaskId, runPluginId)

Generally, there are three types of methods in the model.

1.  Methods that create a record in the database.

        from model import Model
        Model.createPacket(data, sendTime, runTaskId, runPluginId)

2.  Methods that retrieve a record from the database.

        from model import Model
        Model.retrievePacketById(packetId, runTaskId, runPluginId)

3.  Methods that update a record in the database.

        from model import Model
        Model.updatePacketSendTime(packetId, sendTime, runTaskId, runPluginId)
