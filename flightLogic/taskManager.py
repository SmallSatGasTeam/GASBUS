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
        Log.newDebug('TaskManager initialized... startup begins', 0, 0)
        Log.newDebug('Importing active tasks from model', 0, 0)

        activeTasks = Model.retrieveTasksByActive(True, 0, 0)

        self.__firstPriorityTask = None
        self.__firstScheduledTask = None

        Log.newDebug('Adding active tasks that should be imported to the task queues', 0, 0)

        for task in activeTasks:
            Log.newDebug(f'Analyzing {repr(task)} for addition to the task queues', 0, 0)
            if task.getShouldImportOnStart():
                Log.newDebug(f'Adding {repr(task)} to the task queues', 0, 0)
                task.setNextTask(None, 0, 0)
                task.setPreviousTask(None, 0, 0)
                self.addTask(task)
            else:
                Log.newDebug(f'Setting {repr(task)} to inactive', 0, 0)
                task.setActive(False, 0, 0)

        from plugins.startup import Startup
        from objects.task import Task

        Log.newDebug('Initializing startup plugin and task... setting to first priority task', 0, 0)
        
        startupPlugin = Startup.newPlugin(0, 0)
        startupTask = Task.priorityTask(0, startupPlugin, [], 0, 0)

        if self.__firstPriorityTask is not None:
            startupTask.setNextTask(self.__firstPriorityTask, 0, 0)

        self.__firstPriorityTask = startupTask

        Log.newDebug('Running tasks', 0, 0)

        self.__runTasks()

    '''
    private runTasks()

    This method is used to run the tasks in the queue.
    '''
    def __runTasks(self):
        latestTimeStamp = 0
        while True:
            if Model.createTimeStamp() > latestTimeStamp:
                latestTimeStamp = Model.createTimeStamp()
                Log.newDebug(f'Looking for all tasks scheduled to run at {Model.getDateTime(latestTimeStamp)}', 0, 0)
                if self.__firstPriorityTask is not None:
                    self.__recursiveExpirationTimeCheck(None, self.__firstPriorityTask, latestTimeStamp)

            if self.__firstScheduledTask is not None and self.__firstScheduledTask.getScheduledRunTime() <= Model.createTimeStamp():
                Log.newDebug(f'Scheduled tasks being added to the priority queue', 0, 0)
                scheduledTask = self.__firstScheduledTask
                self.__firstScheduledTask = scheduledTask.getNextTask()
                if self.__firstScheduledTask is not None:
                    self.__firstScheduledTask.setPreviousTask(None, 0, 0)

                scheduledTask.setNextTask(None, 0, 0)
                scheduledTask.setPreviousTask(None, 0, 0)
                self.__addTaskToPriorityQueue(scheduledTask)

                Log.newDebug(f'Added scheduled task {repr(scheduledTask)} to the priority queue', 0, 0)
            else:
                task = self.__firstPriorityTask
                if task is not None:
                    Log.newDebug(f'Running first task from priority queue.', 0, 0)
                    self.__firstPriorityTask = task.getNextTask()
                    Log.newDebug(f'Running task {repr(task)}', 0, 0)
                    task.start(self)
    
    '''
    private __recursiveExpirationTimeCheck(task: task, latestTimeStamp: integer):

    This method is used to check if each task in the priority queue has passed its time sensitivity time.
    '''
    def __recursiveExpirationTimeCheck(self, previousTask, task, latestTimeStamp):
        Log.newDebug(f'Checking {repr(task)} for expiration', 0, 0)
        if (task.getExpirationTime() != -1) and (task.getExpirationTime() <= latestTimeStamp):
            Log.newDebug(f'Task {repr(task)} expired... removing from priority queue', 0, 0)
            if task == self.__firstPriorityTask:
                self.__firstPriorityTask = task.getNextTask()
            else:
                if previousTask is not None:
                    previousTask.setNextTask(task.getNextTask(), 0, 0)

            if task.getNextTask() is not None:
                task.getNextTask().setPreviousTask(previousTask, 0, 0)
            
            Log.newDebug(f'Calling {repr(task)} expired function', 0, 0)
            task.expired(self)
        
        if task.getNextTask() is not None:
            self.__recursiveExpirationTimeCheck(task, task.getNextTask(), latestTimeStamp)

    '''
    public addTask(task: Task)

    This method is used to add a task to either the priority or scheduled queue.
    '''
    def addTask(self, task):
        Log.newDebug(f'Adding {repr(task)} to the task queues... checking if scheduled for the future', 0, 0)
        if task.getScheduledRunTime() <= Model.createTimeStamp():
            Log.newDebug(f'Adding {repr(task)} to the priority queue', 0, 0)
            self.__addTaskToPriorityQueue(task)
        else:
            Log.newDebug(f'Adding {repr(task)} to the scheduled queue', 0, 0)
            self.__addTaskToScheduledQueue(task)
    
    '''
    private __addTaskToPriorityQueue(task: Task)

    This method is used to add a task to the priority queue.
    ''' 
    def __addTaskToPriorityQueue(self, task):
        Log.newDebug(f'Adding {repr(task)} to the priority queue... finding where to add', 0, 0)
        if self.__firstPriorityTask is None:
            Log.newDebug(f'Adding {repr(task)} to the priority queue... setting as first priority task', 0, 0)
            self.__firstPriorityTask = task
        # check if the new task is higher priority
        elif task.getPriority() < self.__firstPriorityTask.getPriority():
            Log.newDebug(f'Adding {repr(task)} to the priority queue... setting as first priority task, moving others back', 0, 0)
            task.setNextTask(self.__firstPriorityTask, 0, 0)
            self.__firstPriorityTask = task
        else:
            Log.newDebug(f'Adding {repr(task)} to the priority queue... looking after the first task', 0, 0)
            currentTask = self.__firstPriorityTask.getNextTask()
            if currentTask is None:
                Log.newDebug(f'Adding {repr(task)} to the priority queue... setting as second priority task', 0, 0)
                self.__firstPriorityTask.setNextTask(task, 0, 0)
                task.setPreviousTask(self.__firstPriorityTask, 0, 0)
            else:
                Log.newDebug(f'Adding {repr(task)} to the priority queue... running recursive function to find correct location', 0, 0)
                self.__recursivePriorityAdd(self.__firstPriorityTask, currentTask, task)

    '''
    private ___recursivePriorityAdd(previousTask: Task, task: Task)

    This method is used to recursively search for the correct position to add a task to the priority queue.
    '''
    def __recursivePriorityAdd(self, previousTask, currentTask, task):
        Log.newDebug(f'Recursively adding {repr(task)} to the priority queue... checking if {repr(currentTask)} is the correct location', 0, 0)
        if task.getPriority() < currentTask.getPriority():
            Log.newDebug(f'Recursively adding {repr(task)} to the priority queue... setting as previous task', 0, 0)
            task.setNextTask(currentTask, 0, 0)
            previousTask.setNextTask(task, 0, 0)
            currentTask.setPreviousTask(task, 0, 0)
            task.setPreviousTask(previousTask, 0, 0)
        elif currentTask.getNextTask() is None:
            Log.newDebug(f'Recursively adding {repr(task)} to the priority queue... setting as next task', 0, 0)
            currentTask.setNextTask(task, 0, 0)
            task.setPreviousTask(currentTask, 0, 0)
        else:
            Log.newDebug(f'Recursively adding {repr(task)} to the priority queue... running recursive function to find correct location', 0, 0)
            self.__recursivePriorityAdd(currentTask, currentTask.getNextTask(), task)

    '''
    private __addTaskToScheduledQueue(task: Task)

    This method is used to add a task to the scheduled queue.
    '''
    def __addTaskToScheduledQueue(self, task):
        Log.newDebug(f'Adding {repr(task)} to the scheduled queue... finding where to add', 0, 0)
        if self.__firstScheduledTask is None:
            Log.newDebug(f'Adding {repr(task)} to the scheduled queue... setting as first scheduled task', 0, 0)
            self.__firstScheduledTask = task
        elif task.getScheduledRunTime() < self.__firstScheduledTask.getScheduledRunTime():
            Log.newDebug(f'Adding {repr(task)} to the scheduled queue... setting as first scheduled task, moving others back', 0, 0)
            task.setNextTask(self.__firstScheduledTask, 0, 0)
            self.__firstScheduledTask = task
        else:
            Log.newDebug(f'Adding {repr(task)} to the scheduled queue... looking after the first task', 0, 0)
            currentTask = self.__firstScheduledTask.getNextTask()
            if currentTask is None:
                Log.newDebug(f'Adding {repr(task)} to the scheduled queue... setting as second scheduled task', 0, 0)
                self.__firstScheduledTask.setNextTask(task, 0, 0)
                task.setPreviousTask(self.__firstScheduledTask, 0, 0)
            else:
                Log.newDebug(f'Adding {repr(task)} to the scheduled queue... running recursive function to find correct location', 0, 0)
                self.__recursiveScheduledAdd(self.__firstScheduledTask, self.__firstScheduledTask.getNextTask(), task)
    
    '''
    private __recursiveScheduledAdd(previousTask: Task, task: Task)

    This method is used to recursively search for the correct position to add a task to the scheduled queue.
    '''
    def __recursiveScheduledAdd(self, previousTask, currentTask, task):
        Log.newDebug(f'Recursively adding {repr(task)} to the scheduled queue... checking if {repr(currentTask)} is the correct location', 0, 0)
        if task.getScheduledRunTime() < currentTask.getScheduledRunTime():
            Log.newDebug(f'Recursively adding {repr(task)} to the scheduled queue... setting as previous task', 0, 0)
            previousTask.setNextTask(task, 0, 0)
            currentTask.setPreviousTask(task, 0, 0)
            task.setNextTask(currentTask, 0, 0)
            task.setPreviousTask(previousTask, 0, 0)
        elif currentTask.getNextTask() is None:
            Log.newDebug(f'Recursively adding {repr(task)} to the scheduled queue... setting as next task', 0, 0)
            currentTask.setNextTask(task, 0, 0)
            task.setPreviousTask(currentTask, 0, 0)
        else:
            Log.newDebug(f'Recursively adding {repr(task)} to the scheduled queue... running recursive function to find correct location', 0, 0)
            self.__recursiveScheduledAdd(currentTask, currentTask.getNextTask(), task)

if __name__ == "__main__":
    # During testing, calling this task from the command line will create the task manager.
    taskManager = TaskManager()
