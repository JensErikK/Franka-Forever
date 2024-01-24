
from RobotControl import reset_pose

class CommandExecuter():

    def __init__(self) -> None:
        pass

    def Execute(self, command: str):
            
        if command.lower() == "reset":
            reset_pose()
            return
        
        self.Perform_detect_and_pick(command)

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


if __name__ == "__main__":
    CommandExecuter().Execute("reset")