import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

# defining constants
g = 9.81    # acceleration due to gravity
k = 40      # spring constant
m = 1       # mass of weight
b = 1       # friction co-efficient
t_max = 4   # max time in seconds


# initial conditions
x_0 = 0
x_dot_0 = 0

# y[0] = x, y[1] = x_dot, x_ddot = g - kx/m
def spring_mass_damped_ODE(t, y):
    return (y[1], g - k*y[0]/m - b*y[1]/m)

sol = solve_ivp(spring_mass_damped_ODE, [0, t_max], (x_0, x_dot_0), t_eval = np.linspace(0, t_max, 5*30))

# extracting solutions
x, x_dot = sol.y
t = sol.t
KE = (1/2)*m*x_dot**2
PE = (1/2)*k*x**2 - m*g*x
H = KE + PE # hamiltonian
L = KE - PE # lagrangian
print(np.max(x) + np.max(x)/2)

def max_axis(x):
    return round(np.max(x) + np.max(x) / 3)


# Setting up subplots to store animated plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))

# plotting ax1 - displacement/ velocity against time
x_curve, = ax1.plot(t[0], x[0], 'r', lw=2, label=r'$x$')
x_dot_curve, = ax1.plot(t[0], x_dot[0], 'b', lw=2, label=r'$\dot x$')

# plotting ax2 - velocity against displacement
x_xdot_curve, = ax2.plot(x_dot[0], x[0], 'b', lw=2, label=r'$x$')

# plotting ax3 - KE and PE against time
KE_curve, = ax3.plot(t[0], KE[0], 'g', lw=2, label=r'$KE$')
PE_curve, = ax3.plot(t[0], PE[0], 'r', lw=2, label=r'$PE$')

# plotting ax4 - H and L against time
H_curve, = ax4.plot(t[0], H[0], 'g', lw=2, label=r'$H$')
L_curve, = ax4.plot(t[0], L[0], 'r', lw=2, label=r'$L$')

# Setting up ax1 which shows x/x_dot against time
ax1.set_title(f'Spring Mass System. k/m={k/m}, g={g}')
ax1.set_xlim(t[0],t[-1])
ax1.set_ylim(-max_axis(x_dot),max_axis(x_dot))
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel(r'$x$ (m), $\dot x$ (m/s)')
ax1.legend(loc='upper right')
ax1.grid()

# Setting up ax2 which shows x_dot against x
ax2.set_title(f'Spring Mass System - Phase Diagram')
ax2.set_xlim(-max_axis(x), max_axis(x))
ax2.set_ylim(-max_axis(x_dot), max_axis(x_dot))
ax2.set_xlabel(r'$x$ (m)')
ax2.set_ylabel(r'$\dot x$ (m/s)')
ax2.legend(loc='upper right')
ax2.grid()

# Setting up ax3 which shows KE and PE against time
ax3.set_title(f'Spring Mass System - KE/ PE')
ax3.set_xlim(t[0], t[-1])
ax3.set_ylim(-max_axis(KE-PE), max_axis(KE-PE))
ax3.set_xlabel(r'$t$ (s)')
ax3.set_ylabel(r'$KE/ PE$ (J)')
ax3.legend(loc='upper right')
ax3.grid()

# Setting up ax4 which shows H and L against time
ax4.set_title(f'Spring Mass System - H/ L')
ax4.set_xlim(t[0], t[-1])
ax4.set_ylim(-max_axis(H+L), max_axis(H+L))
ax4.set_xlabel(r'$t$ (s)')
ax4.set_ylabel(r'$H/ L$ (J)')
ax4.legend(loc='upper right')
ax4.grid()


def animate(i):
    # update data points for axes
    x_curve.set_data(t[:i+1], x[:i+1])
    x_dot_curve.set_data(t[:i+1], x_dot[:i+1])
    x_xdot_curve.set_data(x[:i+1], x_dot[:i+1])
    KE_curve.set_data(t[:i+1], KE[:i+1])
    PE_curve.set_data(t[:i+1], PE[:i+1])
    H_curve.set_data(t[:i+1], H[:i+1])
    L_curve.set_data(t[:i+1], L[:i+1])

    # Update position of the point in ax1
    ax1_x_point.set_data(t[i], x[i])
    ax1_x_dot_point.set_data(t[i], x_dot[i])

    # Update position of the point in ax2
    ax2_point.set_data(x[i], x_dot[i])

# Initialize the point in ax1
ax1_x_point, = ax1.plot([], [], 'ko')
ax1_x_dot_point, = ax1.plot([], [], 'ko')

# Initialize the point in ax2
ax2_point, = ax2.plot([], [], 'ko')

ani = animation.FuncAnimation(fig, animate, frames=len(t), interval = 0)

plt.tight_layout(pad=4, h_pad=2, w_pad=2, rect=None)
plt.show()



