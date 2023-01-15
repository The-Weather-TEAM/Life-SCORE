def points_to_affine_function(x1, y1, x2, y2, x3, y3):
    a = (y2 - y1) * (x3 - x2) - (y3 - y2) * (x2 - x1)
    b = (x2 - x1) * (x3 - x2) + (y2 - y1) * (y3 - y2)
    c = x2 * (x2 - x1) * y3 - x2 * (y2 - y1) * x3 + x1 * (y2 - y1) * x3 - y1 * (x3 - x2) * x2
    return a,b,c

