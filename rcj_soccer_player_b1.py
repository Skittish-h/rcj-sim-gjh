# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils

from intercepts import interceptCalculator
from CoordinateRecalculator import coor_recalc, robot_pos_recalc
from GoToFunc import goTo
from Goalie import goalie_angles, goalie_cal_Y, correct_rotation
from SupportOptiPos import support_position

######

INTERCEPT_CONST = 0.03

# Feel free to import built-in libraries
import math
#robot class
class MyRobot(RCJSoccerRobot):

    def getIntercepts(self, data):
        b1 = {"x":data["B1"]["x"],"y": data["B1"]["y"]}
        b2 = {"x":data["B2"]["x"],"y": data["B2"]["y"]}
        b3 = {"x":data["B3"]["x"],"y": data["B3"]["y"]}

        intercept_calc.pushPoint(ball_pos)

        intercepts = {"b1":0,"b2":0 ,"b3":0}
        intercepts["b1"] = intercept_calc.calculateOptimumIntercept(b1, sample_count=200)
        intercepts["b2"] = intercept_calc.calculateOptimumIntercept(b2, sample_count=200)
        intercepts["b3"] = intercept_calc.calculateOptimumIntercept(b3, sample_count=200)

    
    def role_decision(self, team):
        
        #ball_pos = coor_recalc(data['ball']['x'], data['ball']['y'])

        ts = {"b1":intercepts["b1"]["t"],"b2":intercepts["b2"]["t"],"b3":intercepts["b3"]["t"]}

        if team == True:
            if ts["b1"] < ts["b2"] and ts["b1"]< ts['b3']:
                attacker = 1
                if b2["x"] > b3["x"]:
                    goalie = 2
                    support = 3
                else:
                    goalie = 3
                    support = 2
            elif ts["b2"] < ts["b1"] and ts["b2"]< ts['b3']:
                attacker = 2
                if b1["x"] > b3["x"]:
                    goalie = 1
                    support = 3
                else:
                    goalie = 3
                    support = 1
            elif ts["b3"] < ts["b2"] and ts["b3"]< ts['b1']:
                attacker = 3
                if b2["x"] > b1["x"]:
                    goalie = 2
                    support = 1
                else:
                    goalie = 1
                    support = 2
        else:
            if ts["b1"] < ts["b2"] and ts["b1"]< ts['b3']:
                attacker = 1
                if b2["x"] < b3["x"]:
                    goalie = 2
                    support = 3
                else:
                    goalie = 3
                    support = 2
            elif ts["b2"] < ts["b1"] and ts["b2"]< ts['b3']:
                attacker = 2
                if b1["x"] < b3["x"]:
                    goalie = 1
                    support = 3
                else:
                    goalie = 3
                    support = 1
            elif ts["b3"] < ts["b2"] and ts["b3"]< ts['b1']:
                attacker = 3
                if b2["x"] < b1["x"]:
                    goalie = 2
                    support = 1
                else:
                    goalie = 1
                    support = 2 

                
            return {"att" :attacker,"goalie" :goalie,"supp" :support}

    def be_attacker(intercept_pos, robot_pos):
        #push ball pos into intercept calculator
        self.intercept_c.pushPoint(ball_pos)
        #print(ball_pos)
        intercept = 
                
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


    def be_goalie(ball_pos, robot_pos):
        Designated_pos = [[0.58, 0]]
        DesiredPos = coor_recalc(Designated_pos[0][0],Designated_pos[0][1])

        DesiredPos['y'] = goalie_cal_Y(ball_pos)
        ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
        controls =goTo(DesiredPos["x"], DesiredPos["y"], robot_pos, robot_angle) #0 right motor, 1 left motor 
        left_speed = controls[1]
        right_speed = controls[0]

    def be_backup(ball_pos, robot_pos):
        DesiredPos = [[0,0]]
        DesiredPos[0][0] = support_position()['x']
        DesiredPos[0][1] = support_position()['y']

        ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
        controls =goTo(DesiredPos["x"], DesiredPos["y"], robot_pos, robot_angle) #0 right motor, 1 left motor 
        left_speed = controls[1]
        right_speed = controls[0]


    def run(self):
        #create interceptcalc instance
        self.intercept_c = interceptCalculator(3)

        Team = (self.team == "B")
        
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                
                robot_pos = robot_pos_recalc(data[self.name], Team)
                # Get & recalculate the position of the ball
                ball_pos = coor_recalc(data['ball']['x'], data['ball']['y'], Team)
                
                intercepts = self.getIntercepts(data)
                
                roles = self.role_decision(Team, intercepts)

               
                # if roles att is 1 the B1 will execute attacker code
                if role == "att":                
                    be_attacker(ball_pos, robot_pos)

                # if goalie will be 1 B1 will execute goalie code
                elif role == "goal":
                    be_goalie_blue(ball_pos, robot_pos)

                #if support is 1 B1 will execute backup code
                elif role == "back":
                    be_backup(ball_pos, robot_pos)

                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
               
                
my_robot = MyRobot()
my_robot.run()