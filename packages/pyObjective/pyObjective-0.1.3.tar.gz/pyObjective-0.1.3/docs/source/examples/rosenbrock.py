from pyObjective import Variable, Model



"""
We can start by defining the objective function to minimize.

In this example, we use the classic Rosenbrock function, defined as

f(x,y) = (a - x)^2 + b(y - x^2)^2

where the minima lies at (x,y) = (a, a^2).


We can start by defining the variables
"""
x = Variable(name='x', value=1.5, bounds=(-2, 2))
y = Variable(name='y', value=1.5, bounds=(-1, 3))

"""
Since this method uses simulated annealing, the initial guess value is not needed, 
but helps in checking if the function is being evaluated correctly.

Next, we create a model. The model contains the core functionality to evaluate and optimize the function. 

"""

m = Model()

"""
Now, we must tell the model which variables to optimize over. 
Internally, it maintains a list of variables that are to be optimized. If a variable is created but not added 
to the model, it remains fixed at the prescribed value. """

m.add_var(x)
m.add_var(y)

"""
Next, we define the cost function. Notice, all the variables are defined as calls, using x() instead of x. 
"""


def cost():
    a = 1
    b = 100
    return (a - x()) ** 2 + b * (y() - x() ** 2) ** 2

"""
We can check that the cost is being evaluated correctly, simply by calling the cost.
"""

print(f"The cost is {cost()}")

"""
Finally, we must associate the cost function with the optimizer. 
Notice, here the cost is passed without the brackets.
"""

m.objective = cost

"""Solve. The solution gets saved within the model"""

m.solve()

"""
We can print the results neatly. """

m.display_results()

