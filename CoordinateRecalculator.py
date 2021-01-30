#basic coord recalculation
def coor_recalc(x,y):
  x = (x+0.75)/1.5
  y = (y+0.65)/1.3
  return {"x":x,"y":y}

#recalculates robot positions into better 
def robot_pos_recalc(robot_pos: dict):
  temp_orientation = robot_pos["orientation"]
  
  new = coor_recalc(robot_pos['x'], robot_pos['y'])
  new['orientation'] = temp_orientation
  
  return new
