import pybullet as p
import cv2
import pybullet_data
import os
import time
import math
import numpy as np
import inspect

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))

file_name = currentdir+"/humanoid.urdf"
print(file_name)
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF( "plane.urdf", 0, 0, 0)
robot = p.loadURDF(file_name,0,0,1)
# p.resetBasePositionAndOrientation(robot, 0, 0, 1)
cap=cv2.VideoCapture(0)
p.setGravity(0, 0, -10)
while True:
	_, image=cap.read()
	hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	red1_l=np.array([75,50,100])
	red1_u=np.array([90,255,255])
	mask=cv2.inRange(hsv,red1_l,red1_u)
	masked_img=cv2.bitwise_and(hsv,hsv,mask=mask)
	cv2.imshow('img',masked_img)
	cnt_green,im2=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	present=0
	for c_red in cnt_green:
		area=cv2.contourArea(c_red)
		if area>2:
			present=1
			print("there")
	
	if (present==1):
		targetVel = 10
		for joint in range(2, 6):
			p.setJointMotorControl2(robot, joint, p.VELOCITY_CONTROL, targetVelocity =targetVel,force = 5000)
	else:		
		targetVel = 0
		for joint in range(2, 6):
			p.setJointMotorControl2(robot, joint, p.VELOCITY_CONTROL, targetVelocity =targetVel,force = 500)
	p.stepSimulation()			
			
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()

	# p.stepSimulation()