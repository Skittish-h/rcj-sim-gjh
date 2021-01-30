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
    def calculateOptimumIntercept(self, currentPositioning):
        #very complex calculations incoming
        distances = []
        #b: ball x & y
        b = self.pastIntercepts[self.sample_depth-1]
        #r: robot x & y
        r = currentPositioning
        #m: gradients
        m = {'x': self.estimateFunction('x')  ,'y':self.estimateFunction('y')}

        for t in range(10):
            #t1 = time elapsed
            t1 = t
            
            distance_from = math.sqrt(((b['x'] + (t1 * m['x']) - r['x'])**2) + ((b['y'] + t1*m['y'] - r['y'])**int(2)))
            distances.append(distance_from)
        return distances
            