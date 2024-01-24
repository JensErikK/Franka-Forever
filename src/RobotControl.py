
from frankapy import FrankaArm
from autolab_core import RigidTransform
import numpy as np

def start_robot() -> FrankaArm:
    print("Starting Robot")
    return FrankaArm()

async def reset_pose(fa: FrankaArm):

    print("Reseting Robot to defulat pose")
    fa.reset_joints()
    fa.open_gripper()

    await move_left(fa)


async def move_left(fa: FrankaArm):

    T_delta = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0, -0.25, 0]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta)

if __name__ == "__main__":
    reset_pose()