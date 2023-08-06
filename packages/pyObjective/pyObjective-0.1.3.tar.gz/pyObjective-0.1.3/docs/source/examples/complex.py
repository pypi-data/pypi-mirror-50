from pyObjective import Variable, Model
import numpy as np

"""This example script is written to demonstrate the use of classes, and how more complicated models can be built, 
and still passed to the solver. As a rudimentary example, it has two cubes and a sphere, and we are trying to find 
the dimensions such that the cube1 - cube2 + sphere volume is minimized, subject to the bounds. """


# define a new class
class Cube:

    def __init__(self, model):
        self.x = Variable('x', 1, (0.5, 2), "cube length x")
        self.y = Variable('y', 1, (0.5, 2))
        self.z = Variable('z', 1, (0.5, 2))

        model.add_var(self.x)
        model.add_var(self.y)
        model.add_var(self.z)

    def volume(self):
        return self.x() * self.y() * self.z()


# define a sphere, but keep the variable definition on the outside. For fun
class Sphere:

    def __init__(self, radius):
        self.r = radius

    def volume(self):
        return (4 / 3) * np.pi * self.r() ** 3  # unfortunate brackets needed in here, and not before :(


# define simulation model
m = Model()

# create cube
c1 = Cube(m)
c2 = Cube(m)

# define the sphere radius
r = Variable("r", 1, (0.5, 2), "sphere radius")

m.add_var(r)  # try commenting this line, and you will see that it was removed from the optimization

s = Sphere(r)


# define objective function (to be minimized)
def cost():
    return c1.volume() - c2.volume() + s.volume()


m.objective = cost

# solve
m.solve()

# display results
m.display_results()
