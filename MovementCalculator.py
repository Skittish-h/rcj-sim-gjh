#                GJH_team                 #
###### Optimal Movement Calculator ########
# File Predicts optimum movement along a  #
# parabola in such a way that the robot   #
# faces the enemy goal.                   #
###########################################
import math
from LinSolver import gausian_elimination

# function that fits a parabolic movement to a given intercept position, 
# considering that the slope of the tangent (derivative) is equal to that
# from the ball to the goal.
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


#function that takes parabolic equations and gives a point on the tangent (so we can use goto function since we are too lazy:D)
#using derivatives
def get_tangent_point(robot_pos: dict, parabola_constants: dict):
    #calculate derivative f'(x) = 2ax + b
    
    derivative = 2 * parabola_constants['a'] * robot_pos['x'] + parabola_constants['b']

    #define future point
    futurepoint = dict()

    #point is 10 units away from us
    futurepoint['x'] = -10
    futurepoint['y'] = derivative * -10
    

    return futurepoint

#function the takes a parabolic equation and using the discriminant calculates if it will intersect the boundaries of he field
def passes_boundary(parabola_constants: dict):
    #if parabola opens upwards -> checking for intersections at y = 0
    d = 0
    if(parabola_constants['a'] > 0):
        d = parabola_constants['b']**2 - 4*parabola_constants['a']*parabola_constants['c']
    #if parabola opens down -> checking for y = 1 thereforec -=1
    else:
        d = parabola_constants['b']**2 - 4*parabola_constants['a']*(parabola_constants['c']-1)
    if(d < 0):
        return False
    return True