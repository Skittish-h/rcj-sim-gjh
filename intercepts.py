from statistics import mean
import math
#                GJH_team                 #
##########Intercept Calc Class#############
# Class processes past points of ball to  #
# find optimal place for the interception #
# of the ball.                            #
###########################################
color = ""

class interceptCalculator():
    
    #constructor
    #sample depth - amount of samples remembered to estimate ball trajectory; >1
    #default - intial ball position
    def __init__(self,sample_depth, default = {"x":0.5,"y":0.5}):
        self.sample_depth = sample_depth
        self.pastIntercepts = [default for i in range(sample_depth)]
    
    #print's balls point history
    def printPointHistory(self):
        print(self.pastIntercepts)
    

    #estimate gradient of
    # returns m in function future_cord = current + m*time
    def estimateFunction(self, coordinate): 
        #m & c values we averge out
        m_vals = []

        #for every calculatable interval (since 0th term is last and each interval is calcaulated by (new-old)/time)
        for i in range(self.sample_depth-1, -1,-1):
            for b in range(i-1,-1,-1):
                #calculate m: dDistance/dTime
                
                m = (self.pastIntercepts[i][coordinate] - self.pastIntercepts[b][coordinate])/(i-b)
                #calculate c: c = dDistance - m*dTime 
                m_vals.append(m)
        
        return mean(m_vals)
    def get_angles(self, ball_pos: dict, robot_pos: dict):
        # Get the angle between the robot and the ball
        angle = math.atan2(
            ball_pos['y'] - robot_pos['y'],
            ball_pos['x'] - robot_pos['x'],
        )

        if angle < 0:
            angle = 2 * math.pi + angle

        robot_ball_angle = math.degrees(angle)

        # Axis Z is forward
        # TODO: change the robot's orientation so that X axis means forward
        robot_ball_angle -= 90
        if robot_ball_angle > 360:
            robot_ball_angle -= 360

        return robot_ball_angle
    #pushes new point into array
    def pushPoint(self, point):
        self.pastIntercepts.pop(0)
        self.pastIntercepts.append(point)
    
    #calculates time nessecary to traverse a certain distance - used to calculate imtercept
    def calculate_time(self, distance):
        speed_constant = {'m':78, 'c':0}
        
        return speed_constant['m']*distance + speed_constant['c']
        
    #function figuring if the ball is going to hit the robot
    #done by estimating the X time for ball to travel to robot, and thus getting the Y coordinate offset
    '''def should_kick(self, currentPositioning, functions):
        #some data collection r-> robot pos; b-> ball pos
        r = currentPositioning
        b = self.pastIntercepts[self.sample_depth-1]

        #getting distance between ball and robot
        X_dst = b['x'] - r['x']
        Y_dst = b['y'] - r['y']
        
        #feeding this data into our functions to see if they correlate, can't have zero division
        if functions['x'] != 0:
            #calculate time to X
            time_to_X = X_dst/functions['x']
            #error is deviation from funtioned Y movenet and X duration
            error = Y_dst - functions['y']*time_to_X
            
            #give error, direction of ball travel, and time to intersection of ball and robot
            return {"err": error, "dir":"B" if functions['x']>0 else "Y", "time":time_to_X, "x":X_dst}
        return {"err": 100, "dir":"B" if functions['x']>0 else "Y", "time":0, "x":X_dst}'''
        
    def get_desired_hit_angle(self, m_vals, intercept, desired_target={'x':0, 'y':0.5}):
        a_to_target = self.get_angles(desired_target, intercept)
        ball_vector_a = self.get_angles(m_vals,{'x':0, "y":0})
        adjustment = (a_to_target-ball_vector_a)
        return adjustment, a_to_target, ball_vector_a
    #function that calculates the optimum intercept 
    #really long but most of it is just renaming variables and arguments for better visibility and explenations
    def calculateOptimumIntercept(self, currentPositioning, sample_count=50,sample_accuracy=1):
        #very complex calculations incoming
        #all distances we return
        distances = []
        
        #previous X and Y coordinates for colision calc
        prev_b_X = 0
        prev_b_Y = 0

        #time offsets for when collision occurs
        t_offset= 0
        #b: ball x & y
        b = self.pastIntercepts[self.sample_depth-1]
        #r: robot x & y
        r = currentPositioning
        #m: gradients
        m = {'x': self.estimateFunction('x'), 'y':self.estimateFunction('y')}
        #data for decision to kick
        #do sample_count loops with sample accuracy time each
        for t in range(0, sample_count*sample_accuracy, sample_accuracy):
            #t1 = time elapsed since beginning/last collision
            t1 = (t - t_offset)
            
            #calculated future BallX & BallY
            ballx = b['x'] + (t1 * m['x'])
            bally = b['y'] + (t1 * m['y'])
            

            ## *Colision Checks* ##
            
            #the way we compute ricochet's:
            #   -in a prediction, check if balls position isn't negative or > 1in direction
            #   -if it is:
            #       -we asume that the last "OK" coordinate is the riccochet point
            #       -we assume collision is elastic (all k_energy is preserved) (TODO: we might want to calculate collision elasticity)
            #       -offset time to future predictions by the current t ("t_offset" variables)
            #       -invert gradient of travel("m") constant
            #       -set past ball position ("b") to previous X & Y


            #ball is to pass X boundary
            if(ballx < 0 or ballx > 1):
                t_offset = t
                b = {'x':prev_b_X,'y':prev_b_Y}
                m['x'] = -m['x']

                
            if(bally < 0 or bally > 1):
                t_offset = t
                b = {'x':prev_b_X,'y':prev_b_Y}
                m['y'] = -m['y']

            #ball is to pass X boundary
            #print(ballx, bally)
            
            #do math
            distance_from = math.sqrt(((ballx - r['x'])**2) + ((bally - r['y'])**int(2)))
            
            #if we can travel to the ball in time by that coordinate, return
            if(self.calculate_time(distance_from) <= t):
                print(self.get_desired_hit_angle(m, {"x":ballx, "y":bally}))
                return {"isIntercept":True, "x":ballx, "y":bally, "t":t}
            

            #sacrifice memory for processing
            prev_b_X = ballx
            prev_b_Y = bally

        return {"isIntercept":False, "x":0, "y":0}
            