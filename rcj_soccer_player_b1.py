# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils

from intercepts import interceptCalculator, color
from CoordinateRecalculator import coor_recalc, robot_pos_recalc
from GoToFunc import goTo

######

INTERCEPT_CONST = 0.03

# Feel free to import built-in libraries
import math
#robot class
class MyRobot(RCJSoccerRobot):
    def role_decision(self):
        intercept-calc = interceptCalculator(3)
        
        ball_pos = coor_recalc(data['ball']['x'], data['ball']['y'])

        b1 = {"x":data["B1"]["x"],"y": data["B1"]["y"]}
        b2 = {"x":data["B2"]["x"],"y": data["B2"]["y"]}
        b3 = {"x":data["B3"]["x"],"y": data["B3"]["y"]}

        intercept_calc.pushPoint(ball_pos)

        intercepts = {"b1":,"b2":,"b3":}
        intercepts["b1"] = intercept_calc.calculateOptimumIntercept(b1, sample_count=200)
        intercepts["b2"] = intercept_calc.calculateOptimumIntercept(b2, sample_count=200)
        intercepts["b3"] = intercept_calc.calculateOptimumIntercept(b3, sample_count=200)

        ts = {"b1":intercepts["b1"]["t"],"b2":intercepts["b2"]["t"],"b3":intercepts["b3"]["t"]}
        
        if ts["b1"] == min(ts.values):
            attacker = 1
            if b2[x] > b3[x]:
                goalie = 2
                support = 3
            else:
                goalie = 3
                support = 2
        elif ts["b2"] == min(ts.values):
            attacker = 2
            if b1[x] > b3[x]:
                goalie = 1
                support = 3
            else:
                goalie = 3
                support = 1
        elif ts["b3"] == min(ts.values):
            attacker = 3
            if b2[x] > b1[x]:
                goalie = 2
                support = 1
            else:
                goalie = 1
                support = 2
            
        return {"att" :attacker,"goalie" :goalie,"supp" :support}

    def run(self):
        #create interceptcalc instance
        intercept_c = interceptCalculator(3)

        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                
                robot_pos = robot_pos_recalc(data[self.name])
                # Get & recalculate the position of the ball
                #print(data['ball']['x'], data['ball']['y'])
                ball_pos = coor_recalc(data['ball']['x'], data['ball']['y'])
                #push ball pos into intercept calculator
                intercept_c.pushPoint(ball_pos)
                #print(ball_pos)
                intercept = intercept_c.calculateOptimumIntercept(robot_pos, sample_count=200)
                
                
                controls=[]
               
                
                intercept['y']+=(intercept['y']-0.5)*0.1

                if(intercept['t'] < 8 and ball_pos['x']<robot_pos['x']):
                    print("kcikkk")
                    b, robot_angle = self.get_angles({"x":0, "y":0.5}, robot_pos)
                    controls =goTo(0,0.5, robot_pos, robot_angle, magicnum=0.2) 
                else:
                    b, robot_angle = self.get_angles(intercept, robot_pos)
                    controls =goTo(intercept["x"], intercept["y"], robot_pos, robot_angle) 
                
                #print(intercept)

                left_speed = controls[1]
                right_speed = controls[0]
                
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
               
                
my_robot = MyRobot()
my_robot.run()