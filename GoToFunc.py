import math
import utils
import time

def goTo(Dest_pos, robot_pos, robot_angle):
    YAxisToDest = Dest_pos[0][1]-robot_pos["y"]
    XAxisToDest = Dest_pos[0][0]-robot_pos["x"]
    angle = math.atan2(YAxisToDest, XAxisToDest)

    distanceToSpot = math.sqrt(math.pow(YAxisToDest, 2) + math.pow(XAxisToDest, 2))                   
    #shiftAngle =angle-robot_angle
    if angle < 0:
        angle = 2 * math.pi + angle

    if robot_angle < 0:
        robot_angle = 2 * math.pi + robot_angle

    robotDestAngle = math.degrees(angle + robot_angle)
    robotDestAngle -= 90
    if robotDestAngle > 360:
        robotDestAngle -= 360
    
    #create your own get_direction so that it turns only once from beginning
    direction = utils.get_direction(robotDestAngle)
    #print(direction)
    RotateToGoal=False
    ForwardSpeed =10
    RotationSpeed =9
    if(distanceToSpot <=0.15):
        ForwardSpeed /=2 

    if(distanceToSpot <=0.09):
        ForwardSpeed =0;
        RotateToGoal=True
        t2= time.time()
       

    if(RotateToGoal):
        RotationSpeed =0
        #RotateToGoal() 
    
    return [direction, ForwardSpeed, RotationSpeed, distanceToSpot]