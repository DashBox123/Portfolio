import math
import numpy as np
import pandas as pd
import vpython as vp

x = 0
v = 0.45
t = 0
a = -0.02
dt = 0.2

while v > 0:
    print(f"At time t = {round(t,4)} the velocity is {round(v,4)} and x is {round(x,4)}")
    t = t + dt
    v = v + a*dt
    x = x + v*dt