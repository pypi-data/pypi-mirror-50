from pyObjective import Variable, Model

# define a variable, with an initial guess and the (lower, upper) bounds.
x = Variable("x", 1, (-2,2))

# define a model
m = Model()

# add the variable to the model
m.add_var(x)

# define a cost function
def cost():
    return x()**2

#define the cost function as the function to optimize.
m.objective = cost

# solve the problem
m.solve()

m.display_results()