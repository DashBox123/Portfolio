from vpython import *

ball = sphere(pos=vector(0,0.1,0), radius=0.05, color=color.yellow, make_trail=True)
ground = box(pos=vector(0,0,0), size=vector(2.5,0.02,0.5))
g1 = graph(xtitle = "t [s]", ytitle="y [m]")
f1 = gcurve(color=color.blue)

g = vector(0,-9.8,0)
ball_m = 0.05
v_0 = 3.5
theta = 73*pi/180
ball_v = v_0*vector(cos(theta),sin(theta),0)
vscale = 0.1
varrow = arrow(pos=ball.pos, axis=vscale*ball_v, color = color.cyan)

t = 0
dt = 0.01
ground_offset = ground.pos.y + ball.radius+ground.size.y

while ball.pos.y > ground_offset:
    rate(50)
    F = ball_m*g
    a = F/ball_m
    ball_v = ball_v + a*dt
    ball.pos = ball.pos + ball_v*dt
    varrow.pos = ball.pos
    varrow.axis = vscale*ball_v
    t = t + dt
    f1.plot(t, ball.pos.y)


while True:
    rate(50)