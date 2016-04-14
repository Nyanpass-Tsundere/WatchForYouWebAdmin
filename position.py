from sympy import *
x = Symbol('x')
y = Symbol('y')

#先假設三點(a,b,c)的x,y座標
#def Position(xa,ya,xb,yb,xc,yc):
xaa=input(">>> Xa")
yaa=input(">>> Ya")
xba=input(">>> Xb")
yba=input(">>> Yb")
xca=input(">>> Xc")
yca=input(">>> Yc")
AA=input(">>>A")
BB=input(">>>B")
CC=input(">>>C")

xa=float(xaa)
ya=float(yaa)
xb=float(xba)
yb=float(yba)
xc=float(xca)
yc=float(yca)
A=float(AA)
B=float(BB)
C=float(CC)
a = xa**2-2*xa*x+x**2+ya**2-2*ya*y+y**2-A**2
b = xb**2-2*xb*x+x**2+yb**2-2*yb*y+y**2-B**2
c = xc**2-2*xc*x+x**2+yc**2-2*yc*y+y**2-C**2

f1 = a-b
f2 = a-c
f3 = b-c

sol=solve_poly_system((f1,f2,f3),x,y)
print(sol)
