from CoordinateRecalculator import robot_pos_recalc
def support_position (data):
    roles = role_decision(self)
    b1 = {"x":data["B1"]["x"],"y": data["B1"]["y"]}
    b2 = {"x":data["B2"]["x"],"y": data["B2"]["y"]}
    b3 = {"x":data["B3"]["x"],"y": data["B3"]["y"]}

    if roles["att"] == 1:
        att = b1
        if roles["goalie"] == 2:
            goa = b2
        elif roles["goalie"] == 3:
            goa = b3
    elif roles["att"] == 2:
        att = b2
        if roles["goalie"] == 1:
            goa = b1
        elif roles["goalie"] == 3:
            goa = b3
    elif roles["att"] == 3:
        att = b3
        if roles["goalie"] == 2:
            goa = b2
        elif roles["goalie"] == 1:
            goa = b1
        
    supp_opti_cor = {"x": att["x"]+(goa["x"]-att["x"])/(7/4),"y": 0.5+(0.5-att["y"])/(3/2)}
    return supp_opti_cor
    