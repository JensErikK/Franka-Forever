
from frankapy import FrankaArm


def start_robot() -> FrankaArm:
    print("Starting Robot")
    return FrankaArm()

def reset_pose():

    fa = start_robot()

    print("Reseting Robot to defulat pose")
    fa.reset_joints()
    fa.open_gripper()

if __name__ == "__main__":
    reset_pose()