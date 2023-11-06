from frankapy import FrankaArm
import numpy as np
from autolab_core import RigidTransform
from time import sleep

def subsample(data, rate=0.1):
    idx = np.random.choice(np.arange(len(data)), size=int(rate * len(data)))
    return data[idx]


def make_det_one(R):
    U, _, Vt = np.linalg.svd(R)
    return U @ np.eye(len(R)) @ Vt

def get_closest_grasp_pose(T_tag_world, T_ee_world):
    tag_axes = [
        T_tag_world.rotation[:,0], -T_tag_world.rotation[:,0],
        T_tag_world.rotation[:,1], -T_tag_world.rotation[:,1]
    ]
    x_axis_ee = T_ee_world.rotation[:,0]
    dots = [axis @ x_axis_ee for axis in tag_axes]
    grasp_x_axis = tag_axes[np.argmax(dots)]
    grasp_z_axis = np.array([0, 0, -1])
    grasp_y_axis = np.cross(grasp_z_axis, grasp_x_axis)
    grasp_R = make_det_one(np.c_[grasp_x_axis, grasp_y_axis, grasp_z_axis])
    grasp_translation = T_tag_world.translation + np.array([0, 0, 0.05 / 2])
    return RigidTransform(
        rotation=grasp_R,
        translation=grasp_translation,
        from_frame=T_ee_world.from_frame, to_frame=T_ee_world.to_frame
    )


def pickUp(robot, x, y):

    T_ready_world = robot.get_pose()
    T_ball_world = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([x, y, 0.02]),
        from_frame= 'franka_tool_base',
        to_frame= 'world'
    )

    print('Finding closest orthogonal grasp')
    T_grasp_world = get_closest_grasp_pose(T_ball_world, T_ready_world)

    print(T_grasp_world)

    T_lift = RigidTransform(translation=[0, 0, 0.2], from_frame=T_ready_world.to_frame, to_frame=T_ready_world.to_frame)
    T_lift_world = T_lift * T_grasp_world

    print(T_lift_world)

    robot.goto_pose(T_lift_world, duration=2, use_impedance=False)

    robot.open_gripper()

    robot.goto_pose(T_grasp_world, duration=2, use_impedance=False)
    robot.close_gripper()
    robot.reset_pose(duration=2)


def place(robot, x, y):

    T_ready_world = robot.get_pose()
    T_ball_world = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([x, y, 0.03]),
        from_frame= 'franka_tool_base',
        to_frame= 'world'
    )

    T_grasp_world = get_closest_grasp_pose(T_ball_world, T_ready_world)

    robot.goto_pose(T_grasp_world, use_impedance=False)
    robot.open_gripper()
    robot.reset_pose(duration=2)


def pick_and_place(x_from, y_from, x_to, y_to):
    fa = FrankaArm()
    fa.reset_pose(duration=2)
    pickUp(fa, x_from, y_from)
    place(fa, x_to, y_to)


if __name__ == "__main__":

    start = (0.45108569+0.10, 0.07067022)
    target = (0.45108569 - 0.05, 0.07067022)

    while (True):
        pick_and_place(start[0], start[1], target[0], target[1])
        start, target = target, start
        