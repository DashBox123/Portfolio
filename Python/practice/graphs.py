import math
import sys
import numpy as np
import pandas as pd
import vpython as vp
import matplotlib.pyplot as plt


class Car:
    def __init__(self,x,v,a):
        self.x = [x] # distance in m
        self.v = [v] # velocity in m/s
        self.a = a # acceleration in m/s/s

car_a = Car(0.5,0.45,0)
car_b = Car(0,0,0.2)
cars = [car_a, car_b]

dt = 0.01
t = [0]

fig, f1 = plt.subplots()
f1.set_title("My Plot")
f1.set_ylabel("Distance/ m")
f1.set_xlabel("Time/ s")

distance_between = car_a.x[-1] - car_b.x[-1]

while distance_between > 0.01:
    f1.plot(t, car_a.x)
    f1.plot(t, car_b.x)   
    for car in cars:
        car.v.append(car.v[-1] + car.a*dt)
        car.x.append(car.x[-1] + car.v[-1]*dt)
    t.append(t[-1] + dt)
    distance_between = abs(car_a.x[-1] - car_b.x[-1])

print(f"The cars meet at time {round(t[-1],2)} seconds and distance {round(car_a.x[-1],2)} metres")

f1.legend()
f1.grid(True, linestyle='--', linewidth=0.5, color='gray')



g1 = vp.graph(title="My Graph")
plt.show(block=True)