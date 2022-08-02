# GASBUS

The GASBUS satellite utilizes the Flight Logic software for all operational control. The core component of Flight Logic is a task manager that schedules and prioritizes the tasks that the satellite needs to do.

Each task calls a specific plugin that gives the task its functionality. To add functionality to the satellite, the developer should create a plugin that implements the desired processes. After creating the plugin, a task must be created that calls the new plugin. After adding the task to the task manager, it will be called after all higher priority tasks have been finished.

Tasks can also be scheduled into the future. Task scheduling has a one second tollerance. The scheduled task will be added to the priority queue the first time the task manager runs after the designated run time for the task. Additionally, a scheduled task can have an expiration time that instructs the operating system when to deschedule a task if it hasn't had an opportunity to run. After removing a task that wasn't able to run before expiring, the task manager calls a function in the plugin that allows it to reschedule itself for another time or add itself back to the priority queue with a new priority value.

Flight Logic also includes a model that is in charge of storing and retrieving all data on the satellite. The model operates using structured objects including the datum, log, packet, task, and plugin.

All logging on the satellite should be done using the designated log object. This organizes the log for sending in beacons and when requested for debugging purposes. It also ensures that the log is all stored in the database.

## Things to do

Documentation

- [ ] Add known issues to GitHub
- [ ] Start wiki entries on GitHub

Task Manager

- [ ] Set up constants in model to allow changes in startup plugin

Plugin

- [ ] In all plugins, add more debug logs

Startup

- [ ] Set up constants to change plugin names like heartbeat

Unit Testing

- [ ] Add unit tests to the TaskManager
- [ ] Add unit tests to the Model
- [ ] Add unit tests to the objects
- [ ] Add unit tests to the plugins
