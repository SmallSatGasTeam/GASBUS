# Objects

Data in Flight Logic is stored in objects to standardize use. An object class represents a table in the database and an instance of an object represents a row in the table.

## Log

The log object is used to create and store all logs on the satellite. Each log is organized into a log level. The log levels help organize information allowing the user to see what is most important. The log levels are:

| Log Level | Description |
| --------- | ----------- |
| 100       | Error       |
| 200       | Warning     |
| 300       | Info        |
| 400       | Debug       |

### Usage

Logging is a common task on the satellite. It is intended to be simple and easy to use. Each log level has a corresponding function that can be used to log information.

1.  Error

        from objects.log import Log
        Log.newError("[Error message]", runningTaskId, runningPluginId)

2.  Warning

        from objects.log import Log
        Log.newWarning("[Warning message]", runningTaskId, runningPluginId)

3.  Info

            from objects.log import Log
            Log.newInfo("[Info message]", runningTaskId, runningPluginId)

4.  Debug

            from objects.log import Log
            Log.newDebug("[Debug message]", runningTaskId, runningPluginId)

### Printing

The log object has some class variables designating whether each log level should be printed to the console. These variables exist at the top of the log class.

    PRINT_ERROR = True
    PRINT_WARNING = True
    PRINT_INFO = True
    PRINT_DEBUG = False

## Task

The task object is used to encapsulate a plugin and its parameters. The task object contains all the information necessary to schedule and prioritize the running of the corresponding plugin.

Usage of the task object is described in relation to the task manager in the [Flight Logic README](../README.md#plugins-and-tasks).

## Datum

The datum object is used to store all data collected by the satellite. The data can then be retrieved by sensor or from a specific time range.

### Usage

Creating a new datum is accomplished by importing the datum class and then calling the newDatum function.

    from objects.datum import Datum
    newDatum = Datum.newDatum(sensor, datum, recordTimeStamp, runTaskId, runPluginId)

Datums are retrieved through the model.

    from model import Model
    Model.retrieveDatumById(datumId, runTaskId, runPluginId)

## Packet

The packet object is used to store packets to be transmitted from the satellite.

### Usage

Creating a new packet is accomplished by importing the packet class and then calling the newPacket function.

    from objects.packet import Packet
    newPacket = Packet.newPacket(data, sendTime, runTaskId, runPluginId)

Packets are retrieved through the model.

    from model import Model
    Model.retrievePacketById(packetId, runTaskId, runPluginId)
