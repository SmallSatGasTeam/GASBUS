'''
This is the "task" object.

The task object requires a priority and a pluginId. The task object also receives a taskId from the database. The priority tells the task manager how to sort the task in the priority queue. The pluginId is the id of the plugin that the task is associated with.

taskId is an integer available for getting.
priority is an integer available for getting and setting.
pluginId is an integer available for getting. TODO: move away from using ids on the object
previousTaskId is an integer available for getting and setting. TODO: move away from using ids on the object
nextTaskId is an integer available for getting and setting. TODO: move away from using ids on the object
addToQueueTime is an integer available for getting.
scheduledRunTime is an integer available for getting and setting.
expirationTime is an integer available for getting.
startTime is an integer available for getting and setting.
endTime is an integer available for getting and setting.
active is a boolean available for getting and setting.
shouldImportOnStart is a boolean available for getting.
taskParameters is an array available for getting.
TODO: plugin is a plugin object available for getting.
TODO: previousTask is a task object available for getting and setting.
TODO: nextTask is a task object available for getting and setting.

TODO: add task methods
'''

from objects.log import Log
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
    def __init__(self, taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, plugin):
        Log.newDebug(f'Task initialization for {taskId}', 0, 0)

        self.__taskId = taskId
        self.__priority = priority
        self.__pluginId = pluginId
        self.__previousTaskId = previousTaskId
        self.__nextTaskId = nextTaskId
        self.__addToQueueTime = addToQueueTime
        self.__scheduledRunTime = scheduledRunTime
        self.__expirationTime = expirationTime
        self.__startTime = startTime
        self.__endTime = endTime
        self.__active = active
        self.__shouldImportOnStart = shouldImportOnStart
        self.__parameters = parameters
        
        from model import Model # import statement here to avoid circular import

        # object properties
        self.__plugin = plugin
        self.__previousTask = None
        self.__nextTask = None

        Task.tasks.append(self)

        Log.newDebug(f'Setting up previous and next tasks for task {taskId}', 0, 0)

        if previousTaskId != -1:
            self.__previousTask = Task.__checkTasksForId(previousTaskId)
            if self.__previousTask == None:
                self.__previousTask = Model.retrieveTaskById(previousTaskId, 0, 0)
        
        if nextTaskId != -1:
            self.__nextTask = Task.__checkTasksForId(nextTaskId)
            if self.__nextTask == None:
                self.__nextTask = Model.retrieveTaskById(nextTaskId, 0, 0)

        Log.newDebug(f'Task {repr(self)} instantiated.', 0, 0)

    '''
    public Task.newTask(priority: integer, pluginId: integer, previousTaskId: integer, nextTaskId: integer, addToQueueTime: integer, scheduledRunTime: integer, startTime: integer, endTime: integer, active: boolean, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for creating a new task.
    '''
    @classmethod
    def newTask(cls, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, parameters, runTaskId, runPluginId, shouldImportOnStart=True,):
        Log.newDebug(f'Task.newTask run... setting up task in model', runTaskId, runPluginId)

        from model import Model # import statement here to avoid circular import
        taskId = Model.createTask(priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, runTaskId, runPluginId)

        Log.newDebug(f'Getting plugin for task {taskId} from model', runTaskId, runPluginId)
        # PluginId should always point to a valid plugin
        plugin = Model.retrievePluginById(pluginId, runTaskId, runPluginId)

        Log.newDebug(f'Sending task {taskId} to Task constructor', runTaskId, runPluginId)
        return cls(taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, plugin)

    '''
    public Task.newTaskFromPlugin(priority: integer, plugin: plugin, previousTaskId: integer, nextTaskId: integer, addToQueueTime: integer, scheduledRunTime: integer, startTime: integer, endTime: integer, active: boolean, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for creating a new task when the plugin has already been instantiated.
    '''
    @classmethod
    def newTaskFromPlugin(cls, priority, plugin, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, parameters, runTaskId, runPluginId, shouldImportOnStart=True):
        Log.newDebug(f'Task.newTaskFromPlugin run... setting up task in model', runTaskId, runPluginId)

        from model import Model # import statement here to avoid circular import

        taskId = Model.createTask(priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, runTaskId, runPluginId)

        Log.newDebug(f'Sending task {taskId} to Task constructor', runTaskId, runPluginId)
        return cls(taskId, priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, plugin)
    
    '''
    public Task.taskWithId(taskId: integer, priority: integer, pluginId: integer, previousTaskId: integer, nextTaskId: integer, addToQueueTime: integer, scheduledRunTime: integer, startTime: integer, endTime: integer, active: boolean, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for creating a new task object for a task that has already been created in the database. If a task with the given taskId already exists, it will be returned instead of creating a new one to avoid synchronization issues. Otherwise, a new task will be created.
    '''
    @classmethod
    def taskWithId(cls, taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, parameters, runTaskId, runPluginId, shouldImportOnStart=True):
        Log.newDebug(f'Task.taskWithId run... checking for instantiated tasks with same id', runTaskId, runPluginId)

        # check if a task with the given taskId already exists to avoid duplicates and synchronization issues
        task = cls.__checkTasksForId(taskId)
        if task is not None:
            return task

        Log.newDebug(f'Task.taskWithId run... setting up task in model', runTaskId, runPluginId)
        from model import Model # import statement here to avoid circular import
        
        Log.newDebug(f'Getting plugin for task {taskId} from model', runTaskId, runPluginId)
        # PluginId should always point to a valid plugin
        plugin = Model.retrievePluginById(pluginId, runTaskId, runPluginId)

        Log.newDebug(f'Sending task {taskId} to Task constructor', runTaskId, runPluginId)
        return cls(taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, plugin)

    '''
    public Task.priorityTask(priority: integer, plugin: plugin, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for a basic task for addition to the priority queue (rather than the scheduled queue).
    '''
    @classmethod
    def priorityTask(cls, priority, plugin, parameters, runTaskId, runPluginId, expirationTime=-1, expirationDelta=-1, shouldImportOnStart=True):
        Log.newDebug(f'Task.priorityTask run... setting up task in model using passed and default values', runTaskId, runPluginId)
        from model import Model # import statement here to avoid circular import

        previousTaskId = -1
        nextTaskId = -1
        addToQueueTime = Model.createTimeStamp()
        scheduledRunTime = -1
        startTime = -1
        endTime = -1
        active = True

        if expirationDelta != -1:
            expirationTime = Model.createTimeStamp() + expirationDelta
            Log.newDebug(f'Setting expiration time to {expirationTime}', runTaskId, runPluginId)
        
        Log.newDebug('Creating task in model', runTaskId, runPluginId)
        taskId = Model.createTask(priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, runTaskId, runPluginId)

        Log.newDebug(f'Sending task {taskId} to Task constructor', runTaskId, runPluginId)
        return cls(taskId, priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, plugin)

    '''
    public Task.scheduleTaskTimeStamp(priority: integer, plugin: plugin, scheduledRunTime: integer, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for a basic task that will be scheduled to run at a certain time.
    '''
    @classmethod
    def scheduleTaskTimeStamp(cls, priority, plugin, scheduledRunTime, parameters, runTaskId, runPluginId, expirationTime=-1, expirationDelta=-1, shouldImportOnStart=True):
        Log.newDebug(f'Task.scheduleTaskTimeStamp run... setting up task in model using passed and default values', runTaskId, runPluginId)
        from model import Model # import statement here to avoid circular import

        previousTaskId = -1
        nextTaskId = -1
        addToQueueTime = Model.createTimeStamp()
        startTime = -1
        endTime = -1
        active = True

        if expirationDelta != -1:
            expirationTime = scheduledRunTime + expirationDelta
            Log.newDebug(f'Setting expiration time to {expirationTime}', runTaskId, runPluginId)

        Log.newDebug('Creating task in model', runTaskId, runPluginId)
        taskId = Model.createTask(priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, runTaskId, runPluginId)

        Log.newDebug(f'Sending task {taskId} to Task constructor', runTaskId, runPluginId)
        return cls(taskId, priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, plugin)

    '''
    public Task.scheduleTaskDelta(priority: integer, plugin: plugin, delta: integer, runTaskId: integer, runPluginId: integer) -> Task

    This is the class method for a basic task that will be scheduled to run a certain number of seconds in the future.
    '''
    @classmethod
    def scheduleTaskDelta(cls, priority, plugin, delta, parameters, runTaskId, runPluginId, expirationTime=-1, expirationDelta=-1, shouldImportOnStart=True):
        Log.newDebug(f'Task.scheduleTaskDelta run... setting up task in model using passed and default values', runTaskId, runPluginId)
        from model import Model # import statement here to avoid circular import

        previousTaskId = -1
        nextTaskId = -1
        addToQueueTime = Model.createTimeStamp()
        scheduledRunTime = Model.createTimeStamp() + delta
        startTime = -1
        endTime = -1
        active = True

        if expirationDelta != -1:
            expirationTime = scheduledRunTime + expirationDelta
            Log.newDebug(f'Setting expiration time to {expirationTime}', runTaskId, runPluginId)

        Log.newDebug('Creating task in model', runTaskId, runPluginId)
        taskId = Model.createTask(priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, runTaskId, runPluginId)

        Log.newDebug(f'Sending task {taskId} to Task constructor', runTaskId, runPluginId)
        return cls(taskId, priority, plugin.getPluginId(), previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters, plugin)

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

    # TODO: add static get task from id

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

    def getExpirationTime(self):
        return self.__expirationTime # integer
    
    def getStartTime(self):
        return self.__startTime # integer
    
    def getEndTime(self):
        return self.__endTime # integer
    
    def getActive(self):
        return self.__active # boolean

    def getShouldImportOnStart(self):
        return self.__shouldImportOnStart # boolean

    def getParameters(self):
        return self.__parameters # any[]

    def getPlugin(self):
        return self.__plugin # plugin

    def getPreviousTask(self):
        return self.__previousTask # task
    
    def getNextTask(self):
        return self.__nextTask # task

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
            self.__previousTask = None

            if previousTaskId != -1:
                self.__previousTask = Model.retrieveTaskById(previousTaskId)

            return True
        
        return False
    
    def setNextTaskId(self, nextTaskId, runTaskId, runPluginId):
        # update the nextTaskId in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateTaskNextTaskId(self.__taskId, nextTaskId, runTaskId, runPluginId):
            self.__nextTaskId = nextTaskId
            self.__nextTask = None

            if nextTaskId != -1:
                self.__nextTask = Model.retrieveTaskById(nextTaskId)

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
    
    def setPreviousTask(self, previousTask, runTaskId, runPluginId):
         # update the previousTaskId in the model
        from model import Model # import statement here to avoid circular import
        previousTaskId = -1

        if previousTask is not None:
            previousTaskId = previousTask.getTaskId()
        
        if Model.updateTaskPreviousTaskId(self.__taskId, previousTaskId, runTaskId, runPluginId):
            self.__previousTaskId = previousTaskId
            self.__previousTask = previousTask

            return True
        
        return False

    def setNextTask(self, nextTask, runTaskId, runPluginId):
        # update the nextTaskId in the model
        from model import Model # import statement here to avoid circular import
        nextTaskId = -1

        if nextTask is not None:
            nextTaskId = nextTask.getTaskId()
        
        if Model.updateTaskNextTaskId(self.__taskId, nextTaskId, runTaskId, runPluginId):
            self.__nextTaskId = nextTaskId
            self.__nextTask = nextTask

            return True
        
        return False
    
    '''
    ----------------------------------------------------------------------------
    Task methods

    These methods are used to perform actions on the task object.
    ----------------------------------------------------------------------------

    public start(taskManager: taskManager)

    This method is used to start the task.
    '''
    def start(self, taskManager):
        Log.newDebug(f'Task.start() for task {self.__taskId}', self.__taskId, self.__pluginId)
        self.__taskManager = taskManager

        Log.newDebug(f'Setting task {self.__taskId} to inactive and setting start time', self.__taskId, self.__pluginId)
        # set active to false before we start running in case something goes wrong, we don't continually boot with the running task active
        self.setActive(False, self.getTaskId(), self.getPluginId())

        from model import Model
        self.setStartTime(Model.createTimeStamp(), self.getTaskId(), self.getPluginId())

        Log.newDebug(f'Starting the plugin for task {self.__taskId}', self.__taskId, self.__pluginId)
        self.__plugin.start(self.__taskId, self.__taskManager, self.__parameters)

        Log.newDebug(f'Calling terminate function for task {self.__taskId}', self.__taskId, self.__pluginId)
        self.terminate()
    
    '''
    public terminate()

    This method is used to clean up the task after execution and tell the task manager to start the next task.
    '''
    def terminate(self):
        Log.newDebug(f'Task.terminate() for task {self.__taskId}', self.__taskId, self.__pluginId)

        Log.newDebug(f'Setting task {self.__taskId} end time', self.__taskId, self.__pluginId)
        from model import Model
        self.setEndTime(Model.createTimeStamp(), self.getTaskId(), self.getPluginId())
        
        Log.newDebug(f'Terminating the plugin for task {self.__taskId}', self.__taskId, self.__pluginId)
        self.__plugin.terminate(self.__taskId, self.__taskManager, self.__parameters)

    '''
    public expirationTimePassed()

    This method is called if the task expires without executing because the time sensitivity has passed.
    '''
    def expired(self):
        Log.newDebug(f'Task.expired() for task {self.__taskId}', self.__taskId, self.__pluginId)

        Log.newDebug(f'Setting task {self.__taskId} to inactive', self.__taskId, self.__pluginId)
        self.setActive(False, 0, self.getPluginId())

        Log.newDebug(f'Calling expired function for task {self.__taskId}', self.__taskId, self.__pluginId)
        self.getPlugin().expired(self.__taskManager, self.__parameters)

    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the task object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        return f'Task {self.__taskId} with priority {self.__priority} runs plugin {self.__pluginId} at {self.__scheduledRunTime}'

    # represent function
    def __repr__(self):
        return f'Task(taskId={self.__taskId}, priority={self.__priority}, pluginId={self.__pluginId}, previousTaskId={self.__previousTaskId}, nextTaskId={self.__nextTaskId}, scheduledRunTime={self.__scheduledRunTime}, expirationTime={self.__expirationTime}, startTime={self.__startTime}, endTime={self.__endTime}, active={self.__active}, shouldImportOnStart={self.__shouldImportOnStart}, parameters={self.__parameters})'