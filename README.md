# GJH_team SoccerSimulationChallange #

Repository for GJH_team's RoboCup Junior Soccer simulation challange. Ye be warned, a lot of spaghetti code

![](https://i.postimg.cc/G2k5s6w0/152226294-259657789190759-8649648520952280390-n.png)

Look at 'em go

## Abstract

Our 3 robots use dynamic role changing strategies based on the assumption that all data recieved by the robots is the same. The roles are split into an Attacker, Backup and Goalee.
All robots estimate optimum intercepts for ball interception. The Attacker moves to the intercept in a calculated parabolic fashion, the Goalee mirrors the movement of the ball along the y axis. The Support positions himself in a support position.

## Less Abstract

### Observation

Just from observing simple "stock" ball following code that was upped to full speed, our team came to a couple of observations, from which we drew conclusions that were vital to the functionality of our robots:

- The robots are **slow**, and will spend the vast majority of the time not in contact with the ball (rather chasing it). Positioning is therefore key.
- Cluttering (multiple robots chasing the ball) has no visible advantage and seems to just result in a mess. Robots are better used covering more area.
- There is no clear cut obvious strategy for simple goal scoring, unlinke in omni-wheel robots, which can just keep pointed towards the opponents ball and follow the ball. Scoring goals with 2 wheel robots will be relatively complex.
- Most goals are contactless (not pushed into the goal). Hence having some sort of a goalee makes a lot of sense.

### Roles

As a team we very quickly agreed on some role system. Here are the Roles we came up with, and their respective functions:
- Attacker: somehow scores goals.
- Goalie: Loiters around the goal.
- Backup: somehow covers space.
- (Rejected Idea)  Chuck Norris: As a substitute to backup, if the enemy has a robot near the goal, he attempts to push thier goalee into the enemy defense zone to get him despawned to ease the job for the attacker. Retrospectively we should have implemented this.

![](https://i.postimg.cc/FzX1TdBd/stuffds.png)

For optimum play, roles should be switched dynamically. Initially we wanted to switch roles based off who was nearest to the ball. But soon we switched to finding out who would take the shortest to
intercept the ball. This way a robot who is closest to the ball but still travelling slower than the ball and henceforth pointlessly chasing it would be substituted by a better positioned robot. However for this we need to be capable of calculating the Optimum intercept.



### intercepts.py

This file has a class that tracks the balls movement. It assumes that the ball travel is perfectly linear (true) and that collisions are perfectly elastic 
(false, but a decent approximation). The class has a buffer of past ball positions, and using that it estimates the equation of the balls line travel or its velocity vector.

```python
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
```

Since the distance the of the robot can travel per certain time can be approiamted linearly. We simply graph future ball positions, and wait till one is close enough to our robot to be reached in said time it will take for the ball to get there.
This equation can only be solved graphically especially when factoring in the collisions. Collisions are solved by inverting one of the components of the ball's velocity vector.
```python
  def calculateOptimumIntercept(self, currentPositioning, team ,sample_count=50,sample_accuracy=1):
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
        initial_mx = {'x': self.estimateFunction('x'), 'y':self.estimateFunction('y')}
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
            raw_time = self.calculate_time(distance_from)
            if (m['x']>0 and ballx > r['x']) if team else (m['x']<0 and ballx < r['x']):
                raw_time+=10
            if(raw_time <= t):
                #print(t<8)
                return {"isIntercept":True, "x":ballx, "y":bally, "t":t, "kik": False}#abs(self.should_kick(r, initial_mx)['err'])<0.05}
            

            #sacrifice memory for processing
            prev_b_X = ballx
            prev_b_Y = bally

        return {"isIntercept":False, "x":0, "y":0, "t":1000,"kik":False}
```

### Role division

Based on the intercepts of all robots (each robot calculating intercepts for each robot). The robot with the fastest intercept becomes the attacker. The robot closest to our goal becomes the goalie.
Remaining robot is backup.

### Goalie

The goalie is the simplest. He simply reflects the ball upon the X axis relative to the size of the goal area. From Goalie.py:

```Python
def goalie_cal_Y(ball_pos: dict):
    #calculates ration between the outer goal shit and the entire field and returns the Y
    if (ball_pos['y']>0.5):
        goalie_Y = (ball_pos['y']/1.066) + 0.02

    elif(ball_pos['y'] > 0.47 and ball_pos['y'] < 0.52):
        goalie_Y = 0.5

    else:
        goalie_Y = 1.2/(1.066/ball_pos['y']) + 0.02

    
    if (goalie_Y>0.7):
        goalie_Y = 0.7
    elif (goalie_Y<0.26):
        goalie_Y = 0.28

    return goalie_Y
```


### Support 

Second simplest. He stays between the goalie and the Attacker. Tries to cover as much space. His position is dependent solely on the position of the other two robots. 

```python
def support_position (data, Team):
    b1 = coor_r(data[f"{'B' if Team else 'Y'}1"]["x"],data[f"{'B' if Team else 'Y'}1"]["y"], team=Team)
    b2 = coor_r(data[f"{'B' if Team else 'Y'}2"]["x"],data[f"{'B' if Team else 'Y'}2"]["y"], team=Team)
    b3 = coor_r(data[f"{'B' if Team else 'Y'}3"]["x"],data[f"{'B' if Team else 'Y'}3"]["y"], team=Team)
    
    x_cor = {"b1": b1["x"], "b2": b2["x"], "b3": b3["x"]}
    y_cor = {"b1": b1["y"], "b2": b2["y"], "b3": b3["y"]}

    # checking for attacker and goalie
    if x_cor["b1"]==max(x_cor.values()):
        goalie_cor = {"x":x_cor["b1"],"y":y_cor["b1"]}
    if x_cor["b2"]==max(x_cor.values()):
        goalie_cor = {"x":x_cor["b2"],"y":y_cor["b2"]}
    if x_cor["b3"]==max(x_cor.values()):
        goalie_cor = {"x":x_cor["b3"],"y":y_cor["b3"]}
    if x_cor["b1"]==min(x_cor.values()):
        att_cor = {"x":x_cor["b1"],"y":y_cor["b1"]}
    if x_cor["b2"]==min(x_cor.values()):
        att_cor = {"x":x_cor["b2"],"y":y_cor["b2"]}
    if x_cor["b3"]==min(x_cor.values()):
        att_cor = {"x":x_cor["b3"],"y":y_cor["b3"]}

    #calculation of support optimal position
    #switch for colors 
    if Team:
        supp_opti_cor = {"x":att_cor["x"]+(goalie_cor["x"]-att_cor["x"])/(2),"y":0.5+(0.5-att_cor["y"])/(2)}
        if supp_opti_cor['x'] > 0.8:
            supp_opti_cor['x'] = 0.8
    else:
        supp_opti_cor = {"x":goalie_cor["x"]+(att_cor["x"]-goalie_cor["x"])/(2),"y":0.5+(0.5-att_cor["y"])/(2)}
        if supp_opti_cor['x'] < 0.2:
            supp_opti_cor['x'] = 0.2
    return supp_opti_cor
```

### Attacker

Most complicated. Visually, we concluded that the best function that fits the movement of the robot such that he hits the ball at an angle that sends the ball to the enemy goal is a
quadratic function. Taking our intercept, we must find a quadratic function that passes through: the intercept and the robot. However ince quadratic functions have 3 constants we have to find, we also need a
third input from which we can solve our equation for a,b,c where the quadratic funtion is f(x) = ax^2 + bx + c. The third information is that the slope of the line at the point of intersection must be such that it intersects with the ball. 
Using the derivative f'(x) = 2ax + b we can get a third equation. This gives us 3 equations which we can then solve using Gauss-Jordanian Elimination:

```python
def fit_parabola(intercept_pos: dict, robot_pos: dict, goal_pos: dict):
    # to find a fit we have to build 3 linear equations
    # Equations are put in arrays for the gauss-jordan elimination
    # y = ax^2 + bx + c = [x^2, x, 1, y]

    # equation 1: function has to pass through the robot
    # robotY = a*(robotX^2) + b*(robotX) + c
    eq_1 = [robot_pos['x']**2, robot_pos['x'], 1, robot_pos['y']]
    
    # equation 2: function has to pass through the intercept
    # interceptY = a*(interceptX^2) + b*(interceptX) + c
    eq_2 = [intercept_pos['x']**2, intercept_pos['x'], 1, intercept_pos['y']]

    #equation 3: a derivative of a function is equal to the slope of the intercept to the goal
    # f(x) = ax^2 + bx +c // f'(x) = 2ax + b // (slope to goal) = (2*intercept)*a + b

    #avoid null division
    temp_calc = (goal_pos['x'] - intercept_pos['x'])
    if temp_calc == 0:
        temp_calc = 0.001

    derivative = (goal_pos['y'] - intercept_pos['y']) / temp_calc # rise over run

    eq_3 = [2*intercept_pos['x'], 1, 0, derivative]

    matrix = [eq_1, eq_2, eq_3]
    
    #do gaussian elimination
    return gausian_elimination(matrix)
```

If the parabola passes through the bounds of the field, we inore it and travel linearly. If the ball is behind the future intercept, we also ignore the parabola and travel linearly, 
however increasing the nessecary time it takes to get to the point (hence the robot overcompensates and travels to a position behind the ball rather than to the ball).
