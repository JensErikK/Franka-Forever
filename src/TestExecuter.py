
from time import sleep

class CommandExecuter():

    IsLooping = False
    IsExecuting = False

    async def Execute(self, command: str):
        if CommandExecuter.IsExecuting:
            print("Already executing")
            return

        CommandExecuter.IsExecuting = True
        await self._parseAndPerformCommand(command)

        CommandExecuter.IsExecuting = False
        return "Execution Complete"

    async def _parseAndPerformCommand(self, command: str):
        
        if command.lower() == "reset":
            print("Reseting pose")
            sleep(3)
            return

        if command.lower() == "show_loop":
            print("Starting show loop")
            await self._execute_loop()
            return
        
        print(f"Executing {command}")
        sleep(4)
        return "Command executed"


    async def _execute_loop(self):
        CommandExecuter.IsLooping = True
        while CommandExecuter.IsLooping:
            print("Starting new show loop")
            sleep(5)

        return "Looping Done"

    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print(exception_type or "")
        print(exception_value or "")
        print(exception_traceback or "")


if __name__ == "__main__":
    CommandExecuter().Execute("reset")