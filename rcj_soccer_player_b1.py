# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils

from intercepts import interceptCalculator
from CoordinateRecalculator import coor_recalc, robot_pos_recalc
######

# Feel free to import built-in libraries
import math

#robot class
class MyRobot(RCJSoccerRobot):
    def run(self):
        #create interceptcalc instance
        intercept_c = interceptCalculator(3)

        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                
                robot_pos = robot_pos_recalc(data[self.name])
                # Get & recalculate the position of the ball
                #print(data['ball']['x'], data['ball']['y'])
                ball_pos = coor_recalc(data['ball']['x'], data['ball']['y'])
                #push ball pos into intercept calculator
                intercept_c.pushPoint(ball_pos)
                print(ball_pos)
                intercept_c.calculateOptimumIntercept(robot_pos))

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:
                    left_speed = -5
                    right_speed = -5
                else:
                    left_speed = direction * 4
                    right_speed = direction * -4

                # Set the speed to motors
                self.left_motor.setVelocity(10)
                self.right_motor.setVelocity(-10)


my_robot = MyRobot()
my_robot.run()
