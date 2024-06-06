
from openai import OpenAI
from RobotControl import start_robot, reset_pose, pick_left_bowl, pick_right_bowl, place_left_bowl, place_right_bowl, place, dance


class CommandExecuter():

    IsLooping = False
    IsExecuting = False

    def __init__(self) -> None:
        if not CommandExecuter.IsExecuting:
            self.robot = start_robot()
        
    async def Execute(self, command: str):
        if CommandExecuter.IsExecuting:
            return

        CommandExecuter.IsExecuting = True
        await self._parseAndPerformCommand(command)
        CommandExecuter.IsExecuting = False
    
    async def ExecuteLoopStep(self, step: int):
        num_pick_before_switch = 2
        if step % (2*num_pick_before_switch) < num_pick_before_switch:    
            await pick_left_bowl(self.robot)
            await place_right_bowl(self.robot)
        else:
            await pick_left_bowl(self.robot)
            await place_right_bowl(self.robot)

        return

    async def _parseAndPerformCommand(self, command: str):
        
        if command.lower() == "reset":
            await reset_pose(self.robot)
            return

        if command.lower() == "stand_loop":
            await self._execute_loop()
            return

        parsed_command = self._parse_command(command)

        print(parsed_command)

        if "stressball" in parsed_command.lower():
            await pick_left_bowl(self.robot)
            await place(self.robot)
            return
        
        if "candy" in parsed_command.lower():
            await pick_right_bowl(self.robot)
            await place(self.robot)
            return
        
        await dance(self.robot)
    
    def _parse_command(self, command: str) -> str:
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",\
                "content": "You will be given a command. \
                 Your task is to figure out if the command asks for a stress ball or candy. \
                 Respond with \"StressBall\" if they want a stressball and \"Candy\" if they want candy. \
                 If they are asking for something else tell them you cant give them what they are asking for."},
                {"role": "user", "content": command}
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content


    # async def _execute_loop(self):
    #     CommandExecuter.IsLooping = True
    #     num_pick_before_switch = 2

    #     while CommandExecuter.IsLooping:
    #         for i in range(2*num_pick_before_switch):
    #             if i < num_pick_before_switch:    
    #                 await pick_left_bowl(self.robot)
    #                 await place_right_bowl(self.robot)
    #             else:
    #                 await pick_left_bowl(self.robot)
    #                 await place_right_bowl(self.robot)
    #             if not CommandExecuter.IsLooping:
    #                 break

    #     await reset_pose(self.robot)
    #     return

    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print(exception_type or "")
        print(exception_value or "")
        print(exception_traceback or "")


if __name__ == "__main__":
    CommandExecuter().Execute("reset")