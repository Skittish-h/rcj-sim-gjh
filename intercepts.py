from statistics import mean
import math
#                GJH_team                 #
##########Intercept Calc Class#############
# Class processes past points of ball to  #
# find optimal place for the interception #
# of the ball.                            #
###########################################
class interceptCalculator():
    
    #constructor
    #sample depth - amount of samples remembered to estimate ball trajectory; >1
    #default - intial ball position
    def __init__(self,sample_depth, default = {"x":0.0,"y":0.0}):
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
    
    #pushes new point into array
    def pushPoint(self, point):
        self.pastIntercepts.pop(0)
        self.pastIntercepts.append(point)
    
    #function that calculates the optimum intercept 
    #really long but most of it is just renaming variables and arguments for better visibility and explenations
    def calculateOptimumIntercept(self, currentPositioning):
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
        
        for t in range(50):
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


            print(ballx, bally)
            
            distance_from = math.sqrt(((ballx - r['x'])**2) + ((bally - r['y'])**int(2)))
            distances.append(distance_from)

            prev_b_X = ballx
            prev_b_Y = bally

        return distances
            