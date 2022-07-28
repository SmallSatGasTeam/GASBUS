'''
This is the "taskManager" module.

The task manager module contains the queue of tasks to be executed and keeps track of all the tasks that have been scheduled. Once a task has reached its scheduled run time, the task manager will add it to the queue. The task manager also is in charge of keeping the tasks in the queue in order of priority and keeping that order up to date as priorities may change.
'''

class TaskManager:
    # class variables
    taskQueue = [] # a list of all instantiated logs

    '''
    ----------------------------------------------------------------------------
    Constructor

    This method is used to instantiate a new task manager.
    ----------------------------------------------------------------------------

    default constructor
    '''

    def __init__(self):
        pass