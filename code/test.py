import math
def calculate_coefficient(moyenne, maximum, x):
    difference = maximum - moyenne
    coefficient = (x - moyenne) / difference
    rep = coefficient*100
    rep = 100/(1+math.exp(-0.08*rep))
    return rep

moyenne = 0.00078740157
maximum = 0.0009
x = 0.00078740157
x2 = 0.0009
coefficient = calculate_coefficient(moyenne, maximum, x)
print(coefficient)
coefficient = calculate_coefficient(moyenne, maximum, x2)
print(coefficient)
