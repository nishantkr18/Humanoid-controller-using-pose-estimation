import pybullet
import cv2
import pybullet_data
import os
import time
import math
import numpy as np
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

file_name = currentdir + "/humanoid.urdf"
pybullet.connect(pybullet.GUI)
pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
pybullet.loadURDF("plane.urdf", 0, 0, 0)
robot = pybullet.loadURDF(file_name, 0, 0, 0.5)
cap = cv2.VideoCapture(0)
pybullet.setGravity(0, 0, 0)
numJoints = pybullet.getNumJoints(robot)  # 25
action = [i for i in range(numJoints)]

scale = 100.0


def nothing(x):
    pass


cv2.namedWindow("controller with scale" + str(scale))
# create trackbars for joints
for i in range(numJoints):
    cv2.createTrackbar(str(i), "controller with scale" + str(scale), 00, 100, nothing)
# create switch for ON/OFF functionality
switch = "0 : OFF \n1 : ON"
cv2.createTrackbar(switch, "controller with scale" + str(scale), 0, 1, nothing)

while 1:
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    actions = [
        cv2.getTrackbarPos(str(i), "controller with scale" + str(scale)) / scale
        for i in range(numJoints)
    ]
    s = cv2.getTrackbarPos(switch, "controller with scale" + str(scale))
    for i in range(numJoints):
        pybullet.setJointMotorControl2(
            robot, i, pybullet.POSITION_CONTROL, targetPosition=actions[i], force=500
        )
    pybullet.stepSimulation()


cv2.destroyAllWindows()
