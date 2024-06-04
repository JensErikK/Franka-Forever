
from openai import OpenAI
from RobotControl import start_robot, reset_pose, pick_left_bowl, pick_right_bowl, place, dance

class CommandExecuter():

    def __init__(self) -> None:
        self.robot = start_robot()
        pass

    async def Execute(self, command: str):
        
        if command.lower() == "reset":
            await reset_pose(self.robot)
            return

        parsed_command = self.parse_command(command)

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
    
    def parse_command(self, command: str) -> str:
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


    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print(exception_type or "")
        print(exception_value or "")
        print(exception_traceback or "")


if __name__ == "__main__":
    CommandExecuter().Execute("reset")