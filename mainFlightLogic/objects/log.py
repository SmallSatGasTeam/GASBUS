'''
This is the "log" object.

The log object requires a message, taskId, pluginId, level, time stamp, sent marker, and an echo marker. The log object also receives a logId from the database. The message is the information logged. The taskId identifies which task was running when the log was created. The pluginId identifies which plugin was running when the log was created. The level indicates what will happen to the log after logging. The timeStamp is the time the log was created. The sent marker indicates whether the log has been transmitted to the ground and the echo marker indicates whether the log has been echoed by the ground.

logId is an integer available for getting.
message is a string available for getting.
taskId is an integer available for getting.
pluginId is an integer available for getting.
level is a integer available for getting.
timeStamp is an integer available for getting.
sentMarker is a boolean available for getting and setting.
echoMarker is a boolean available for getting and setting.
'''

class Log:
    # class variables
    logs = [] # a list of all instantiated logs

    ERROR_LEVEL = 100
    WARNING_LEVEL = 200
    INFO_LEVEL = 300
    DEBUG_LEVEL = 400

    PRINT_ERROR = True
    PRINT_WARNING = True
    PRINT_INFO = True
    PRINT_DEBUG = True

    '''
    ----------------------------------------------------------------------------
    Constructors

    These methods are used to instantiate new logs.
    ----------------------------------------------------------------------------

    default constructor - never use this outside of the class, use the class methods instead
    '''
    def __init__(self, logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker):
        self.__logId = logId
        self.__message = message
        self.__taskId = taskId
        self.__pluginId = pluginId
        self.__level = level
        self.__timeStamp = timeStamp
        self.__sentMarker = sentMarker
        self.__echoMarker = echoMarker

        Log.logs.append(self)

    '''
    public Log.newLog(message: string, taskId: integer, pluginId: integer, level: integer) -> Log

    This is the class method for creating a new log.
    '''
    @classmethod
    def newLog(cls, message, taskId, pluginId, level):
        from model import Model # import statement here to avoid circular import
        logId, timeStamp = Model.createLog(message, taskId, pluginId, level)

        # when logs are created, they are not sent or echoed
        sentMarker = False
        echoMarker = False

        if level == cls.ERROR_LEVEL and cls.PRINT_ERROR:
            print(f'ERROR   | {Model.getDateTime(timeStamp)} | Task: {taskId:05} | Plugin: {pluginId:03} | {message}')
        
        if level == cls.WARNING_LEVEL and cls.PRINT_WARNING:
            print(f'WARNING | {Model.getDateTime(timeStamp)} | Task: {taskId:05} | Plugin: {pluginId:03} | {message}')
        
        if level == cls.INFO_LEVEL and cls.PRINT_INFO:
            print(f'INFO    | {Model.getDateTime(timeStamp)} | Task: {taskId:05} | Plugin: {pluginId:03} | {message}')

        if level == cls.DEBUG_LEVEL and cls.PRINT_DEBUG:
            print(f'DEBUG   | {Model.getDateTime(timeStamp)} | Task: {taskId:05} | Plugin: {pluginId:03} | {message}')

        return cls(logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker)

    '''
    public Log.logWithId(logId: integer, message: string, taskId: integer, pluginId: integer, level: integer, timeStamp: integer, sentMarker: boolean, echoMarker: boolean) -> Log

    This is the class method for creating a new log object for a log that has already been created in the database. If a log with the given logId already exists, it will be returned instead of creating a new log object to avoid synchronization issues. Otherwise, a new log object will be created.
    '''
    @classmethod
    def logWithId(cls, logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker):
        # check if a log with the same logId already exists to avoid duplicates and syncronization issues
        log = cls.__checkLogsForId(logId)
        if log is not None:
            return log

        return cls(logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker)

    '''
    public Log.newError(message: string, taskId: integer, pluginId: integer) -> Log

    This is the class method for creating a new error log.
    '''
    @classmethod
    def newError(cls, message, taskId, pluginId):
        return cls.newLog(message, taskId, pluginId, cls.ERROR_LEVEL)
    
    '''
    public Log.newWarning(message: string, taskId: integer, pluginId: integer) -> Log

    This is the class method for creating a new warning log.
    '''
    @classmethod
    def newWarning(cls, message, taskId, pluginId):
        return cls.newLog(message, taskId, pluginId, cls.WARNING_LEVEL)

    '''
    public Log.newInfo(message: string, taskId: integer, pluginId: integer) -> Log

    This is the class method for creating a new info log.
    '''
    @classmethod
    def newInfo(cls, message, taskId, pluginId):
        return cls.newLog(message, taskId, pluginId, cls.INFO_LEVEL)

    '''
    public Log.newDebug(message: string, taskId: integer, pluginId: integer) -> Log

    This is the class method for creating a new debug log.
    '''
    @classmethod
    def newDebug(cls, message, taskId, pluginId):
        return cls.newLog(message, taskId, pluginId, cls.DEBUG_LEVEL)

    '''
    private static Log.__checkLogsForId(logId: integer) -> Log | None

    Checks to see if a log with a given logId has already been created. If it has, it will be returned.
    '''
    @staticmethod
    def __checkLogsForId(logId):
        for log in Log.logs:
            if log.getLogId() == logId:
                return log
        return None

    '''
    ----------------------------------------------------------------------------
    Getters

    These methods are used to access the values of the log object.
    ----------------------------------------------------------------------------
    '''
    def getLogId(self):
        return self.__logId # integer
    
    def getMessage(self):
        return self.__message # string
    
    def getTaskId(self):
        return self.__taskId # integer

    def getPluginId(self):
        return self.__pluginId # integer

    def getLevel(self):
        return self.__level # integer

    def getTimeStamp(self):
        return self.__timeStamp # integer

    def getSentMarker(self):
        return self.__sentMarker # boolean

    def getEchoMarker(self):
        return self.__echoMarker # boolean

    '''
    ----------------------------------------------------------------------------
    Setters
    
    These methods are used to set the values of the log object.
    ----------------------------------------------------------------------------
    '''
    def setSentMarker(self, sentMarker, runTaskId, runPluginId):
        # update the sent marker in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateLogSentMarker(self.__logId, sentMarker, runTaskId, runPluginId):
            # update the sent marker in the log object
            self.__sentMarker = sentMarker
            return True

        return False

    def setEchoMarker(self, echoMarker, runTaskId, runPluginId):
        # update the echo marker in the model
        from model import Model # import statement here to avoid circular import
        if Model.updateLogEchoMarker(self.__logId, echoMarker, runTaskId, runPluginId):
            # update the echo marker in the log object
            self.__echoMarker = echoMarker
            return True

        return False
    
    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the log object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        return f'Log {self.__logId} says "{self.__message}" recorded during task {self.__taskId} by plugin {self.__pluginId} at level {self.__level} at time {self.__timeStamp}. Sent marker: {self.__sentMarker}. Echo marker: {self.__echoMarker}'

    # represent function
    def __repr__(self):
        return f'Log(logId={self.__logId}, message="{self.__message}", taskId={self.__taskId}, pluginId={self.__pluginId}, level={self.__level}, timeStamp={self.__timeStamp}, sentMarker={self.__sentMarker}, echoMarker={self.__echoMarker})'