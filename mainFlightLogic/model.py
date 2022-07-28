'''
This is the "model" module.

The model module contains the database connection and the database functions. Any function that needs to access the database should be placed in this module.

This module contains only static methods meaning that it cannot be instantiated.
'''

import sqlite3
from sqlite3 import Error
from datetime import datetime
from objects.log import Log
from objects.datum import Datum
from objects.packet import Packet
from objects.task import Task
from objects.plugin import Plugin

class Model:
    '''
    ----------------------------------------------------------------------------
    Connection methods

    These methods are used to connect to the database and close the connection after the data has been recorded.
    ----------------------------------------------------------------------------

    private static __check_connection(runTaskId: integer, runPluginId: integer) -> connection | False

    Attempts to open a connection. If the connection is successful, the connection is returned. If the connection is not successful, False is returned.
    '''
    @staticmethod
    def __check_connection(runTaskId, runPluginId):
        connection = None
        try:
            connection = sqlite3.connect("satData.db")
            return connection
        except Error as e:
            Log.newLog(f'Database Connection Error: {e}', runTaskId, runPluginId, 100)
            return False
    
    '''
    private static __close_connection(connection: connection) -> None

    Closes the passed connection.
    '''
    @staticmethod
    def __close_connection(connection):
        connection.close()

    '''
    ----------------------------------------------------------------------------
    Time methods

    These method are used to create and utilize integer timestamps for the database.
    ----------------------------------------------------------------------------

    public static createTimeStamp() -> integer

    Creates a time stamp for now and returns it as an integer for comparison or database storage.
    '''
    @staticmethod
    def createTimeStamp():
        return int(datetime.now().timestamp())

    '''
    public static getTimeStamp(timeStamp: integer) -> datetime:

    Returns a datetime object from the passed integer time stamp.
    '''
    @staticmethod
    def getDateTime(timeStamp):
        return datetime.utcfromtimestamp(timeStamp)

    '''
    ----------------------------------------------------------------------------
    Log methods

    These methods are used to create and store log entries in the database.
    ----------------------------------------------------------------------------

    private static __checkLogsTable(connection: connection) -> True | False

    Checks if the logs table exists. If it does not exist, it is created.
    '''
    @staticmethod
    def __checkLogsTable(connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs';")

            # if the logs table doesn't exist, create it
            if cursor.fetchone() is None:
                cursor.execute("CREATE TABLE logs (logId INTEGER PRIMARY KEY, message TEXT, taskId INTEGER, pluginId INTEGER, level INTEGER, timeStamp INTEGER, sentMarker INTEGER, echoMarker INTEGER);")

            connection.commit()
            return True
        except Error as e:
            Log.newLog(f'Database Logs Table Error: {e}', 0, 0, 100)
            return False

    '''
    public static createLog(message: string, taskId: integer, pluginId: integer, level: integer) -> (logId: integer, timeStamp: integer)

    Creates a log entry in the database using passed and default values, then returns the logId and timeStamp.
    '''
    @staticmethod
    def createLog(message, taskId, pluginId, level):
        # set up the connection
        connection = Model.__check_connection(taskId, pluginId)
        if connection and Model.__checkLogsTable(connection):
            cursor = connection.cursor()

            # new log default values
            timeStamp = Model.createTimeStamp()
            sentMarker = False
            echoMarker = False

            # insert the new log into the database
            cursor.execute("""INSERT INTO logs (message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""", (message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker))

            logId = cursor.lastrowid

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return logId, timeStamp

        return False

    '''
    public static retrieveLogById(logId: integer, runTaskId: integer, runPluginId: integer) -> Log | False

    Retrieves a log entry from the database using the passed logId. If the log is found, it is returned as a log object.
    '''
    @staticmethod
    def retrieveLogById(logId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkLogsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker
                                FROM logs
                                WHERE logId = ?""", (logId,))
            result = cursor.fetchone()

            Model.__close_connection(connection)

            # format the result into a log object
            if result is not None:
                return Log.logWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])

        return False

    '''
    public static retrieveLogsByTime(startTime: integer, endTime: integer, runTaskId: integer, runPluginId: integer) -> Log[] | False

    Retrieves all log entries from the database between the passed start and end times.
    '''
    @staticmethod
    def retrieveLogsByTime(startTime, endTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkLogsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker
                                FROM logs
                                WHERE timeStamp BETWEEN ? AND ?""", (startTime, endTime))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of log objects
            logs = []
            for result in results:
                logs.append(Log.logWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]))

            return logs

        return False
    
    '''
    public static retrieveLogsByTaskId(taskId: integer, runTaskId: integer, runPluginId: integer) -> Log[] | False

    Retrieves all log entries from the database for the passed taskId.
    '''
    @staticmethod
    def retrieveLogsByTaskId(taskId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkLogsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker
                                FROM logs
                                WHERE taskId = ?""", (taskId,))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of log objects
            logs = []
            for result in results:
                logs.append(Log.logWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]))

            return logs

        return False
    
    '''
    public static retrieveLogsByPluginId(pluginId: integer, runTaskId: integer, runPluginId: integer) -> Log[] | False

    Retrieves all log entries from the database for the passed pluginId.
    '''
    @staticmethod
    def retrieveLogsByPluginId(pluginId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkLogsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker
                                FROM logs
                                WHERE pluginId = ?""", (pluginId,))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of log objects
            logs = []
            for result in results:
                logs.append(Log.logWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]))

            return logs

        return False
    
    '''
    public static updateSentMarker(logId: integer, sentMarker: boolean, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the sentMarker value for the passed logId.
    '''
    @staticmethod
    def updateLogSentMarker(logId, sentMarker, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkLogsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE logs
                                SET sentMarker = ?
                                WHERE logId = ?""", (sentMarker, logId))

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return True

        return False
    
    '''
    public static updateEchoMarker(logId: integer, echoMarker: boolean, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the echoMarker value for the passed logId.
    '''
    @staticmethod
    def updateLogEchoMarker(logId, echoMarker, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkLogsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE logs
                                SET echoMarker = ?
                                WHERE logId = ?""", (echoMarker, logId))

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return True

        return False
    
    '''
    ----------------------------------------------------------------------------
    Datum methods

    These methods are used to create and store datum entries in the database.
    ----------------------------------------------------------------------------

    private static __checkDataTable(connection: connection) -> True | False

    Checks if the data table exists. If it does not exist, it is created.
    '''
    @staticmethod
    def __checkDataTable(connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data';")

            # if the data table doesn't exist, create it
            if cursor.fetchone() is None:
                cursor.execute("CREATE TABLE data (datumId INTEGER PRIMARY KEY, sensor INTEGER, datum TEXT, recordTimeStamp INTEGER);")

            connection.commit()
            return True
        except Error as e:
            Log.newLog(f'Database Data Table Error: {e}', 0, 0, 100)
            return False

    '''
    public static createDatum(sensor: integer, datum: string, recordTimeStamp: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Creates a datum entry in the database then returns the datumId.
    '''
    @staticmethod
    def createDatum(sensor, datum, recordTimestamp, runTaskId, runPluginId):
        # set up the connection
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkLogsTable(connection):
            cursor = connection.cursor()

            # insert the new datum into the database
            cursor.execute("""INSERT INTO data (sensor, datum, recordTimeStamp)
                                VALUES (?, ?, ?)""", (sensor, datum, recordTimestamp))

            datumId = cursor.lastrowid

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return datumId

        return False

    '''
    public static retrieveDatumById(datumId: integer, runTaskId: integer, runPluginId: integer) -> Datum | False

    Retrieves a datum entry from the database by the passed datumId. If the datum is found, it is returned as a Datum object.
    '''
    @staticmethod
    def retrieveDatumById(datumId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkDataTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT datumId, sensor, datum, recordTimeStamp
                                FROM data
                                WHERE datumId = ?""", (datumId,))
            result = cursor.fetchone()

            Model.__close_connection(connection)

            # format result as a datum object
            if result:
                return Datum.datumWithId(result[0], result[1], result[2], result[3])

        return False

    '''
    public static retrieveDatumBySensor(sensor: integer, runTaskId: integer, runPluginId: integer) -> Datum[] | False

    Retrieves all datum entries from the database for the passed sensor.
    '''
    @staticmethod
    def retrieveDataBySensor(sensor, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkDataTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT datumId, sensor, datum, recordTimeStamp
                                FROM data
                                WHERE sensor = ?""", (sensor,))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of datum objects
            datums = []
            for result in results:
                datums.append(Datum.datumWithId(result[0], result[1], result[2], result[3]))

            return datums

        return False

    '''
    public static retrieveDataByTime(startTime: integer, endTime: integer, runTaskId: integer, runPluginId: integer) -> Datum[] | False

    Retrieves all datum entries from the database between the passed startTime and endTime.
    '''
    @staticmethod
    def retrieveDataByTime(startTime, endTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkDataTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT datumId, sensor, datum, recordTimeStamp
                                FROM data
                                WHERE recordTimeStamp BETWEEN ? AND ?""", (startTime, endTime))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of datum objects
            datums = []
            for result in results:
                datums.append(Datum.datumWithId(result[0], result[1], result[2], result[3]))

            return datums

        return False
    
    '''
    ----------------------------------------------------------------------------
    Packet methods

    These methods are used to create and store packet entries in the database.
    ----------------------------------------------------------------------------

    private static __checkPacketsTable(connection: connection) -> True | False

    Checks if the packets table exists. If it does not exist, it is created.
    '''
    @staticmethod
    def __checkPacketsTable(connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='packets';")

            # if the packets table doesn't exist, create it
            if cursor.fetchone() is None:
                cursor.execute("CREATE TABLE packets (packetId INTEGER PRIMARY KEY, data TEXT, sendTime INTEGER);")

            connection.commit()
            return True
        except Error as e:
            Log.newLog(f'Database Packets Table Error: {e}', 0, 0, 100)
            return False
    
    '''
    public static createPacket(data: string, sendTime: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Creates a packet entry in the database then returns the packetId.
    '''
    @staticmethod
    def createPacket(data, sendTime, runTaskId, runPluginId):
        # set up the connection
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkPacketsTable(connection):
            cursor = connection.cursor()

            # insert the new packet into the database
            cursor.execute("""INSERT INTO packets (data, sendTime)
                                VALUES (?, ?)""", (data, sendTime))

            packetId = cursor.lastrowid

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return packetId

        return False

    '''
    public static retrievePacketById(packetId: integer, runTaskId: integer, runPluginId: integer) -> Packet | False

    Retrieves a packet entry from the database by the passed packetId. If the packet is found, it is returned as a Packet object.
    '''
    @staticmethod
    def retrievePacketById(packetId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkPacketsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT packetId, data, sendTime
                                FROM packets
                                WHERE packetId = ?""", (packetId,))
            result = cursor.fetchone()

            Model.__close_connection(connection)

            # format result as a packet object
            if result:
                return Packet.packetWithId(result[0], result[1], result[2])

        return False

    '''
    public static retrievePacketBySendTime(startTime: integer, endTime: integer, runTaskId: integer, runPluginId: integer) -> Packet[] | False

    Retrieves all packet entries from the database between the passed startTime and endTime.
    '''
    @staticmethod
    def retrievePacketsBySendTime(startTime, endTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkPacketsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT packetId, data, sendTime
                                FROM packets
                                WHERE sendTime BETWEEN ? AND ?""", (startTime, endTime))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of packet objects
            packets = []
            for result in results:
                packets.append(Packet.packetWithId(result[0], result[1], result[2]))

            return packets

        return False
    
    '''
    public static updateSendTime(packetId: integer, sendTime: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the send time value for the passed packetId.
    '''
    @staticmethod
    def updatePacketSendTime(packetId, sendTime, runTaskId, runPluginId):
        # set up the connection
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkPacketsTable(connection):
            cursor = connection.cursor()

            # update the send time value
            cursor.execute("""UPDATE packets
                                SET sendTime = ?
                                WHERE packetId = ?""", (sendTime, packetId))

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return True

        return False

    '''
    ----------------------------------------------------------------------------
    Task methods

    These methods are used to create and store task entries in the database.
    ----------------------------------------------------------------------------

    private static __checkTasksTable(connection: connection) -> True | False

    Checks if the tasks table exists. If it does not exist, it is created.
    '''
    @staticmethod
    def __checkTasksTable(connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';")

            # if the tasks table doesn't exist, create it
            if cursor.fetchone() is None:
                cursor.execute("CREATE TABLE tasks (taskId INTEGER PRIMARY KEY, priority INTEGER, pluginId INTEGER, previousTaskId INTEGER, nextTaskId INTEGER, addToQueueTime INTEGER, scheduledRunTime INTEGER, startTime INTEGER, endTime INTEGER, active INTEGER);")

            connection.commit()
            return True
        except Error as e:
            Log.newLog(f'Database Tasks Table Error: {e}', 0, 0, 100)
            return False

    '''
    public static createTask(priority: integer, pluginId: integer, previousTaskId: integer, nextTaskId: integer, addToQueueTime: integer, scheduledRunTime: integer, startTime: integer, endTime: integer, active: boolean, runTaskId: integer, runPluginId: integer) -> boolean

    Creates a task entry in the database then returns the taskId.
    '''
    @staticmethod
    def createTask(priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active, runTaskId, runPluginId):
        # set up the connection
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            cursor = connection.cursor()

            # insert the new task into the database
            cursor.execute("""INSERT INTO tasks (priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active))

            taskId = cursor.lastrowid

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return taskId

        return False

    '''
    public static retrieveTaskById(taskId: integer, runTaskId: integer, runPluginId: integer) -> Task | False

    Retrieves a task entry from the database by the passed taskId. If the task is found, it is returned as a Task object.
    '''
    @staticmethod
    def retrieveTaskById(taskId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active
                                FROM tasks
                                WHERE taskId = ?""", (taskId,))
            result = cursor.fetchone()

            Model.__close_connection(connection)

            # format result as a task object
            if result:
                return Task.taskWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9])

        return False

    '''
    public static retrieveTasksByPluginId(pluginId: integer, runTaskId: integer, runPluginId: integer) -> Task[] | False
    '''
    @staticmethod
    def retrieveTasksByPluginId(pluginId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active
                                FROM tasks
                                WHERE pluginId = ?""", (pluginId,))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of task objects
            tasks = []
            for result in results:
                tasks.append(Task.taskWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]))

            return tasks

        return False
    
    '''
    public static retrieveTasksByAddToQueueTime(startTime: integer, endTime: integer, runTaskId: integer, runPluginId: integer) -> Task[] | False

    Returns a list of tasks that were added to the queue between the start and end times.
    '''
    @staticmethod
    def retrieveTasksByAddToQueueTime(startTime, endTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active
                                FROM tasks
                                WHERE addToQueueTime BETWEEN ? AND ?""", (startTime, endTime))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of task objects
            tasks = []
            for result in results:
                tasks.append(Task.taskWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]))

            return tasks

        return False
    
    '''
    public static retrieveTasksByScheduledRunTime(startTime: integer, endTime: integer, runTaskId: integer, runPluginId: integer) -> Task[] | False

    Returns a list of tasks that were scheduled to run between the start and end times.
    '''
    @staticmethod
    def retrieveTasksByScheduledRunTime(startTime, endTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active
                                FROM tasks
                                WHERE scheduledRunTime BETWEEN ? AND ?""", (startTime, endTime))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of task objects
            tasks = []
            for result in results:
                tasks.append(Task.taskWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]))

            return tasks

        return False
    
    '''
    public static retrieveTasksByStartTime(startTime: integer, endTime: integer, runTaskId: integer, runPluginId: integer) -> Task[] | False

    Returns a list of tasks that were started between the start and end times.
    '''
    @staticmethod
    def retrieveTasksByStartTime(startTime, endTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active
                                FROM tasks
                                WHERE startTime BETWEEN ? AND ?""", (startTime, endTime))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of task objects
            tasks = []
            for result in results:
                tasks.append(Task.taskWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]))

            return tasks

        return False
    
    '''
    public static retrieveTasksByActive(active: boolean, runTaskId: integer, runPluginId: integer) -> Task[] | False

    Returns a list of tasks that are active or inactive.
    '''
    @staticmethod
    def retrieveTasksByActive(active, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, startTime, endTime, active
                                FROM tasks
                                WHERE active = ?""", (active,))
            results = cursor.fetchall()

            Model.__close_connection(connection)

            # format result as a list of task objects
            tasks = []
            for result in results:
                tasks.append(Task.taskWithId(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]))

            return tasks

        return False

    '''
    public static updateTaskPriority(taskId: integer, priority: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the priority of a task.
    '''
    @staticmethod
    def updateTaskPriority(taskId, priority, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE tasks
                                SET priority = ?
                                WHERE taskId = ?""", (priority, taskId))
            connection.commit()

            Model.__close_connection(connection)

            return True

        return False
    
    '''
    public static updateTaskPreviousTaskId(taskId: integer, previousTaskId: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the previous task id of a task.
    '''
    @staticmethod
    def updateTaskPreviousTaskId(taskId, previousTaskId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE tasks
                                SET previousTaskId = ?
                                WHERE taskId = ?""", (previousTaskId, taskId))
            connection.commit()

            Model.__close_connection(connection)

            return True

        return False
    
    '''
    public static updateTaskNextTaskId(taskId: integer, nextTaskId: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the next task id of a task.
    '''
    @staticmethod
    def updateTaskNextTaskId(taskId, nextTaskId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE tasks
                                SET nextTaskId = ?
                                WHERE taskId = ?""", (nextTaskId, taskId))
            connection.commit()

            Model.__close_connection(connection)

            return True

        return False
    
    '''
    public static updateTaskScheduledRunTime(taskId: integer, scheduledRunTime: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the scheduled run time of a task.
    '''
    @staticmethod
    def updateTaskScheduledRunTime(taskId, scheduledRunTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE tasks
                                SET scheduledRunTime = ?
                                WHERE taskId = ?""", (scheduledRunTime, taskId))
            connection.commit()

            Model.__close_connection(connection)

            return True

        return False
    
    '''
    public static updateTaskStartTime(taskId: integer, startTime: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the start time of a task.
    '''
    @staticmethod
    def updateTaskStartTime(taskId, startTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE tasks
                                SET startTime = ?
                                WHERE taskId = ?""", (startTime, taskId))
            connection.commit()

            Model.__close_connection(connection)

            return True

        return False
    
    '''
    public static updateTaskEndTime(taskId: integer, endTime: integer, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the end time of a task.
    '''
    @staticmethod
    def updateTaskEndTime(taskId, endTime, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE tasks
                                SET endTime = ?
                                WHERE taskId = ?""", (endTime, taskId))
            connection.commit()

            Model.__close_connection(connection)

            return True

        return False
    
    '''
    public static updateTaskActive(taskId: integer, active: boolean, runTaskId: integer, runPluginId: integer) -> boolean

    Updates the active status of a task.
    '''
    @staticmethod
    def updateTaskActive(taskId, active, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkTasksTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""UPDATE tasks
                                SET active = ?
                                WHERE taskId = ?""", (active, taskId))
            connection.commit()

            Model.__close_connection(connection)

            return True

        return False
    
    '''
    ----------------------------------------------------------------------------
    Plugin methods

    These methods are used to create and store plugin entries in the database.
    ----------------------------------------------------------------------------

    private static __checkPluginsTable(connection: connection) -> True | False

    Checks if the plugins table exists. If it does not exist, it is created.
    '''
    @staticmethod
    def __checkPluginsTable(connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plugins';")

            # if the packets table doesn't exist, create it
            if cursor.fetchone() is None:
                cursor.execute("CREATE TABLE plugins (pluginId INTEGER PRIMARY KEY, identifier TEXT);")

            connection.commit()
            return True
        except Error as e:
            Log.newLog(f'Database Plugins Table Error: {e}', 0, 0, 100)
            return False

    '''
    public static createPlugin(identifier: string, runTaskId: integer, runPluginId: integer) -> integer

    Creates a new plugin entry in the database then returns the plugin id.
    '''
    @staticmethod
    def createPlugin(identifier, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkPluginsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO plugins (identifier)
                                VALUES (?)""", (identifier,))
            connection.commit()

            pluginId = cursor.lastrowid

            # commit the changes and close the connection
            connection.commit()
            Model.__close_connection(connection)
            return pluginId

        return False

    '''
    public static retrievePluginById(pluginId: integer, runTaskId: integer, runPluginId: integer) -> Plugin
    '''
    @staticmethod
    def retrievePluginById(pluginId, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkPluginsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT *
                                FROM plugins
                                WHERE pluginId = ?""", (pluginId,))
            result = cursor.fetchone()

            Model.__close_connection(connection)

            # format result as a plugin object
            if result:
                return Plugin(result[0], result[1])

        return False

    '''
    public static retrievePluginByIdentifier(identifier: string, runTaskId: integer, runPluginId: integer) -> Plugin
    '''
    @staticmethod
    def retrievePluginByIdentifier(identifier, runTaskId, runPluginId):
        connection = Model.__check_connection(runTaskId, runPluginId)
        if connection and Model.__checkPluginsTable(connection):
            # database query
            cursor = connection.cursor()
            cursor.execute("""SELECT *
                                FROM plugins
                                WHERE identifier = ?""", (identifier,))
            result = cursor.fetchone()

            Model.__close_connection(connection)

            # format result as a plugin object
            if result:
                return Plugin(result[0], result[1])

        return False
