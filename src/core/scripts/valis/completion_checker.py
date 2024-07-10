# processed masks overlaps rigid registration non_rigid_registration data

import os
import time


def check_completion():
    path = "/root/Documents/dummyOutput2/dummy2/"
    completion = 0
    rigid_array = ["processed", "masks", "overlaps", "rigid_registration", "data"]
    non_rigid_array = rigid_array.copy()
    non_rigid_array.insert(-1, "non_rigid_registration")
    iter = 0

    while completion < 100:
        if os.path.exists(path + rigid_array[iter]):
            iter += 1
            completion += 20
            print("\n************\n" + str(completion) + "%\n************\n")
        time.sleep(.5)


if __name__ == "__main__":
    check_completion()
