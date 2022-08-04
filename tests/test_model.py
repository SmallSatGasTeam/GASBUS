import pytest
import sqlite3
import os
from GASBUS_flight_logic.model import Model

class TestModel:
    def deleteDatabase(self):
        if os.path.exists('satData.db'):
            os.remove('satData.db')
    
    def checkTimestamp(self, timestamp):
        import datetime
        return int(datetime.datetime.now().timestamp()) - 1 <= timestamp <= int(datetime.datetime.now().timestamp())

    '''
    ----------------------------------------------------------------------------
    Connection method tests
    ----------------------------------------------------------------------------
    '''
    def test__check_connection(self):
        # Test the ability of the model to create a new database and connect to it.
        self.deleteDatabase()
        connection1 = Model._Model__check_connection(-10, -10)
        assert type(connection1) == sqlite3.Connection

        # Test the database connection.
        cursor1 = connection1.cursor()
        cursor1.execute('SELECT name FROM sqlite_schema WHERE type="table" AND name NOT LIKE "sqlite_%"')
        result = cursor1.fetchall()

        assert result == []

        # Add a table to the database.
        cursor1.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
        cursor1.execute('INSERT INTO test (name) VALUES ("test")')

        # Retrieve information from the database.
        cursor1.execute('SELECT id, name FROM test')
        result = cursor1.fetchall()

        assert result == [(1, 'test')]
        connection1.commit()
        connection1.close()

        # Test the ability of the model to connect to an existing database.
        connection2 = Model._Model__check_connection(-10, -10)
        assert type(connection2) == sqlite3.Connection

        # Retrieve information from the database.
        cursor2 = connection2.cursor()
        cursor2.execute('SELECT id, name FROM test')
        result = cursor2.fetchall()

        assert result == [(1, 'test')]

        # Clean up.
        connection2.close()
        self.deleteDatabase()
        
    def test__close_connection(self):
        # Test the ability of the model to close a connection to the database.
        connection = Model._Model__check_connection(-10, -10)
        assert type(connection) == sqlite3.Connection

        Model._Model__close_connection(connection)
        with pytest.raises(sqlite3.ProgrammingError) as e:
            connection.cursor()
        assert "closed database" in str(e.value)
        self.deleteDatabase()

    '''
    ----------------------------------------------------------------------------
    Time method tests
    ----------------------------------------------------------------------------
    '''
    def test_createTimeStamp(self):
        # Test the ability of the model to create a timestamp.
        timestamp = Model.createTimeStamp()
        assert type(timestamp) == int

        # Test the timestamp is in line with datetime.
        import datetime
        assert self.checkTimestamp(timestamp) == True
    
    '''
    ----------------------------------------------------------------------------
    Log method tests
    ----------------------------------------------------------------------------
    '''
    def test__checkLogsTable(self):
        # Test the ability of the model to create the logs table.
        connection1 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkLogsTable(connection1) == True

        cursor1 = connection1.cursor()
        cursor1.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs';")
        result = cursor1.fetchall()

        assert result == [('logs',)]
        connection1.close()

        # Test to make sure there is only one logs table after calling the function a second time.
        connection2 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkLogsTable(connection2) == True
        cursor2 = connection2.cursor()
        cursor2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs';")
        result = cursor2.fetchall()

        assert result == [('logs',)]

        # Clean up.
        connection2.close()
        self.deleteDatabase()
    
    def test_createLog(self):
        # Test the ability of the model to create a log.
        (logId, timeStamp) = Model.createLog('test', -10, -10, 0)
        assert type(logId) == type(timeStamp) == int

        # Test the log is in line with the database.
        connection = Model._Model__check_connection(-10, -10)
        cursor = connection.cursor()
        cursor.execute('SELECT logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker FROM logs')
        result = cursor.fetchall()

        assert result == [(1, 'test', -10, -10, 0, timeStamp, 0, 0)]

        assert self.checkTimestamp(timeStamp) == True

        assumedResult = [(1, 'test', -10, -10, 0, timeStamp, 0, 0)]

        # Test 100 more logs of varying parameters.
        for i in range(100):
            (logId, timeStamp) = Model.createLog('test' + str(i), -10 - i, -15 - i, i * 10)
            assert type(logId) == type(timeStamp) == int

            assumedResult.append((logId, 'test' + str(i), -10 - i, -15 - i, i * 10, timeStamp, 0, 0))
            
        cursor.execute('SELECT logId, message, taskId, pluginId, level, timeStamp, sentMarker, echoMarker FROM logs')
        result = cursor.fetchall()

        assert result == assumedResult

        # Clean up.
        connection.close()
        self.deleteDatabase()

    def test_retrieveLogById(self):
        # Test the ability of the model to retrieve a log by id
        (logId, timeStamp) = Model.createLog('test by id', -10, -10, 0)

        log = Model.retrieveLogById(logId, -10, -10)

        assert log.getLogId() == logId
        assert log.getMessage() == 'test by id'
        assert log.getTaskId() == -10
        assert log.getPluginId() == -10
        assert log.getLevel() == 0
        assert log.getTimeStamp() == timeStamp
        assert log.getSentMarker() == False
        assert log.getEchoMarker() == False

        # Test more logs
        for i in range(100):
            (logId, timeStamp) = Model.createLog(f'test{i}', -10 * i, -11 * i, i + 2)

            log = Model.retrieveLogById(logId, -10, -10)

            assert log.getLogId() == logId
            assert log.getMessage() == f'test{i}'
            assert log.getTaskId() == -10 * i
            assert log.getPluginId() == -11 * i
            assert log.getLevel() == i + 2
            assert log.getTimeStamp() == timeStamp
            assert log.getSentMarker() == False
            assert log.getEchoMarker() == False

        self.deleteDatabase()
    
    def test_retrieveLogsByTime(self):
        # Test the ability of the model to retrieve logs by time.
        (logId, timeStamp) = Model.createLog('test by time', -10, -10, 0)

        logs = Model.retrieveLogsByTime(Model.createTimeStamp() - 1, Model.createTimeStamp(), -10, -10)

        assert logs[0].getLogId() == logId
        assert logs[0].getMessage() == 'test by time'
        assert logs[0].getTaskId() == -10
        assert logs[0].getPluginId() == -10
        assert logs[0].getLevel() == 0
        assert logs[0].getTimeStamp() == timeStamp
        assert logs[0].getSentMarker() == False
        assert logs[0].getEchoMarker() == False

        # Test more logs
        for i in range(100):
            (logId, timeStamp) = Model.createLog(f'test{i}', -10 * i, -11 * i, i + 2)

            logs = Model.retrieveLogsByTime(Model.createTimeStamp() - 1, Model.createTimeStamp(), -10, -10)

            logInLogs = False

            for log in logs:
                if log.getLogId() == logId and log.getMessage() == f'test{i}':
                    logInLogs = True
            
            assert logInLogs == True
    
        self.deleteDatabase()
    
    def test_retrieveLogsByTaskId(self):
        # Test the ability of the model to retrieve logs by task id.
        (logId, timeStamp) = Model.createLog('test by task id', -10, -10, 0)

        logs = Model.retrieveLogsByTaskId(-10, -10, -10)

        assert logs[0].getLogId() == logId
        assert logs[0].getMessage() == 'test by task id'
        assert logs[0].getTaskId() == -10
        assert logs[0].getPluginId() == -10
        assert logs[0].getLevel() == 0
        assert logs[0].getTimeStamp() == timeStamp
        assert logs[0].getSentMarker() == False
        assert logs[0].getEchoMarker() == False

        # Test more logs
        for i in range(100):
            (logId, timeStamp) = Model.createLog(f'test{i}', (-7 + -3 * i) % 5, -16 + i, i - 7)

            logs = Model.retrieveLogsByTaskId((-7 + -3 * i) % 5, -10,  -10)

            logInLogs = False

            for log in logs:
                if log.getLogId() == logId and log.getMessage() == f'test{i}':
                    logInLogs = True
            
            assert logInLogs == True
    
        self.deleteDatabase()
    
    def test_retrieveLogsByPluginId(self):
        # Test the ability of the model to retrieve logs by plugin id.
        (logId, timeStamp) = Model.createLog('test by plugin id', -10, -10, 0)

        logs = Model.retrieveLogsByPluginId(-10, -10, -10)

        assert logs[0].getLogId() == logId
        assert logs[0].getMessage() == 'test by plugin id'
        assert logs[0].getTaskId() == -10
        assert logs[0].getPluginId() == -10
        assert logs[0].getLevel() == 0
        assert logs[0].getTimeStamp() == timeStamp
        assert logs[0].getSentMarker() == False
        assert logs[0].getEchoMarker() == False

        # Test more logs
        for i in range(100):
            (logId, timeStamp) = Model.createLog(f'test{i}', -10, (-15 + -6 * i) % 7, i + 7)

            logs = Model.retrieveLogsByPluginId((-15 + -6 * i) % 7, -10, -10)

            logInLogs = False

            for log in logs:
                if log.getLogId() == logId and log.getMessage() == f'test{i}':
                    logInLogs = True
            
            assert logInLogs == True
    
        self.deleteDatabase()
    
    def test_updateLogSentMarker(self):
        # Test the ability of the model to update a log's sent marker.
        (logId, _) = Model.createLog('test sent marker', -10, -10, 0)

        assert Model.retrieveLogById(logId, -10, -10).getSentMarker() == False

        Model.updateLogSentMarker(logId, True, -10, -10)

        assert Model.retrieveLogById(logId, -10, -10).getSentMarker() == True

        # Test more logs
        for i in range(100):
            (logId, _) = Model.createLog(f'test{i}', 17 * i, -11 + i, i - 2)

            assert Model.retrieveLogById(logId, -10, -10).getSentMarker() == False

            Model.updateLogSentMarker(logId, True, -10, -10)

            assert Model.retrieveLogById(logId, -10, -10).getSentMarker() == True
    
        self.deleteDatabase()
    
    def test_updateLogEchoMarker(self):
        from GASBUS_flight_logic.objects.log import Log

        # Test the ability of the model to update a log's echo marker.
        (logId, _) = Model.createLog('test echo marker', -10, -10, 0)

        assert Model.retrieveLogById(logId, -10, -10).getEchoMarker() == False

        Model.updateLogEchoMarker(logId, True, -10, -10)

        assert Model.retrieveLogById(logId, -10, -10).getEchoMarker() == True

        # Test more logs
        for i in range(100):
            (logId, _) = Model.createLog(f'test{i}', 17 * i, -11 + i, i - 2)

            assert Model.retrieveLogById(logId, -10, -10).getEchoMarker() == False

            Model.updateLogEchoMarker(logId, True, -10, -10)

            assert Model.retrieveLogById(logId, -10, -10).getEchoMarker() == True
    
        self.deleteDatabase()

    '''
    ----------------------------------------------------------------------------
    Datum method tests
    ----------------------------------------------------------------------------
    '''
    def test__checkDataTable(self):
        # Test the ability of the model to check if the datum table exists.
        connection1 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkDataTable(connection1) == True

        cursor1 = connection1.cursor()
        cursor1.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="data";')
        result = cursor1.fetchall()

        assert result == [('data',)]
        connection1.close()

        # Test to make sure there is only one data table after calling the function a second time.
        connection2 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkDataTable(connection2) == True
        cursor2 = connection2.cursor()
        cursor2.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="data";')
        result = cursor2.fetchall()

        assert result == [('data',)]

        # Clean up.
        connection2.close()
        self.deleteDatabase()

    def test_createDatum(self):
        # Test the ability of the model to create a datum.
        timestamp = Model.createTimeStamp()
        datumId = Model.createDatum(-10, 'test', timestamp, -10, -10)
        assert type(datumId) == int

        # Test the datum is in line with the database.
        connection = Model._Model__check_connection(-10, -10)
        cursor = connection.cursor()
        cursor.execute('SELECT datumId, sensor, datum, recordTimeStamp FROM data WHERE datumId = ?;', (datumId,))
        result = cursor.fetchall()

        assert result == [
            (1, -10, 'test', timestamp)
        ]

        assert self.checkTimestamp(timestamp) == True

        assumedResult = [
            (1, -10, 'test', timestamp)
        ]

        # Test more datums
        for i in range(100):
            datumId = Model.createDatum(3 - 7 * i % 9, f'test{i}', timestamp, -10, -10)
            assert type(datumId) == int

            assumedResult.append((datumId, 3 - 7 * i % 9, f'test{i}', timestamp))
        
        cursor.execute('SELECT datumId, sensor, datum, recordTimeStamp FROM data;')
        result = cursor.fetchall()
        
        assert result == assumedResult

        # Clean up.
        connection.close()
        self.deleteDatabase()
    
    def test_retrieveDatumById(self):
        # Test the ability of the model to retrieve a datum by id.
        timestamp = Model.createTimeStamp()
        datumId = Model.createDatum(-10, 'test by id', timestamp, -10, -10)

        datum = Model.retrieveDatumById(datumId, -10, -10)

        assert datum.getDatumId() == datumId
        assert datum.getSensor() == -10
        assert datum.getDatum() == 'test by id'
        assert datum.getRecordTimeStamp() == timestamp
    
        # Test more datums
        for i in range(100):
            timestamp = Model.createTimeStamp()
            datumId = Model.createDatum(3 - 7 * i % 9, f'test{i}', timestamp, -10, -10)

            datum = Model.retrieveDatumById(datumId, -10, -10)

            assert datum.getDatumId() == datumId
            assert datum.getSensor() == 3 - 7 * i % 9
            assert datum.getDatum() == f'test{i}'
            assert datum.getRecordTimeStamp() == timestamp

        self.deleteDatabase()
    
    def test_retrieveDataBySensor(self):
        # Test the ability of the model to retrieve a datum by sensor.
        timestamp = Model.createTimeStamp()
        datumId = Model.createDatum(-10, 'test by sensor', timestamp, -10, -10)

        data = Model.retrieveDataBySensor(-10, -10, -10)

        assert data[0].getDatumId() == datumId
        assert data[0].getSensor() == -10
        assert data[0].getDatum() == 'test by sensor'
        assert data[0].getRecordTimeStamp() == timestamp
    
        # Test more datums
        for i in range(100):
            timestamp = Model.createTimeStamp()
            datumId = Model.createDatum(3 - 7 * i % 9, f'test{i}', timestamp, -10, -10)

            data = Model.retrieveDataBySensor(3 - 7 * i % 9, -10, -10)

            datumInData = False

            for datum in data:
                if datum.getDatumId() == datumId and datum.getSensor() == 3 - 7 * i % 9:
                    datumInData = True
            
            assert datumInData == True
            
        self.deleteDatabase()

    def test_retrieveDataByTime(self):
        # Test the ability of the model to retrieve a datum by time.
        timestamp = Model.createTimeStamp()
        datumId = Model.createDatum(-10, 'test by time', timestamp, -10, -10)

        data = Model.retrieveDataByTime(timestamp - 1, timestamp, -10, -10)

        assert data[0].getDatumId() == datumId
        assert data[0].getSensor() == -10
        assert data[0].getDatum() == 'test by time'
        assert data[0].getRecordTimeStamp() == timestamp
    
        # Test more datums
        for i in range(100):
            timestamp = Model.createTimeStamp()
            datumId = Model.createDatum(i, f'test{i}', timestamp, -10, -10)

            data = Model.retrieveDataByTime(timestamp - 1, timestamp, -10, -10)

            datumInData = False

            for datum in data:
                if datum.getDatumId() == datumId and datum.getRecordTimeStamp() == timestamp:
                    datumInData = True
            
            assert datumInData == True
            
        self.deleteDatabase()
    
    '''
    ----------------------------------------------------------------------------
    Packet method tests
    ----------------------------------------------------------------------------
    '''
    def test__checkPacketsTable(self):
        # Test the ability of the model to check if the packets table exists.
        connection1 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkPacketsTable(connection1) == True
        
        cursor1 = connection1.cursor()
        cursor1.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="packets";')
        result = cursor1.fetchall()

        assert result == [('packets',)]
        connection1.close()

        # Test to make sure there is only one packets table after calling the function a second time.
        connection2 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkPacketsTable(connection2) == True
        cursor2 = connection2.cursor()
        cursor2.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="packets";')
        result = cursor2.fetchall()

        assert result == [('packets',)]

        # Clean up.
        connection2.close()
        self.deleteDatabase()

    def test_createPacket(self):
        # Test the ability of the model to create a packet.
        timestamp = Model.createTimeStamp()
        packetId = Model.createPacket('test', timestamp, -10, -10)

        assert type(packetId) == int

        # Test the packet is in line with the database.
        connection = Model._Model__check_connection(-10, -10)
        cursor = connection.cursor()
        cursor.execute('SELECT packetId, data, sendTime FROM packets WHERE packetId = ?;', (packetId,))
        result = cursor.fetchall()

        assert result == [
            (1, 'test', timestamp)
        ]

        assert self.checkTimestamp(timestamp) == True

        # Test more packets
        for i in range(100):
            timestamp = Model.createTimeStamp()
            packetId = Model.createPacket(f'data{i}', timestamp, -10, -10)

            assert type(packetId) == int

            cursor.execute('SELECT packetId, data, sendTime FROM packets WHERE packetId = ?;', (packetId,))
            result = cursor.fetchall()

            assert result == [
                (packetId, f'data{i}', timestamp)
            ]

        # Clean up.
        connection.close()
        self.deleteDatabase()
    
    def test_retrievePacketById(self):
        # Test the ability of the model to retrieve a packet by id.
        timestamp = Model.createTimeStamp()
        packetId = Model.createPacket('test by id', timestamp, -10, -10)

        packet = Model.retrievePacketById(packetId, -10, -10)

        assert packet.getPacketId() == packetId
        assert packet.getData() == 'test by id'
        assert packet.getSendTime() == timestamp
    
        # Test more packets
        for i in range(100):
            timestamp = Model.createTimeStamp()
            packetId = Model.createPacket(f'data{i}', timestamp, -10, -10)

            packet = Model.retrievePacketById(packetId, -10, -10)

            assert packet.getPacketId() == packetId
            assert packet.getData() == f'data{i}'
            assert packet.getSendTime() == timestamp

        self.deleteDatabase()
    
    def test_retrievePacketsBySendTime(self):
        # Test the ability of the model to retrieve a packet by time.
        timestamp = Model.createTimeStamp()
        packetId = Model.createPacket('test by time', timestamp, -10, -10)

        packets = Model.retrievePacketsBySendTime(timestamp - 1, timestamp, -10, -10)

        assert packets[0].getPacketId() == packetId
        assert packets[0].getData() == 'test by time'
        assert packets[0].getSendTime() == timestamp
    
        # Test more packets
        for i in range(100):
            timestamp = Model.createTimeStamp()
            packetId = Model.createPacket(f'data{i}', timestamp, -10, -10)

            packets = Model.retrievePacketsBySendTime(timestamp - 1, timestamp, -10, -10)

            packetInPackets = False

            for packet in packets:
                if packet.getPacketId() == packetId and packet.getSendTime() == timestamp:
                    packetInPackets = True

            assert packetInPackets == True

        self.deleteDatabase()
    
    def test_updatePacketSendTime(self):
        # Test the ability of the model to update a packet's send time.
        timestamp = Model.createTimeStamp()
        packetId = Model.createPacket('test by time', timestamp, -10, -10)
        
        assert Model.retrievePacketById(packetId, -10, -10).getSendTime() == timestamp

        Model.updatePacketSendTime(packetId, timestamp + 1, -10, -10)

        assert Model.retrievePacketById(packetId, -10, -10).getSendTime() == timestamp + 1

        # Test more packets
        for i in range(100):
            timestamp = Model.createTimeStamp()
            packetId = Model.createPacket(f'data{i}', timestamp, -10, -10)

            assert Model.retrievePacketById(packetId, -10, -10).getSendTime() == timestamp

            Model.updatePacketSendTime(packetId, timestamp + 1, -10, -10)

            assert Model.retrievePacketById(packetId, -10, -10).getSendTime() == timestamp + 1
        
        self.deleteDatabase()
    
    '''
    ----------------------------------------------------------------------------
    Task method tests
    ----------------------------------------------------------------------------
    '''
    def test__checkTasksTable(self):
        # Test the ability of the model to check if the tasks table exists.
        connection1 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkTasksTable(connection1) == True
        
        cursor1 = connection1.cursor()
        cursor1.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="tasks";')
        result = cursor1.fetchall()

        assert result == [('tasks',)]
        connection1.close()

        # Test to make sure there is only one tasks table after calling the function a second time.
        connection2 = Model._Model__check_connection(-10, -10)
        assert Model._Model__checkTasksTable(connection2) == True
        cursor2 = connection2.cursor()
        cursor2.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="tasks";')
        result = cursor2.fetchall()

        assert result == [('tasks',)]

        # Clean up.
        connection2.close()
        self.deleteDatabase()
    
    def test_createTask(self):
        # Test the ability of the model to create a task.
        addToQueueTime = Model.createTimeStamp()
        taskId = Model.createTask(0, -10, -1, -1, addToQueueTime, -1, -1, -1, -1, True, False, [], -10, -10)

        assert type(taskId) == int

        # Test the task is in line with the database.
        connection = Model._Model__check_connection(-10, -10)
        cursor = connection.cursor()
        cursor.execute('SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters FROM tasks WHERE taskId = ?;', (taskId,))
        result = cursor.fetchall()

        assert result == [
            (1, 0, -10, -1, -1, addToQueueTime, -1, -1, -1, -1, 1, 0, '')
        ]

        # Test more tasks
        for i in range(100):
            addToQueueTime = Model.createTimeStamp()
            scheduledRunTime = Model.createTimeStamp() + i
            expirationTime = Model.createTimeStamp() + 2 * i + 1
            taskId = Model.createTask(i, i - 10, -1, -1, addToQueueTime, scheduledRunTime, expirationTime, -1, -1, True, False, [], -10, -10)

            assert type(taskId) == int

            cursor.execute('SELECT taskId, priority, pluginId, previousTaskId, nextTaskId, addToQueueTime, scheduledRunTime, expirationTime, startTime, endTime, active, shouldImportOnStart, parameters FROM tasks WHERE taskId = ?;', (taskId,))
            result = cursor.fetchall()

            assert result == [
                (taskId, i, i - 10, -1, -1, addToQueueTime, scheduledRunTime, expirationTime, -1, -1, 1, 0, '')
            ]

        # Clean up.
        connection.close()
        self.deleteDatabase()
    
    def test_retrieveTaskById(self):
        # Test the ability of the model to retrieve a task by id.
        addToQueueTime = Model.createTimeStamp()
        taskId = Model.createTask(0, -10, -1, -1, addToQueueTime, -1, -1, -1, -1, True, False, [], -10, -10)

        task = Model.retrieveTaskById(taskId, -10, -10)

        assert task.getTaskId() == taskId
        assert task.getPriority() == 0
        assert task.getPluginId() == -10
        assert task.getPreviousTaskId() == -1
        assert task.getNextTaskId() == -1
        assert task.getAddToQueueTime() == addToQueueTime
        assert task.getScheduledRunTime() == -1
        assert task.getExpirationTime() == -1
        assert task.getStartTime() == -1
        assert task.getEndTime() == -1
        assert task.getActive() == True
        assert task.getShouldImportOnStart() == False
        assert task.getParameters() == ['']

        # Test more tasks
        for i in range(100):
            addToQueueTime = Model.createTimeStamp()
            scheduledRunTime = Model.createTimeStamp() + i
            expirationTime = Model.createTimeStamp() + 2 * i + 1
            taskId = Model.createTask(i, i - 10, -1, -1, addToQueueTime, scheduledRunTime, expirationTime, -1, -1, True, False, [], -10, -10)

            task = Model.retrieveTaskById(taskId, -10, -10)

            assert task.getTaskId() == taskId
            assert task.getPriority() == i
            assert task.getPluginId() == i - 10
            assert task.getPreviousTaskId() == -1
            assert task.getNextTaskId() == -1
            assert task.getAddToQueueTime() == addToQueueTime
            assert task.getScheduledRunTime() == scheduledRunTime
            assert task.getExpirationTime() == expirationTime
            assert task.getStartTime() == -1
            assert task.getEndTime() == -1
            assert task.getActive() == True
            assert task.getShouldImportOnStart() == False
            assert task.getParameters() == ['']

        # Clean up.
        self.deleteDatabase()
    
    def test_retrieveTasksByPluginId(self):
        # Test the ability of the model to retrieve tasks by plugin id.
        addToQueueTime = Model.createTimeStamp()
        taskId = Model.createTask(0, -12, -1, -1, addToQueueTime, -1, -1, -1, -1, True, False, [], -10, -10)

        tasks = Model.retrieveTasksByPluginId(-12, -10, -10)

        assert tasks[0].getTaskId() == taskId
        assert tasks[0].getPriority() == 0
        assert tasks[0].getPluginId() == -12
        assert tasks[0].getPreviousTaskId() == -1
        assert tasks[0].getNextTaskId() == -1
        assert tasks[0].getAddToQueueTime() == addToQueueTime
        assert tasks[0].getScheduledRunTime() == -1
        assert tasks[0].getExpirationTime() == -1
        assert tasks[0].getStartTime() == -1
        assert tasks[0].getEndTime() == -1
        assert tasks[0].getActive() == True
        assert tasks[0].getShouldImportOnStart() == False
        assert tasks[0].getParameters() == ['']

        # Test more tasks
        for i in range(100):
            addToQueueTime = Model.createTimeStamp()
            scheduledRunTime = Model.createTimeStamp() + i
            expirationTime = Model.createTimeStamp() + 2 * i + 1
            taskId = Model.createTask(i, (i - 10) % 17, -1, -1, addToQueueTime, scheduledRunTime, expirationTime, -1, -1, True, False, [], -10, -10)

            tasks = Model.retrieveTasksByPluginId((i - 10) % 17, -10, -10)

            taskInTasks = False

            for task in tasks:
                if task.getTaskId() == taskId and task.getPluginId() == (i - 10) % 17:
                    taskInTasks = True

            assert taskInTasks == True

        # Clean up.
        self.deleteDatabase()
