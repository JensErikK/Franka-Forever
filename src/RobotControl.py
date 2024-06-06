
from frankapy import FrankaArm
from autolab_core import RigidTransform
import numpy as np

def start_robot() -> FrankaArm:
    print("Starting Robot")
    return FrankaArm()

async def reset_pose(fa: FrankaArm):

    fa.reset_joints()
    fa.open_gripper()

async def open_gripper(fa: FrankaArm):
    fa.open_gripper()

async def pick_left_bowl(fa: FrankaArm, reset_before_pick=True):

    if (reset_before_pick):
        await reset_pose(fa)
    else:
        await open_gripper(fa)
    
    T_delta_left_bowl = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0, -0.25, -0.40]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta_left_bowl)
    fa.close_gripper()
    fa.reset_pose()

async def pick_right_bowl(fa: FrankaArm, reset_before_pick=True):

    if (reset_before_pick):
        await reset_pose(fa)
    else:
        await open_gripper(fa)
    
    T_delta_left_bowl = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0, 0.25, -0.40]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta_left_bowl)
    fa.close_gripper()
    fa.reset_pose()

async def place_left_bowl(fa: FrankaArm):

    T_delta_left_bowl = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0, -0.25, -0.35]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta_left_bowl)
    fa.open_gripper()
    fa.reset_pose()

async def place_right_bowl(fa: FrankaArm):
    
    T_delta_left_bowl = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0, 0.25, -0.35]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta_left_bowl)
    fa.open_gripper()
    fa.reset_pose()


async def dance(fa: FrankaArm):

    await reset_pose(fa)
    
    T_delta_left_bowl = RigidTransform(
        rotation= np.array([    [0.2588190,  0.0000000,  0.9659258],
                                [0.0000000,  1.0000000,  0.0000000],
                                [-0.9659258,  0.0000000, 0.2588190] ]),
        translation= np.array([0.10, 0, 0.15]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta_left_bowl)
    
    fa.close_gripper()
    fa.open_gripper()
    fa.close_gripper()
    
    await reset_pose(fa)


async def place(fa: FrankaArm):

    T_delta_left_bowl = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0.20, 0, -0.15]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta_left_bowl)
    fa.open_gripper()
    fa.reset_pose()


async def move_left(fa: FrankaArm):

    T_delta = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0, -0.25, 0]),
        from_frame= 'world',
        to_frame= 'world'
    )

    fa.goto_pose_delta(T_delta)

if __name__ == "__main__":
    dance(FrankaArm())