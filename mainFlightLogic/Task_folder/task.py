
import asyncio

class task:
    
    def __init__(self):
        '''
        Task set up function
        '''
        raise Exception("No __init__ function defined for child task")
    
    
    def getPriority(self):
        '''
        Returns task priority, 0 is exitucted first
        '''
        raise Exception("No getPriority function defined for child task")

    
    def startTask(self):
        '''
        Starts task exitcution
        '''
        raise Exception("No startTask function defined for child task")
    
    def tearDown(self):
        '''
            destroys task, and all objects that it holds
        '''
        raise Exception("No tearDown function defined for child task")

    async def startTask(self):
        '''
        Starts task exitcution
        '''
        raise Exception("No async startTask function defined for child task")

   
    async def tearDown(self):
        '''
            destroys task, and all objects that it holds
        '''
        raise Exception("No async tearDown function defined for child task")
    
    def isAsync(self):
        '''
            returns bool if the function is async or not
        '''
        raise Exception("No  isAsync function defined for child task")

    def schedula(self):
        '''
<<<<<<< HEAD
            returns a touple, index 0: 1/0 1= repeat, 0=run once, index 1: int millia seconds interval to repate at
=======
            returns a trouphat3oe8hgq[oiwegd[0u 23nw[eole, index 0: 1/0 1= repeat, 0=run once, index 1: int millia seconds interval to repate at
>>>>>>> 5f15c41c903a1a93b9b87a47507da6f816eca1f9
        '''
        raise Exception("No  schedula function defined for child task")
    
    def getTaskUID(self):
        '''
            returns the task unique ID
        '''
        raise Exception("No  schedula function defined for child task")