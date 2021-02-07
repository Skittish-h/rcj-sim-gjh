#                GJH_team                 #
###### Optimal Movement Calculator ########
# File Predicts optimum movement along a  #
# parabola in such a way that the robot   #
# faces the enemy goal.                   #
###########################################
import math

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
    eq_2 = [intercept_pos['x']**2, intercept_pos['x'], 1, robot_pos['y']]

    #equation 3: a derivative of a function is equal to the slope of the intercept to the goal
    # f(x) = ax^2 + bx +c // f'(x) = 2ax + b // (slope to goal) = (2*intercept)*a + b
    derivative = (goal_pos['y'] - intercept_pos['y']) / (goal_pos['x'] - intercept_pos['x']) # rise over run

    eq_3 = [2*intercept_pos['x'], 1, 0, derivative]
    
    #TODO: do gaussian elimination

    return {"a":0,"b":0,"c":0}


#function that takes parabolic equations and finds angular error between robot and the parabola's path
#using derivatives
def get_angular_error(robot_pos: dict, parabola_constants: dict):
    #calculate derivative f'(x) = 2ax + b
    
    derivative = 2 * parabola_constants['a'] * robot_pos['x'] + parabola_constants['b']
    print(derivative)
    angle = math.atan(derivative)
    angle = math.degrees(angle - robot_pos['orientation'])

    return angle
