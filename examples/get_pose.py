from frankapy import FrankaArm

if __name__ == "__main__":
    fa = FrankaArm()

    T_ready_world = fa.get_pose()

    print(T_ready_world)
    