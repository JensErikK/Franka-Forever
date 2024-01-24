
from RobotControl import start_robot, reset_pose

class CommandExecuter():

    def __init__(self) -> None:
        self.robot = start_robot()
        pass

    async def Execute(self, command: str):
            
        if command.lower() == "reset":
            await reset_pose(self.robot)
            return
        
        await self.Perform_detect_and_pick(command)

    def Perform_detect_and_pick(self, command: str):
        placeTarget = self.GetTargetFromCommand(command)
        objectTypesToPickup = self.GetObjectClassesToPickUp(command)

        objectPositions = self.FindObjectsWithPositions()


        targetPosition = [t[1] for t in objectPositions if t[0] == placeTarget][0]
        pickUpPositions = [t[1] for t in objectPositions if t[0] in objectTypesToPickup]

        if not targetPosition:
            return

        for position in pickUpPositions:
            self.PickAndPlace(position, targetPosition)

    def GetTargetFromCommand(self, command: str) -> str:
        return "Bowl"
    
    def GetObjectClassesToPickUp(self, command: str):
        return ["Sports Ball"]
    

    def FindObjectsWithPositions(self):
        return [("Sports Ball", [1,2,3]), ("Bowl", [2,3,4])]
    
    def PickAndPlace(self, pickUpPos, placePos):
        return print(f"PickFrom: {pickUpPos}, PlaceTo: {placePos}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print(exception_type or "")
        print(exception_value or "")
        print(exception_traceback or "")


if __name__ == "__main__":
    CommandExecuter().Execute("reset")