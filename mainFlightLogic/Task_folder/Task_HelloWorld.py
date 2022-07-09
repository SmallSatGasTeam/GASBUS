from task import task
import asyncio

def creat_Task():
    return helloWorldTask(10, message = "Hello world\nTaryn is amazing ;)")

class helloWorldTask(task):
    def __init__(self, priority, message):
        self.__priority = priority
        self.__message = message

    def getPriority(self):
        return self.__priority

    def startTask(self):
        print(self.__message)
        #await(1000)

    def tearDown(self):
        pass #pass beacuese we dont have a tear down.

    def schedula(self):
        return (1, 1000)
    def getTaskUID(self):
        return 0
