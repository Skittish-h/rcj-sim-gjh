from CoordinateRecalculator import robot_pos_recalc
def support_position (data):
    """ need to know which robot is attack and which one is goalee 
    x_cor = {"b1":data["B1"]["x"],"b2":data["B2"]["x"],"b3":data["B3"]["x"]}
    y_cor = {"b1": data["B1"]["y"], "b2": data["B2"]["y"], "b3": data["B3"]["y"]}

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
        att_cor = {"x":x_cor["b3"],"y":y_cor["b3"]}"""
    

    #calculation of support optimal position
    b2 = robot_pos_recalc(data["B2"])
    b3 = robot_pos_recalc(data["B3"])
    supp_opti_cor = {"x": b3["x"]+(b2["x"]-b3["x"])/(7/4),"y": 0.5+(0.5-b3["y"])/(3/2)}
    return supp_opti_cor
    