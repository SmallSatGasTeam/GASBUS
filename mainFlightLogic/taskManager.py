'''
This is the "taskManager" module.

The task manager module contains the queue of tasks to be executed and keeps track of all the tasks that have been scheduled. Once a task has reached its scheduled run time, the task manager will add it to the queue. The task manager also is in charge of keeping the tasks in the queue in order of priority and keeping that order up to date as priorities may change.
'''

from model import Model
from objects.log import Log

class TaskManager:
    '''
    ----------------------------------------------------------------------------
    Constructor

    This method is used to instantiate a new task manager.
    ----------------------------------------------------------------------------

    default constructor
    '''
    def __init__(self):
        # TODO: create task for startup plugin
        from plugins.startup import Startup
        from objects.task import Task

        startupPlugin = Startup.newPlugin(self, 0, 0)
        startupTask = Task.newTaskFromPlugin(0, startupPlugin, -1, -1, Model.createTimeStamp(), -1, -1, -1, True, 0, 0)
        self.__firstPriorityTask = startupTask

        Log.newLog("Startup task added to priority queue", 0, 0, 100)

        # TODO: get tasks from database
        activeTasks = Model.retrieveTasksByActive(True, 0, 0)

        for task in activeTasks:
            # TODO: put all active unscheduled tasks into priority queue

            # TODO: put all sheduled tasks in queue
            pass

        self.nextTask()

        pass

    '''
    I'm thinking that we pass the task manager into each class and then they perform a callback during the tear down. That would call:

    public nextTask()
    '''

    def nextTask(self):
        # TODO: check current time against the first scheduled task time
            # TODO: if necessary add scheduled tasks to the priority queue
        
        task = self.__firstPriorityTask
        if task is not None:
            self.__firstPriorityTask = task.getNextTask()
            task.start(self)
        else:
            Log.newLog("No tasks to run", 0, 0, 100)
            # TODO: wait or look for scheduled tasks

    '''
    public addTask(task: Task)

    This method is used to add a task to either the priority or scheduled queue.
    '''
    def addTask(self, task):
        if task.getScheduledRunTime() < Model.createTimeStamp():
            self.__addTaskToPriorityQueue(task)

        else:
            # TODO: schedule task
            pass
    
    def __addTaskToPriorityQueue(self, task):
        if self.__firstPriorityTask is None:
            self.__firstPriorityTask = task
        # check if the new task is hig
        elif task.getPriority() < self.__firstPriorityTask.getPriority():
            task.setNextTask(self.__firstPriorityTask)
            self.__firstPriorityTask = task
        else:
            task.setNextTask(self.__firstPriorityTask)
            self.__firstPriorityTask = task
    
if __name__ == "__main__":
    # During testing, calling this task from the command line will create the task manager.
    taskManager = TaskManager()
