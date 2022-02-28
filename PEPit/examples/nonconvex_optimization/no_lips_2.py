import numpy as np

from PEPit import PEP
from PEPit.functions import ConvexFunction
from PEPit.functions import ConvexIndicatorFunction
from PEPit.primitive_steps import bregman_gradient_step


def wc_no_lips_2(L, gamma, n, verbose=1):
    """
    Consider the constrainted composite convex minimization problem

        .. math:: F_\\star \\triangleq \\min_x \\{F(x) \equiv f_1(x)+f_2(x) \\}

    where :math:`f_2` is a closed convex indicator function and :math:`f_1` is possibly non-convex, :math:`L`-smooth relatively to :math:`h`,
    and :math:`h` is closed proper and convex.

    This code computes a worst-case guarantee for the **NoLips** method.
    That is, it computes the smallest possible :math:`\\tau(n,L,\\gamma)` such that the guarantee

        .. math:: \\min_{0 \\leqslant t \\leqslant n-1} D_h(x_t;x_{t+1}) \\leqslant \\tau(n, L, \\gamma) (F(x_0) - F(x_n))

    is valid, where :math:`x_n` is the output of the **NoLips** method,
    and where :math:`D_h` is the Bregman distance generated by :math:`h`:

    .. math:: D_h(x; y) \\triangleq h(x) - h(y) - \\nabla h (y)^T(x - y).

    In short, for given values of :math:`n`, :math:`L`, and :math:`\\gamma`, :math:`\\tau(n, L, \\gamma)` is computed
    as the worst-case value of :math:`\\min_{0 \\leqslant t \\leqslant n-1}D_h(x_t;x_{t+1})` when
    :math:`F(x_0) - F(x_n) \\leqslant 1`.

    **Algorithms**: This method (also known as Bregman Gradient, or Mirror descent) can be found in, e.g., [1, Section 3]. For :math:`t \\in \\{0, \\dots, n-1\\}`,

        .. math:: x_{t+1} = \\arg\\min_{u \\in R^d} \\nabla f(x_t)^T(u - x_t) + \\frac{1}{\\gamma} D_h(u; x_t).

    **Theoretical guarantees**: An empirically **tight** worst-case guarantee is

        .. math:: \\min_{0 \\leqslant t \\leqslant n-1}D_h(x_t;x_{t+1}) \\leqslant \\frac{\\gamma}{n}(F(x_0) - F(x_n)).

    **References**: The detailed setup is presented in [1]. The PEP approach for studying such settings
    is presented in [2].

    `[1] J. Bolte, S. Sabach, M. Teboulle, Y. Vaisbourd (2018). First order methods beyond convexity and Lipschitz
    gradient continuity with applications to quadratic inverse problems. SIAM Journal on Optimization, 28(3), 2131-2151.
    <https://arxiv.org/pdf/1706.06461.pdf>`_

    `[2] R. Dragomir, A. Taylor, A. d’Aspremont, J. Bolte (2021). Optimal complexity and certification of Bregman
    first-order methods. Mathematical Programming, 1-43.
    <https://arxiv.org/pdf/1911.08510.pdf>`_

    DISCLAIMER: This example requires some experience with PEPit and PEPs (see Section 4 in [2]).

    Args:
        L (float): relative-smoothness parameter.
        gamma (float): step-size (equal to :math:`\\frac{1}{2L}` for guarantee).
        n (int): number of iterations.
        verbose (int): Level of information details to print.
                       -1: No verbose at all.
                       0: This example's output.
                       1: This example's output + PEPit information.
                       2: This example's output + PEPit information + CVXPY details.

    Returns:
        pepit_tau (float): worst-case value.
        theoretical_tau (float): theoretical value.

    Example:
        >>> L = 1
        >>> gamma = 1 / L
        >>> pepit_tau, theoretical_tau = wc_no_lips_2(L=L, gamma=gamma, n=3, verbose=1)
        (PEPit) Setting up the problem: size of the main PSD matrix: 14x14
        (PEPit) Setting up the problem: performance measure is minimum of 3 element(s)
        (PEPit) Setting up the problem: initial conditions (1 constraint(s) added)
        (PEPit) Setting up the problem: interpolation conditions for 3 function(s)
                 function 1 : 12 constraint(s) added
                 function 2 : 12 constraint(s) added
                 function 3 : 25 constraint(s) added
        (PEPit) Compiling SDP
        (PEPit) Calling SDP solver
        (PEPit) Solver status: optimal (solver: MOSEK); optimal value: 0.3333333333330493
        *** Example file: worst-case performance of the NoLips_2 in Bregman distance ***
            PEPit guarantee:		 min_t Dh(x_(t-1), x_(t)) <= 0.333333 (F(x_0) - F(x_n))
            Theoretical guarantee :	 min_t Dh(x_(t-1), x_(t)) <= 0.333333 (F(x_0) - F(x_n))

    """

    # Instantiate PEP
    problem = PEP()

    # Declare two convex functions and a convex function
    d1 = problem.declare_function(ConvexFunction, reuse_gradient=True)
    d2 = problem.declare_function(ConvexFunction, reuse_gradient=True)
    func1 = (d2 - d1) / 2
    h = (d1 + d2) / L / 2
    func2 = problem.declare_function(ConvexIndicatorFunction, D=np.inf)

    # Define the function to optimize as the sum of func1 and func2
    func = func1 + func2

    # Then define the starting point x0 of the algorithm and its function value f0
    x0 = problem.set_initial_point()
    gh0, h0 = h.oracle(x0)
    gf0, f0 = func1.oracle(x0)
    _, F0 = func.oracle(x0)

    # Compute n steps of the NoLips starting from x0
    x1, x2 = x0, x0
    gfx = gf0
    ghx = gh0
    hx1, hx2 = h0, h0
    for i in range(n):
        x2, _, _ = bregman_gradient_step(gfx, ghx, func2 + h, gamma)
        gfx, _ = func1.oracle(x2)
        ghx, hx2 = h.oracle(x2)
        Dhx = hx1 - hx2 - ghx * (x1 - x2)
        # update the iterates
        x1, hx1 = x2, hx2
        # Set the performance metric to the Bregman distance to the last iterate
        problem.set_performance_metric(Dhx)
    _, Fx = func.oracle(x2)
    # Set the initial constraint that is the Bregman distance between x0 and x^*
    problem.set_initial_condition(F0 - Fx <= 1)

    # Solve the PEP
    pepit_verbose = max(verbose, 0)
    pepit_tau = problem.solve(verbose=pepit_verbose)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = gamma / n

    # Print conclusion if required
    if verbose != -1:
        print('*** Example file: worst-case performance of the NoLips_2 in Bregman distance ***')
        print('\tPEPit guarantee:\t min_t Dh(x_(t-1), x_(t)) <= {:.6} (F(x_0) - F(x_n))'.format(pepit_tau))
        print('\tTheoretical guarantee :\t min_t Dh(x_(t-1), x_(t)) <= {:.6} (F(x_0) - F(x_n))'.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the upper theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":

    L = 1
    gamma = 1 / L
    pepit_tau, theoretical_tau = wc_no_lips_2(L=L, gamma=gamma, n=3, verbose=1)
