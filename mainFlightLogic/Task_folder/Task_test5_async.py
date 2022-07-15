from task import task
import asyncio
import time

def creat_Task():
    return helloWorldTask(510)

class helloWorldTask(task):
    def __init__(self, priority):
        self.__priority = priority

    def getPriority(self):
        return self.__priority

    async def startTask(self):
        while(True):
            print("Test 5: This is an aysnc func " + str(time.time()))
            await asyncio.sleep(1)

    async def tearDown(self):
        await asyncio.sleep(1)
        pass #pass beacuese we dont have a tear down.
    
    def schedula(self):
        return (0, -1)

    def isAsync(self):
        return True