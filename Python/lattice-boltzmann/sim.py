# The following article (https://medium.com/swlh/create-your-own-lattice-boltzmann-simulation-with-python-8759e8b53b1c)
# was used to help code this

import numpy as np
from matplotlib import pyplot

plot_iter = 5 # plot after iterations

# "cell" refers to a body-centered cubic lattice of 9 points
def main():
    Nx = 400 # cells across x-direction
    Ny = 100 # cells across y-direction
    tau = 0.53 # timescale of collisions
    Nt = 30000 # iterations
    obj_radius = 12

    # lattice speeds and weights
    NL = 9 # directions each lattice point can move in (8 + 1)
    # x and y components of lattice point velocities
    vx = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
    vy = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
    # weights of velocity directions for each lattice point such that
    # up/down/left/right = 1/9
    # diagonal = 1/36
    # central i.e. into itself = 4/9
    weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])

    # initial conditions to make fluid flow left to right
    Fluid = np.ones((Ny, Nx, NL)) + 0.01 * np.random.standard_normal(size=(Ny, Nx, NL)) # returns normally distributed array of 1s that is 100x400x9
    Fluid[:, :, 3] = 2.3 # Assigning non-zero value to cells +x direction of movement

    # circle object
    circle = np.full((Ny,Nx), False)

    # making circle into boundary with radius obj_radius
    for y in range(0, Ny):
        for x in range(0, Nx):
            if distance(Nx/4, Ny/2, x, y) < obj_radius:
                circle[y][x] = True

    # main loop
    for it in range(Nt):

        # boundary conditions to make walls absorb
        Fluid[:, -1, [6, 7, 8]] = Fluid[:, -2, [6, 7, 8]]
        Fluid[:, 0, [2, 3, 4]] = Fluid[:, 1, [2, 3, 4]]  

        # particle streaming
        for i, cx, cy in zip(range(NL), vx, vy):
            # roll i.e. move each particle along cx direction
            Fluid[:, :, i] = np.roll(Fluid[:, :, i], cx, axis = 1)
            # move each particle along cy direction
            Fluid[:, :, i] = np.roll(Fluid[:, :, i], cy, axis = 0)

        # elastic collisions with object
            bndryF = Fluid[circle, :]
            bndryF = bndryF[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]

        # fluid variables
        velocities = np.sum(Fluid, 2) # sum of velocities of all particles
        ux = np.sum(Fluid * vx, 2) / velocities # x-component of fluid velocity
        uy = np.sum(Fluid * vy, 2) / velocities # y-component of fluid velocit

        # setting fluid velocities of particles that collide with our boundary
        Fluid[circle, :] = bndryF
        # setting fluid velocities of particles that are INSIDE our boundary to 0
        ux[circle] = 0
        uy[circle] = 0

        # inter-particle collisions of isothermal fluid
        Feq = np.zeros(Fluid.shape)
        for i, cx, cy, w in zip(range(NL), vx, vy, weights):
            Feq[:, :, i] = velocities * w * (
                1 + 3 * (cx*ux + cy*uy) + (9/2) * (cx*ux + cy*uy)**2 - (3/2)*(ux**2 + uy**2)
                )
        Fluid = Fluid + (-1/tau) * (Fluid-Feq)

        if it%plot_iter == 0: # plots after ever n iterations
            pyplot.imshow(np.sqrt(ux**2 + uy**2)) # plot of magnitude of velocity
            pyplot.pause(10e-9)
            pyplot.cla()

# returns distance between 2 points
def distance(x_1, y_1, x_2, y_2):
    return np.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
    

if __name__ == "__main__":
    main()