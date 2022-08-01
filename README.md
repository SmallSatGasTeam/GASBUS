# Main Flight Logic

Flight Logic is the software that operates the GASBUS satellite. The core component of Flight Logic is a task manager that schedules and prioritizes the tasks that the satellite needs to do.

Each task calls a specific plugin that gives the task its functionality. To add functionality to the satellite, the developer should create a plugin that implements the desired processes. After creating the plugin, a task must be created that calls the new plugin. After adding the task to the task manager, it will be called after all higher priority tasks have been finished.

Tasks can also be scheduled into the future. Task scheduling has a one second tollerance. The scheduled task will be added to the priority queue the first time the task manager runs after the designated run time for the task. Additionally, a scheduled task can have a time sensitivity value that instructs the operating system how long to wait before descheduling a task. After removing a task that wasn't able to run within its time sensitivity time frame, the task manager calls a function in the plugin that allows it to reschedule itself for another time or add itself back to the priority queue with a new priority value.

Flight Logic also includes a model that is in charge of storing and retrieving all data on the satellite. The model operates using structured objects including the datum, log, packet, task, and plugin.

All logging on the satellite should be done using the designated log object. This organizes the log for sending in beacons and when requested for debugging purposes. It also ensures that the log is all stored in the database.

## Usage

Just call the taskManager.py from the command line.

After doing that:

- The task manager will create the priority and scheduled task queues
- The model will create the database (if necessary) and prepare it for storing data
- The task manager will schedule a task implementing the startup plugin
- The discoverPlugins will run logging all plugins into the database for further use
- The startup plugin will call all other plugins that should be performed on startup
- The startup plugin will start the heartbeat

## Plugins and Tasks

The primary unit that provides functionality is the plugin. Plugins aren't called directly, but rather are encapsulated in tasks and then scheduled in the task manager. The reason for this is to allow the tasks to implement all of the functionality related to scheduling and for the plugin to focus primarily on the unique functionality for which the plugin is created.

The process for creating a new plugin is simple:

    from plugins.plugin import Plugin
    newPlugin = Plugin.pluginFromClassName("[name of plugin]", runningTaskId, runningPluginId)

If the desired plugin hasn't already been instantiated, this will call the discoverPlugins function to find and instantiate it. The proper plugin child class will then be returned.

After creating the plugin object, to schedule the plugin, it must be encapsulated within a task. There are three ways to do this.

1.  Add the task directly to the priority queue.

        from objects.task import Task
        newTask = Task.priorityTask(priority, newPlugin, pluginParameters, runningTaskId, runningPluginId)

2.  Schedule the task for a certain number of seconds (called the delta) in the future compared to the current time.

        from objects.task import Task
        newTask = Task.scheduleTaskDelta(priority, newPlugin, delta, timeSensitivity, pluginParameters, runningTaskId, runningPluginId)

3.  Schedule the task for a specific date and time in the future.

        from objects.task import Task
        newTask = Task.scheduleTaskTimeStamp(priority, newPlugin, scheduledRunTime, timeSensitivity, pluginParameters, runningTaskId, runningPluginId)

After creating a task, it must then be added to the task manager. The task manager should be passed to each plugin. Add the task passing the new task to the addTask() function.

    taskManager.addTask(newTask)

The task will now run after its scheduled time after all higher priority tasks have run.

## Things to do

Overall

- [ ] Create test cases to describe edge events and ascertain functionality

Documentation

- [x] Document the usage of plugins and tasks
- [ ] Revamp function comments and statements comments
- [ ] README.md files in other directories
- [ ] Add known issues to GitHub
- [ ] Start wiki entries on GitHub
- [ ] Describe naming conventions of tasks and plugins
- [ ] Update README.md to include the new task call structure

Task Manager

- [x] Set up the functionality for time sensitivity
- [x] Import active tasks on startup from database
- [x] Rename timeSensitivity to expirationTime
- [ ] Add more debug logs

Task

- [x] Set start and end times for task run
- [x] Add field shouldImportOnStartup for if the task should be imported if still active in the database on startup
- [ ] Redo visual functions for tasks
- [x] Rename timeSensitivity to expirationTime
- [ ] Add more debug logs
- [ ] Ability to add task with expirationTime expressed as delta from scheduledRunTime (can be implemented as extra optional parameter)
- [ ] Set up task parameters

Plugin

- [x] Add timeSensitivityPassed() to structure
- [ ] Add test functionality to run on initial import
- [ ] Redo visual functions for plugins
- [x] Rename timeSensitivityPassed to expired
- [ ] In all plugins, add more debug logs
- [ ] Set up task parameters

DiscoverPlugins

- [ ] Run the test function on each new plugin

Log

- [x] Create functions for Log.newErrorLog(), Log.newWarningLog(), Log.newInfoLog(), Log.newDebugLog()
- [x] Set specific log levels for error, warning, info, and debug

Unit Testing

- [ ] Add unit tests to the TaskManager
- [ ] Add unit tests to the Model
- [ ] Add unit tests to the objects
- [ ] Add unit tests to the plugins
