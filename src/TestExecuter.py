
from time import sleep

class CommandExecuter():

    async def Execute(self, command: str):

        await self._parseAndPerformCommand(command)

        return "Execution Complete"

    async def ExecuteLoopStep(self, step: int):
        print(f"Running loop step {step}")
        sleep(5)
        return

    async def _parseAndPerformCommand(self, command: str):
        
        if command.lower() == "reset":
            print("Reseting pose")
            sleep(3)
            return
        
        print(f"Executing {command}")
        sleep(4)
        return "Command executed"
    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print(exception_type or "")
        print(exception_value or "")
        print(exception_traceback or "")


if __name__ == "__main__":
    CommandExecuter().Execute("reset")