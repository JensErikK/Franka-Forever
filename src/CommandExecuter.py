


class CommandExecuter():

    def __init__(self) -> None:
        pass

    def GetTargetFromCommand(self, command: str) -> str:
        return "Bowl"
    

    def GetObjectClassesToPickUp(self, command: str):
        return ["Sports Ball"]
    

    def FindObjectsWithPositions(self):
        return [("Sports Ball", [1,2,3]), ("Bowl", [2,3,4])]
    
    def PickAndPlace(self, pickUpPos, placePos):
        return print(f"PickFrom: {pickUpPos}, PlaceTo: {placePos}")


    def Execute(self, command: str):
            
            placeTarget = self.GetTargetFromCommand(command)
            objectTypesToPickup = self.GetObjectClassesToPickUp(command)


            objectPositions = self.FindObjectsWithPositions()


            targetPosition = [t[1] for t in objectPositions if t[0] == placeTarget][0]
            pickUpPositions = [t[1] for t in objectPositions if t[0] in objectTypesToPickup]

            if not targetPosition:
                return


            for position in pickUpPositions:
                self.PickAndPlace(position, targetPosition)


if __name__ == "__main__":
    CommandExecuter().Execute("Heisann")