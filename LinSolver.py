#                GJH_team                 #
####### Linear Equation Calculator ########
# Calcualtes linear equations using the   #

###########################################

import copy
from fractions import Fraction
 
A = [[1, 3, 2, 1], [2, 3, 3, 1], [5, -3, 1, 5]]

#function that does gausian elimination. Too lazy to go for generic implementation so this will be specific a system of equations with 3 variables
def gausian_elimination(matrix):
    #first eliminate first column of zeroes
    for i in range(1,3):
        coef = (matrix[i][0]/matrix[0][0])
        for j in range(4):
            matrix[i][j] = matrix[i][j] - float(matrix[0][j] * coef)
    
    #first eliminate second column of zeroes
    coef = (matrix[2][1]/matrix[1][1])
    for i in range(4):
        matrix[2][i] = matrix[2][i] - float(matrix[1][i] * coef)
    #find 3rd value
    #print(matrix)

    c = matrix[2][3]/matrix[2][2]
    b = ((matrix[1][3]) - (matrix[1][2]*c))/matrix[1][1]
    a = ((matrix[0][3])- (matrix[0][1]*b) - (matrix[0][2]*c))/matrix[0][0]
    return {'a':a,'b':b,'c':c}
    
gausian_elimination(A)