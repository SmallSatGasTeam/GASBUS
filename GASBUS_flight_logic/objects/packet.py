'''
This is the "packet" object.

The packet object requires a datum and a send time. The packet object also receives a packetId from the database. The datum is the piece of information to be transmitted for the packet. The send time is the time the packet is to be sent.

packetId is an integer available for getting.
datum is a string available for getting.
sendTime is an integer available for getting and setting.
'''

class Packet:
    '''
    ----------------------------------------------------------------------------
    Constructors

    These methods are used to instantiate new packets.
    ----------------------------------------------------------------------------

    default constructor - never use this outside of the class, use the class methods instead
    '''
    def __init__(self, packetId, data, sendTime):
        self.__packetId = packetId
        self.__data = data
        self.__sendTime = sendTime

    '''
    public Packet.newPacket(data: string, sendTime: integer) -> Packet

    This is the class method for creating a new packet.
    '''
    @classmethod
    def newPacket(cls, data, sendTime, runTaskId, runPluginId):
        from model import Model # import statement here to avoid circular import
        packetId = Model.createPacket(data, sendTime, runTaskId, runPluginId)

        return cls(packetId, data, sendTime)

    '''
    public Packet.packetWithId(packetId: integer, data: string, sendTime: integer) -> Packet

    This is the class method for creating a new packet object for a packet that has already been created in the database.
    '''
    @classmethod
    def packetWithId(cls, packetId, data, sendTime):

        return cls(packetId, data, sendTime)

    '''
    ----------------------------------------------------------------------------
    Getters

    These methods are used to access the values of the packet object.
    ----------------------------------------------------------------------------
    '''
    def getPacketId(self):
        return self.__packetId # integer

    def getData(self):
        return self.__data # string

    def getSendTime(self):
        return self.__sendTime # integer

    '''
    ----------------------------------------------------------------------------
    Setters
    
    These methods are used to set the values of the packet object.
    ----------------------------------------------------------------------------
    '''
    def setSendTime(self, sendTime, runTaskId, runPluginId):
        # update the send time in the model
        from model import Model # import statement here to avoid circular import
        if Model.updatePacketSendTime(self.__packetId, sendTime, runTaskId, runPluginId):
            # update the send time in the packet object
            self.__sendTime = sendTime
            return True

        return False
    
    '''
    ----------------------------------------------------------------------------
    Visual methods
    
    These methods determine how the packet object will be displayed.
    ----------------------------------------------------------------------------
    '''
    # string function
    def __str__(self):
        return f'Packet {self.__packetId} will send "{self.__datum}" at {self.__sendTime}'

    # represent function
    def __repr__(self):
        return f'Packet(packetId={self.__packetId}, datum="{self.__datum}", sendTime={self.__sendTime})'