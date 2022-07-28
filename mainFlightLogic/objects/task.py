# TODO: update with new variables

'''
This is the "task" object.

The task object requires a priority and a pluginId. The task object also receives a taskId from the database. The priority tells the task manager how to sort the task in the priority queue. The pluginId is the id of the plugin that the task is associated with.

taskId is an integer available for getting.
priority is an integer available for getting and setting.
pluginId is an integer available for getting.
'''

class Task:
    # class variables
    tasks = [] # a list of all instantiated tasks

    '''
    ----------------------------------------------------------------------------
    Constructors

    These methods are used to instantiate new tasks.
    ----------------------------------------------------------------------------

    default constructor - never use this outside of the class, use the class methods instead
    '''
    def __init__(self, taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active):
        self.__taskId = taskId
        self.__priority = priority
        self.__pluginId = pluginId
        self.__previousTaskId = previousTaskId
        self.__nextTaskId = nextTaskId
        self.__addToQueueTime = addToQueueTime
        self.__scheduledRunTime = scheduledRunTime
        self.__startTime = startTime
        self.__endTime = endTime
        self.__active = active

        Task.tasks.append(self)

    '''
    public Task.newTask(priority: integer, pluginId: integer, previousTaskId: integer, nextTaskId: integer, addToQueueTime: integer, scheduledRunTime: integer, startTime: integer, endTime: integer, active: boolean, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for creating a new task.
    '''
    @classmethod
    def newTask(cls, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active, runTaskId, runPluginId):
        from model import Model # import statement here to avoid circular import
        taskId = Model.createTask(priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active, runTaskId, runPluginId)

        return cls(taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active)
    
    '''
    public Task.taskWithId(taskId: integer, priority: integer, pluginId: integer, previousTaskId: integer, nextTaskId: integer, addToQueueTime: integer, scheduledRunTime: integer, startTime: integer, endTime: integer, active: boolean, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for creating a new task object for a task that has already been created in the database. If a task with the given taskId already exists, it will be returned instead of creating a new one to avoid synchronization issues. Otherwise, a new task will be created.
    '''
    @classmethod
    def taskWithId(cls, taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active, runTaskId, runPluginId):
        # check if a task with the given taskId already exists to avoid duplicates and synchronization issues
        task = cls.__checkTasksForId(taskId)
        if task is not None:
            return task

        return cls.newTask(priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active, runTaskId, runPluginId)

    '''
    private static Task.__checkTasksForId(taskId: integer) -> Task | None

    Checks to see if a task with the given taskId has already been created. If it has, it will be returned.
    '''
    @staticmethod
    def __checkTasksForId(taskId):
        for task in Task.tasks:
            if task.getTaskId() == taskId:
                return task
        return None

    '''
    ----------------------------------------------------------------------------
    Getters

    These methods are used to access the values of the task object.
    ----------------------------------------------------------------------------
    '''
    def getTaskId(self):
        return self.__taskId # integer
    
    def getPriority(self):
        return self.__priority # integer

    def getPluginId(self):
        return self.__pluginId # integer
    
    def getPreviousTaskId(self):
        return self.__previousTaskId # integer
    
    def getNextTaskId(self):
        return self.__nextTaskId # integer
    
    def getAddToQueueTime(self):
        return self.__addToQueueTime # integer

    def getScheduledRunTime(self):
        return self.__scheduledRunTime # integer
    
    def getStartTime(self):
        return self.__startTime # integer
    
    def getEndTime(self):
        return self.__endTime # integer
    
    def getActive(self):
        return self.__active # boolean

    '''
    ----------------------------------------------------------------------------
    Setters
    
    These methods are used to set the values of the task object.
    ----------------------------------------------------------------------------
    '''
    def setPriority(self, priority, runTaskId, runPluginId):
        # update the priority in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskPriority(self.__taskId, priority, runTaskId, runPluginId):
            self.__priority = priority
            return True

            # TODO: adjust priority queue

        return False

    def setPreviousTaskId(self, previousTaskId, runTaskId, runPluginId):
        # update the previousTaskId in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskPreviousTaskId(self.__taskId, previousTaskId, runTaskId, runPluginId):
            self.__previousTaskId = previousTaskId
            return True
        
        return False
    
    def setNextTaskId(self, nextTaskId, runTaskId, runPluginId):
        # update the nextTaskId in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskNextTaskId(self.__taskId, nextTaskId, runTaskId, runPluginId):
            self.__nextTaskId = nextTaskId
            return True
    
    def setScheduledRunTime(self, scheduledRunTime, runTaskId, runPluginId):
        # update the scheduledRunTime in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskScheduledRunTime(self.__taskId, scheduledRunTime, runTaskId, runPluginId):
            self.__scheduledRunTime = scheduledRunTime
            return True

        return False

    def setStartTime(self, startTime, runTaskId, runPluginId):
        # update the startTime in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskStartTime(self.__taskId, startTime, runTaskId, runPluginId):
            self.__startTime = startTime
            return True

        return False
    
    def setEndTime(self, endTime, runTaskId, runPluginId):
        # update the endTime in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskEndTime(self.__taskId, endTime, runTaskId, runPluginId):
            self.__endTime = endTime
            return True
        
        return False
    
    def setActive(self, active, runTaskId, runPluginId):
        # update the active in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskActive(self.__taskId, active, runTaskId, runPluginId):
            self.__active = active
            return True

        return False
    
    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the task object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        # TODO: update with new variables

        return f'Task {self.__taskId} with priority {self.__priority} runs plugin {self.__pluginId}'

    # represent function
    def __repr__(self):
        # TODO: update with new variables

        return f'Task(taskId={self.__taskId}, priority={self.__priority}, pluginId={self.__pluginId})'
