.. pyObjective documentation master file, created by
   sphinx-quickstart on Sat Aug  3 09:18:12 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyObjective!
=======================================

pyObjective is a python package to complement scipy's optimize toolbox.



.. toctree::
   :maxdepth: 2

   examples
   reference



   

Introduction
=============

pyObjective is a tool to define complex models and solve them using scipy's optimize module.

Scipy however works by asking for a function, and the bounds and returns a vector that optimizes the function.
Scipy does not have any understanding of what the variables are and how they are arranged. This makes using it sometimes tricky:
the user is required to know and keep track of the variables and the respective variable bounds.

Instead, pyObjective allows a user to define a variable on the fly, defining the variable bounds at the time the variable is created.
From there the variable is added to the model, and the model's solve method is called to optimize the cost function.

The simplest possible example is below, but more in-depth examples are available on the left.

Quick Start
===========

Here is a minimal example on finding the minimum of :math:`x^2`.

.. literalinclude:: examples/simplest.py

and this gives the formatted output

.. literalinclude:: examples/out_simplest.txt

which is very close to the true optimal, :math:`x=0`.
The small deviation occurs because the underlying method used is scipy.optimize.dual_annealing.
This method is effective for problems which have many local minima, but is fundamentally a stochastic method, and does is not guaranteed to get the numerically exact result.

Look at the examples to see examples of how to use the package.


Future Developments
====================

The next few steps include:

* adding linear and non-linear constraints
* support for units
* create model instances with variables fully defined, so they can be inspected, or used in the future.
* adding more representative examples. 

Index
==================

* :ref:`genindex`
* :ref:`search`