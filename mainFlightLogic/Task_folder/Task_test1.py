from task import task
import asyncio

def creat_Task():
    return helloWorldTask(100)

class helloWorldTask(task):
    def __init__(self, priority):
        self.__priority = priority

    def getPriority(self):
        return self.__priority

    def startTask(self):
        print("Test 1")
        #await(1000)

    async def tearDown(self):
        await(1000)
        pass #pass beacuese we dont have a tear down.

    #creating a merge conflit