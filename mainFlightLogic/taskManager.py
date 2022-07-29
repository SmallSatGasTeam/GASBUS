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
        from plugins.startup import Startup
        from objects.task import Task

        startupPlugin = Startup.newPlugin(0, 0)
        startupTask = Task.newTaskFromPlugin(0, startupPlugin, -1, -1, Model.createTimeStamp(), -1, -1, -1, True, 0, 0)
        self.__firstPriorityTask = startupTask
        self.__firstScheduledTask = None

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
        while True:
            if self.__firstScheduledTask is not None and self.__firstScheduledTask.getScheduledRunTime() <= Model.createTimeStamp():
                scheduledTask = self.__firstScheduledTask
                self.__firstScheduledTask = scheduledTask.getNextTask()
                self.__addTaskToPriorityQueue(scheduledTask)
            
            task = self.__firstPriorityTask
            if task is not None:
                self.__firstPriorityTask = task.getNextTask()
                task.start(self)

    '''
    public addTask(task: Task)

    This method is used to add a task to either the priority or scheduled queue.
    '''
    def addTask(self, task):
        if task.getScheduledRunTime() < Model.createTimeStamp():
            self.__addTaskToPriorityQueue(task)

        else:
            self.__addTaskToScheduledQueue(task)
            pass
    
    def __addTaskToPriorityQueue(self, task):
        if self.__firstPriorityTask is None:
            self.__firstPriorityTask = task
        # check if the new task is higher priority
        elif task.getPriority() < self.__firstPriorityTask.getPriority():
            task.setNextTask(self.__firstPriorityTask)
            self.__firstPriorityTask = task
        else:
            # TODO position the task in the priority queue
            pass
    
    def __addTaskToScheduledQueue(self, task):
        if self.__firstScheduledTask is None:
            self.__firstScheduledTask = task
        elif task.getScheduledRunTime() < self.__firstScheduledTask.getScheduledRunTime():
            task.setNextTask(self.__firstScheduledTask)
            self.__firstScheduledTask = task
        else:
            # TODO: position the task in the scheduled queue
            pass

if __name__ == "__main__":
    # During testing, calling this task from the command line will create the task manager.
    taskManager = TaskManager()
