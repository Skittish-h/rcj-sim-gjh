import math

def goalie_angles(ball_pos: dict):

	#return the angle at which the robot should rotate to face the ball

    blue = {'x': 0.73, 'yr': -0.105,  'yc': 0, 'yl': 0.105 }

    if (ball_pos['y'] >= 0.105):

    	angle_center = math.atan2(
    	ball_pos['x'] - blue['x'],
     	ball_pos['y'] - blue['yl'],
    	)

    elif(ball_pos['y']<= -0.105):

    	angle_center = math.atan2(
    	ball_pos['x'] - right_blue['x'],
     	ball_pos['y'] - right_blue['yr'],
	    )

    elif(ball_pos['y']> -0.105 and ball_pos['y']<0.105):

    	angle_center = math.atan2(
    		ball_pos['x']- blue['x'],
    		ball_pos['y']-blue['yc'])
    print(math.degrees(angle_center))
    return math.degrees(angle_center)
    

'''
def move_to_X(robot_pos: dict):
	if (robot_pos['x'] < 0.58):
		left_speed = 5
        right_speed = 5
    elif (robot_pos['x'] > 0.58):
    	left_speed = 0
        right_speed = 0
    return left_speed, right_speed
    '''
    
def rotate_to_ball(angle):
     if angle >= 345 or angle <= 15:
        return 0
    return -1 if ball_angle < 180 else 1


ball_pos={'x': 0, 'y': 0.0}

goalie_angles(ball_pos)