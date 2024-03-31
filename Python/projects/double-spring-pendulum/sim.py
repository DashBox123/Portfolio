import numpy as np
import sympy as sp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter

# Declaring basic constants
t, m, g, k, l = sp.symbols('t m g k l')

# Declaring basic time-dependent functions
r1, r2, theta1, theta2 = sp.symbols('r1, r2, theta1, theta2', cls=sp.Function)


# Defining time-dependent functions and 1st and 2nd order derivatives
theta1 = theta1(t)
theta1_dot = sp.diff(theta1, t)
theta1_ddot = sp.diff(theta1_dot, t)

theta2 = theta2(t)
theta2_dot = sp.diff(theta2, t)
theta2_ddot = sp.diff(theta2_dot, t)

r1 = r1(t)
r1_dot = sp.diff(r1, t)
r1_ddot = sp.diff(r1_dot, t)

r2 = r2(t)
r2_dot = sp.diff(r2, t)
r2_ddot = sp.diff(r2_dot, t)

# Declaring spatial coordinates
x1, y1, x2, y2 = sp.symbols('x1, y1, x2, y2', cls=sp.Function)
x1 = x1(r1, theta1, l)
y1 = y1(r1, theta1, l)
x2 = x2(x1, r2, theta2)
y2 = y2(y1, r2, theta2)

# Defining spatial coordinates and their t derivatives
x1 = (l + r1)*sp.cos(theta1)
x1_dot = sp.diff(x1, t)

x2 = x1 + (l + r2)*sp.cos(theta2)
x2_dot = sp.diff(x2, t)

y1 = - (l + r1)*sp.sin(theta1)
y1_dot = sp.diff(y1, t)

y2 = y1 - (l + r2)*sp.sin(theta2)
y2_dot = sp.diff(y2, t)

# Defining the Lagrangian
T = (1/2)*m*(x1_dot**2 + y1_dot**2) + (1/2)*m*(x2_dot**2 + y2_dot**2)
V = m*g*y1 + m*g*y2 + (1/2)*k*(r1**2) + (1/2)*k*(r2**2)
L = T - V

# Computing Lagrange equations for r1, r2, theta1, theta2, and simplifying via sympy
L1 = (sp.diff(L, r1) - sp.diff(sp.diff(L, r1_dot), t)          ).simplify()
L2 = (sp.diff(L, r2) - sp.diff(sp.diff(L, r2_dot), t)          ).simplify()
L3 = (sp.diff(L, theta1) - sp.diff(sp.diff(L, theta1_dot), t)  ).simplify()
L4 = (sp.diff(L, theta2) - sp.diff(sp.diff(L, theta2_dot), t)  ).simplify()

# Compute analytical solutions and simplify -- sol contains 4 solutions that are 2nd order ODE of r1/r2/theta1/theta2 against t
sol = sp.solve([L1, L2, L3, L4], (r1_ddot, r2_ddot, theta1_ddot, theta2_ddot), simplify = True, rational = False)

# lambdify our sols so we can obtain numerical answers
r1_dot_f= sp.lambdify(r1_dot, r1_dot)
r2_dot_f= sp.lambdify(r2_dot, r2_dot)
theta1_dot_f= sp.lambdify(theta1_dot, theta1_dot)
theta2_dot_f= sp.lambdify(theta2_dot, theta2_dot)

ddot_vars = (m, k ,g, l, theta1, theta2, r1, r2, theta1_dot, theta2_dot, r1_dot, r2_dot)
r1_ddot_f = sp.lambdify(ddot_vars, sol[r1_ddot])
r2_ddot_f = sp.lambdify(ddot_vars, sol[r2_ddot])
theta1_ddot_f = sp.lambdify(ddot_vars, sol[theta1_ddot])
theta2_ddot_f = sp.lambdify(ddot_vars, sol[theta2_ddot])

# Defining ODE vector to be solved
def S_dot(S, t):
    theta1, theta1_dot, theta2, theta2_dot, r1, r1_dot, r2, r2_dot = S
    return [
        theta1_dot_f(theta1_dot),
        theta1_ddot_f(m,k,g,l,theta1,theta2,r1,r2,theta1_dot,theta2_dot,r1_dot,r2_dot),
        theta2_dot_f(theta2_dot),
        theta2_ddot_f(m,k,g,l,theta1,theta2,r1,r2,theta1_dot,theta2_dot,r1_dot,r2_dot),
        r1_dot_f(r1_dot),
        r1_ddot_f(m,k,g,l,theta1,theta2,r1,r2,theta1_dot,theta2_dot,r1_dot,r2_dot),
        r2_dot_f(r2_dot),
        r2_ddot_f(m,k,g,l,theta1,theta2,r1,r2,theta1_dot,theta2_dot,r1_dot,r2_dot),
    ]

# constants
t = np.linspace(0, 20, 1000)
g = 9.81
m = 1
k = 10
l = 1

# inital conditions
initial_conditions = list(
    {
        'theta1_0' : np.pi / 2,
        'theta1_dot_0' : 0,
        'theta2_0' : (3/2) * np.pi / 2,
        'theta2_dot_0' : 0,
        'r1_0' : 0,
        'r1_dot_0' : 5,
        'r2_0' : 0,
        'r2_dot_0' : 5
    }.values()
)

ans = odeint(S_dot, y0 = initial_conditions, t = t)

# solutions dictionary
solutions = {
    'r1' : ans.T[4],
    'r2' : ans.T[6],
    'theta1' : ans.T[0],
    'theta2' : ans.T[2]
}

# get x1, x2, y1, y2
def getx1x2y1y2(r1, r2, theta1, theta2):
    # compute x1, x2, y1, y2
    x1 = (l + r1)*np.cos(theta1)
    x2 = x1 + (l + r2)*np.cos(theta2)
    y1 = - (l + r1)*np.sin(theta1)
    y2 = y1 - (l + r2)*np.sin(theta2)
    
    # return
    return (
        x1,
        x2,
        y1,
        y2
    )

x1, x2, y1, y2 = getx1x2y1y2(solutions['r1'], solutions['r2'], solutions['theta1'], solutions['theta2'])

def animate(i):
    ln1.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.grid()
ln1, = plt.plot([], [], 'ro--', lw = 3, markersize = 8)
ax.set_ylim(-10, 10)
ax.set_xlim(-10, 10)
ani = animation.FuncAnimation(fig, animate, frames = 1000, interval = 50)
ani.save('pendulum.gif', writer = 'pillow', fps = 50)
