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
    grasp_translation = T_tag_world.translation + np.array([0, 0, -cfg['cube_size'] / 2])
    return RigidTransform(
        rotation=grasp_R,
        translation=grasp_translation,
        from_frame=T_ee_world.from_frame, to_frame=T_ee_world.to_frame
    )

if __name__ == "__main__":
    fa = FrankaArm()

    print('Reset with pose')
    fa.reset_pose()
    print('Opening Grippers')
    fa.open_gripper()


    T_ready_world = fa.get_pose()
    T_ball_world = RigidTransform(
        rotation= np.eye(3),
        translation= np.array([0.45108569, 0.07067022, 0.03280668]),
        from_frame= 'franka_tool_base',
        to_frame= 'world'
    )

    print('Finding closest orthogonal grasp')
    T_grasp_world = get_closest_grasp_pose(T_ball_world, T_ready_world)
    T_lift = RigidTransform(translation=[0, 0, 0.2], from_frame=T_ready_world.to_frame, to_frame=T_ready_world.to_frame)
    T_lift_world = T_lift * T_grasp_world

    print('Commanding robot')
    fa.goto_pose(T_lift_world, use_impedance=False)
    fa.goto_pose(T_grasp_world, use_impedance=False)
    fa.close_gripper()
    fa.goto_pose(T_lift_world, use_impedance=False)
    sleep(3)
    fa.goto_pose(T_grasp_world, use_impedance=False)
    fa.open_gripper()
    fa.goto_pose(T_lift_world, use_impedance=False)
    fa.goto_pose(T_ready_world, use_impedance=False)