'''
This is the "startupTask" object.

The startup task object is run when the satellite starts up. It is the first task and schedules all the other tasks that should run immediately after the satellite starts.
'''

from mainFlightLogic.tasks.task import Task

class StartupTask(Task):
    pass