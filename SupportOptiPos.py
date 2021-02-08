from CoordinateRecalculator import robot_pos_recalc
def support_position (data):
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
        att_cor = {"x":x_cor["b3"],"y":y_cor["b3"]}

    #calculation of support optimal position
    supp_opti_cor = {"x":att_cor["x"]+(goalie_cor["x"]-att_cor["x"])/2,"y":0.5+(0.5-att_cor["y"])/2}
    return supp_opti_cor