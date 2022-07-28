'''
This is the "datum" object.

The datum object requires a sensor, a datum, and a record time stamp. The datum object also receives a datumId from the database. The sensor indicates which sensor recorded the datum. The datum is the piece of information recorded by the sensor. The record time stamp is the time the datum was recorded by the sensor.

datumId is an integer available for getting.
sensor is an integer available for getting.
datum is a string available for getting.
recordTimeStamp is an integer available for getting.
'''

class Datum:
    # class variables
    data = [] # a list of all instantiated data

    '''
    ----------------------------------------------------------------------------
    Constructors

    These methods are used to instantiate new data.
    ----------------------------------------------------------------------------

    default constructor - never use this outside of the class, use the class methods instead
    '''
    def __init__(self, datumId, sensor, datum, recordTimeStamp):
        self.__datumId = datumId
        self.__sensor = sensor
        self.__datum = datum
        self.__recordTimeStamp = recordTimeStamp

        Datum.data.append(self)

    '''
    public Datum.newDatum(sensor: integer, datum: string, recordTimeStamp: integer, runTaskId: integer, runPluginId: integer) -> Datum

    This is the class method for creating a new datum.
    '''
    @classmethod
    def newDatum(cls, sensor, datum, recordTimeStamp, runTaskId, runPluginId):
        from model import Model # import statement here to avoid circular import
        datumId = Model.createDatum(sensor, datum, recordTimeStamp, runTaskId, runPluginId)

        return cls(datumId, sensor, datum, recordTimeStamp)

    '''
    public Datum.datumWithId(datumId: integer, sensor: integer, datum: string, recordTimeStamp: integer) -> Datum

    This is the class method for creating a new datum object for a datum that has already been created in the database. If a datum with the given datumId already exists, it will be returned instead of creating a new datum object to avoid synchronization issues. Otherwise, a new datum object will be created.
    '''
    @classmethod
    def datumWithId(cls, datumId, sensor, datum, recordTimeStamp):
        # check if a datum with the given datumId already exists to avoid duplicates and synchronization issues
        datum = cls.__checkDataForId(datumId)
        if datum is not None:
            return datum
        
        return cls(datumId, sensor, datum, recordTimeStamp)

    '''
    private static Datum.__checkDataForId(datumId: integer) -> Datum | None

    Checks to see if a datum with a given datumId has already been created. If it has, it will be returned.
    '''
    @staticmethod
    def __checkDataForId(datumId):
        for datum in Datum.data:
            if datum.getDatumId() == datumId:
                return datum
        return None

    '''
    ----------------------------------------------------------------------------
    Getters

    These methods are used to access the values of the datum object.
    ----------------------------------------------------------------------------
    '''
    def getDatumId(self):
        return self.__datumId # integer
    
    def getSensor(self):
        return self.__sensor # integer
    
    def getDatum(self):
        return self.__datum # string
    
    def getRecordTimeStamp(self):
        return self.__recordTimeStamp # integer

    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the datum object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        return f'Datum {self.__datumId} from sensor {self.__sensor} is "{self.__datum}" recorded at {self.__recordTimeStamp}'

    # represent function
    def __repr__(self):
        return f'Datum(datumId={self.__datumId}, sensor={self.__sensor}, datum="{self.__datum}", recordTimeStamp={self.__recordTimeStamp})'