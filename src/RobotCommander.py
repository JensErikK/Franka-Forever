import aiohttp
import urllib.parse

class RobotCommander():

    IsLooping = False
    IsExecuting = False

    async def Execute(self, command: str):
        if RobotCommander.IsExecuting:
            return

        RobotCommander.IsExecuting = True

        if (command.lower() == "show_loop"):
            return await self.ExecuteLoop()

        encodedCommand = urllib.parse.quote(command)
        await self._call_robot(f"http://127.0.0.1:5001/execute?command={encodedCommand}")
       
        RobotCommander.IsExecuting = False
        return "Command Executed"
    
    async def ExecuteLoop(self):
        RobotCommander.IsLooping = True
        step = 0

        while RobotCommander.IsLooping:
            await self._call_robot(f"http://127.0.0.1:5001/executeloop?step={step}")
            step +=1

        RobotCommander.IsExecuting = False
        return "Looping Complete"

    async def _call_robot(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    print(data)
            return True
        except:
            return False


    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print(exception_type or "")
        print(exception_value or "")
        print(exception_traceback or "")
