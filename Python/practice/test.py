import math
import numpy as np
import pandas as pd
import vpython as vp




G = 6.67e-11 #Nm2/kg2
Me = 5.972e24 #kg
Re = 6.378e9 #metres

a = (G*Me)/ (Re**2) # N/kg

print(a,"N/kg")

vct1 = np.array([1,2,3,4])
vct2 = np.array([1,2,3,4])

print(vct1+vct2)

A = vp.vector(1,2,3)
B = vp.vector(4,5,6)
C = A + B
print("Vector C:",C)
print("Cx:", C.x)
print("|C|:",round(vp.mag(C),2))
print("A.B:",vp.dot(A,B))
print("AxB:",vp.cross(A,B))


# Create a 3D scene
scene = vp.canvas()

# Create a sphere
vp.sphere()

# Run the scene
scene.run()