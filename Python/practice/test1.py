from vpython import *
import time



# Create a graph
graph1 = graph(title='My Graph', xtitle='Time', ytitle='Value')

# Create a curve to plot on the graph
curve1 = gcurve(color=color.blue)

# Add data points to the curve
for t in range(100):
    curve1.plot(t, sin(t * 0.1))


while True:
    rate(60)

