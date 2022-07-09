import asyncio
import heapq as hq
import sys
import DiscoverTask
import time

class taskManager:
    def __init__(self):
        self.FakeDataBase = []
        self.__tasks = []
        self.__discovered_plugins = DiscoverTask.getTasks()
        for task in self.__discovered_plugins:
            task_obj = self.__discovered_plugins[task].creat_Task()
            self.__tasks.append((task_obj.getPriority(), task_obj))
        hq.heapify(self.__tasks)
        
    
    async def start_All_Task(self):
        print("Task exicution started")
        while(True):
            if(len(self.__tasks) == 0):
                await asyncio.sleep(0.2)
            task = hq.heappop(self.__tasks)[1]
            if(task.schedula == 1):
                 self.FakeDataBase.append([task.getTaskUID, time.time, task.schedula[1], task])
            task.startTask()
            await asyncio.sleep(0.1)
            

    async def schedular(self):
        print("Schedular started")
        while (True):
            if(len(self.FakeDataBase) == 0):
                await asyncio.sleep(0.20)
            print(self.FakeDataBase)
            if(time.time <= self.FakeDataBase[0][1] + self.FakeDataBase[0][2]):
                self.__tasks.append((self.FakeDataBase[0][3].getPriority(), self.FakeDataBase[0][3]))
            await asyncio.sleep(0.1)

            



async def main():
    tm = taskManager()
    run=[]
    run.append(asyncio.create_task(tm.start_All_Task()))
    run.append(asyncio.create_task(tm.schedular()))
    
if __name__ == "__main__":
    asyncio.run(main())
    while(True):
        pass