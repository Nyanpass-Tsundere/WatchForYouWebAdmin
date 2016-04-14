from sympy import *

def resLocate(beaLocs,beaDist):
    x = Symbol('x')
    y = Symbol('y')

    a = beaLocs[0][0]**2-2*beaLocs[0][0]*x+x**2+beaLocs[0][1]**2-2*beaLocs[0][1]*y+y**2-beaDist[0]**2
    b = beaLocs[1][0]**2-2*beaLocs[1][0]*x+x**2+beaLocs[1][1]**2-2*beaLocs[1][1]*y+y**2-beaDist[1]**2
    c = beaLocs[2][0]**2-2*beaLocs[2][0]*x+x**2+beaLocs[2][1]**2-2*beaLocs[2][1]*y+y**2-beaDist[2]**2
    
    f1 = a-b
    f2 = a-c
    f3 = b-c
    
    sol=solve_poly_system((f1,f2,f3),x,y)
    return sol

