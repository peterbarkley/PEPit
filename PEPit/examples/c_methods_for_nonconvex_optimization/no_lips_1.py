import numpy as np

from PEPit.pep import PEP
from PEPit.functions.convex_function import ConvexFunction
from PEPit.functions.convex_indicator import ConvexIndicatorFunction
from PEPit.primitive_steps.bregman_gradient_step import bregman_gradient_step


def wc_no_lips1(L, gamma, n, verbose=True):
    """
    Consider the constrainted non-convex minimization problem,
        min_x { F(x) = f_1(x) + f_2(x) }
    where f_2 is a closed convex indicator function and f_1 is L-smooth relatively to h (possibly non-convex),
    and h is closed proper and convex.

    This code computes a worst-case guarantee for the NoLips Method solving this problem.
    That is, it computes the smallest possible tau(n,L) such that the guarantee
       min_{1<= i <=n} Dh(x_{i-1], x_i) <= tau(n, L) * (F(x0) - F(x_n))
    is valid, where x_n is the output of the NoLips method,
    and where Dh is the Bregman distance generated by h.

    The detailed approach is availaible in
    [1] Heinz H. Bauschke, Jérôme Bolte, and Marc Teboulle. "A Descent Lemma
         Beyond Lipschitz Gradient Continuity: First-Order Methods Revisited
         and Applications." (2017)
    [2] Radu-Alexandru Dragomir, Adrien B. Taylor, Alexandre d’Aspremont, and
         Jérôme Bolte. "Optimal Complexity and Certification of Bregman
         First-Order Methods". (2019)

    DISCLAIMER: This example requires some experience with PESTO and PEPs
    (see Section 4 in [2]).

    :param L: (float) relative-smoothness parameter
    :param gamma: (float) step size (equal to 1/(2*L) for guarantee)
    :param n: (int) number of iterations.
    :param verbose: (bool) if True, print conclusion

    :return: (tuple) worst_case value, theoretical value
    """

    # Instantiate PEP
    problem = PEP()

    # Declare two convex functions and a convex indicator function
    d1 = problem.declare_function(ConvexFunction,
                                  param={})
    d2 = problem.declare_function(ConvexFunction,
                                  param={})
    func1 = (d2 - d1) / 2
    h = (d1 + d2) / 2 / L
    func2 = problem.declare_function(ConvexIndicatorFunction,
                                     param={'D': np.inf})
    # Define the function to optimize as the sum of func1 and func2
    func = func1 + func2

    # Then define the starting point x0 of the algorithm and its function value f0
    x0 = problem.set_initial_point()
    gh0, h0 = h.oracle(x0)
    gf0, f0 = func1.oracle(x0)
    _, F0 = func.oracle(x0)

    # Compute n steps of the NoLips starting from x0
    xx = [x0 for i in range(n + 1)]
    gfx = gf0
    ghx = [gh0 for i in range(n + 1)]
    hx = [h0 for i in range(n + 1)]
    for i in range(n):
        xx[i + 1], _, _ = bregman_gradient_step(gfx, ghx[i], func2 + h, gamma)
        gfx, _ = func1.oracle(xx[i + 1])
        ghx[i + 1], hx[i + 1] = h.oracle(xx[i + 1])
        Dh = hx[i + 1] - hx[i] - ghx[i] * (xx[i + 1] - xx[i])
        # Set the performance metric to the final distance in Bregman distances to the last iterate
        problem.set_performance_metric(Dh)
    _, Fx = func.oracle(xx[n])

    # Set the initial constraint that is the distance in function values between x0 and x^*
    problem.set_initial_condition(F0 - Fx <= 1)

    # Solve the PEP
    pepit_tau = problem.solve(verbose=verbose)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = gamma / (1 - L * gamma) / n

    # Print conclusion if required
    if verbose:
        print('*** Example file: worst-case performance of the NoLips in function values ***')
        print('\tPEP-it guarantee:\t min_i Dh(x_(i+1)), x_(i)) <= {:.6} (F(x_0) - F(x_n))'.format(pepit_tau))
        print('\tTheoretical guarantee :\t min_i Dh(x_(i+1), x_(i)) <= {:.6} (F(x_0) - F(x_n))'.format(
            theoretical_tau))
    # Return the worst-case guarantee of the evaluated method (and the upper theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":
    L = 1
    gamma = 1 / L / 2
    n = 5

    pepit_tau, theoretical_tau = wc_no_lips1(L=L,
                                             gamma=gamma,
                                             n=n)
