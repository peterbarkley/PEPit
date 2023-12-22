# PEPit: Performance Estimation in Python

[![Build Status](https://github.com/PerformanceEstimation/PEPit/actions/workflows/tests.yaml/badge.svg?branch=master&event=push)](https://github.com/PerformanceEstimation/PEPit/actions)
[![Codecov Status](https://codecov.io/gh/PerformanceEstimation/PEPit/branch/master/graph/badge.svg?token=NwT4oACGS4)](https://codecov.io/gh/PerformanceEstimation/PEPit)
[![Documentation Status](https://readthedocs.org/projects/pepit/badge/?version=latest)](https://pepit.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/PEPit.svg)](https://pypi.python.org/pypi/PEPit/)
[![Downloads](https://static.pepy.tech/badge/pepit)](https://pepy.tech/project/pepit)
[![License](https://img.shields.io/github/license/PerformanceEstimation/PEPit.svg)](https://github.com/PerformanceEstimation/PEPit/blob/master/LICENSE)

This open source Python library provides a generic way to use PEP framework in Python.
Performance estimation problems were introduced in 2014 by **Yoel Drori** and **Marc Teboulle**, see [1].
PEPit is mainly based on the formalism and developments from [2, 3] by a subset of the authors of this toolbox.
A friendly informal introduction to this formalism is available in this [blog post](https://francisbach.com/computer-aided-analyses/)
and a corresponding Matlab library is presented in [4] ([PESTO](https://github.com/AdrienTaylor/Performance-Estimation-Toolbox)).

Website and documentation of PEPit: [https://pepit.readthedocs.io/](https://pepit.readthedocs.io/)

Source Code (MIT): [https://github.com/PerformanceEstimation/PEPit](https://github.com/PerformanceEstimation/PEPit)

## Using and citing the toolbox

This code comes jointly with the following [`reference`](https://arxiv.org/pdf/2201.04040.pdf):

    B. Goujaud, C. Moucer, F. Glineur, J. Hendrickx, A. Taylor, A. Dieuleveut (2022).
    "PEPit: computer-assisted worst-case analyses of first-order optimization methods in Python."

When using the toolbox in a project, please refer to this note via this Bibtex entry:

```bibtex
@article{pepit2022,
  title={{PEPit}: computer-assisted worst-case analyses of first-order optimization methods in {P}ython},
  author={Goujaud, Baptiste and Moucer, C\'eline and Glineur, Fran\c{c}ois and Hendrickx, Julien and Taylor, Adrien and Dieuleveut, Aymeric},
  journal={arXiv preprint arXiv:2201.04040},
  year={2022}
}
```


## Demo [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PerformanceEstimation/PEPit/blob/master/ressources/demo/PEPit_demo.ipynb)


This [notebook](https://github.com/PerformanceEstimation/PEPit/blob/master/ressources/demo/PEPit_demo.ipynb) provides a demonstration of how to use PEPit to obtain a worst-case guarantee on a simple algorithm (gradient descent), and a more advanced analysis of three other examples.




## Installation

The library has been tested on Linux and MacOSX.
It relies on the following Python modules:

- Numpy
- Scipy
- Cvxpy
- Matplotlib (for the demo notebook)


### Pip installation

You can install the toolbox through PyPI with:

```console
pip install pepit
```

or get the very latest version by running:

```console
pip install -U https://github.com/PerformanceEstimation/PEPit/archive/master.zip # with --user for user install (no root)
```

### Post installation check
After a correct installation, you should be able to import the module without errors:

```python
import PEPit
```

### Online environment
You can also try the package in this Binder repository. [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/PerformanceEstimation/PEPit/HEAD)

## Example

The folder [Examples](https://pepit.readthedocs.io/en/latest/examples.html#) contains numerous introductory examples to the toolbox.

Among the other examples, the following code (see [`GradientMethod`](https://pepit.readthedocs.io/en/latest/examples/a.html#gradient-descent))
generates a worst-case scenario for <img src="https://render.githubusercontent.com/render/math?math=N"> iterations of the gradient method, applied to the minimization of a smooth (possibly strongly) convex function f(x).
More precisely, this code snippet allows computing the worst-case value of <img src="https://render.githubusercontent.com/render/math?math=f(x_N)-f_\star"> when <img src="https://render.githubusercontent.com/render/math?math=x_N"> is generated by gradient descent, and when <img src="https://render.githubusercontent.com/render/math?math=\|x_0-x_\star\|=1">.

```Python
from PEPit import PEP
from PEPit.functions import SmoothConvexFunction


def wc_gradient_descent(L, gamma, n, wrapper="cvxpy", solver=None, verbose=1):
    """
    Consider the convex minimization problem

    .. math:: f_\\star \\triangleq \\min_x f(x),

    where :math:`f` is :math:`L`-smooth and convex.

    This code computes a worst-case guarantee for **gradient descent** with fixed step-size :math:`\\gamma`.
    That is, it computes the smallest possible :math:`\\tau(n, L, \\gamma)` such that the guarantee

    .. math:: f(x_n) - f_\\star \\leqslant \\tau(n, L, \\gamma) \\|x_0 - x_\\star\\|^2

    is valid, where :math:`x_n` is the output of gradient descent with fixed step-size :math:`\\gamma`, and
    where :math:`x_\\star` is a minimizer of :math:`f`.

    In short, for given values of :math:`n`, :math:`L`, and :math:`\\gamma`,
    :math:`\\tau(n, L, \\gamma)` is computed as the worst-case
    value of :math:`f(x_n)-f_\\star` when :math:`\\|x_0 - x_\\star\\|^2 \\leqslant 1`.

    **Algorithm**:
    Gradient descent is described by

    .. math:: x_{t+1} = x_t - \\gamma \\nabla f(x_t),

    where :math:`\\gamma` is a step-size.

    **Theoretical guarantee**:
    When :math:`\\gamma \\leqslant \\frac{1}{L}`, the **tight** theoretical guarantee can be found in [1, Theorem 3.1]:

    .. math:: f(x_n)-f_\\star \\leqslant \\frac{L}{4nL\\gamma+2} \\|x_0-x_\\star\\|^2,

    which is tight on some Huber loss functions.

    **References**:

    `[1] Y. Drori, M. Teboulle (2014).
    Performance of first-order methods for smooth convex minimization: a novel approach.
    Mathematical Programming 145(1–2), 451–482.
    <https://arxiv.org/pdf/1206.3209.pdf>`_

    Args:
        L (float): the smoothness parameter.
        gamma (float): step-size.
        n (int): number of iterations.
        wrapper (str): the name of the wrapper to be used.
        solver (str): the name of the solver the wrapper should use.
        verbose (int): level of information details to print.
                        
                        - -1: No verbose at all.
                        - 0: This example's output.
                        - 1: This example's output + PEPit information.
                        - 2: This example's output + PEPit information + solver details.

    Returns:
        pepit_tau (float): worst-case value
        theoretical_tau (float): theoretical value

    Example:
        >>> L = 3
        >>> pepit_tau, theoretical_tau = wc_gradient_descent(L=L, gamma=1 / L, n=4, wrapper="cvxpy", solver=None, verbose=1)
        (PEPit) Setting up the problem: size of the Gram matrix: 7x7
        (PEPit) Setting up the problem: performance measure is minimum of 1 element(s)
        (PEPit) Setting up the problem: Adding initial conditions and general constraints ...
        (PEPit) Setting up the problem: initial conditions and general constraints (1 constraint(s) added)
        (PEPit) Setting up the problem: interpolation conditions for 1 function(s)
        			Function 1 : Adding 30 scalar constraint(s) ...
        			Function 1 : 30 scalar constraint(s) added
        (PEPit) Setting up the problem: additional constraints for 0 function(s)
        (PEPit) Compiling SDP
        (PEPit) Calling SDP solver
        (PEPit) Solver status: optimal (wrapper:cvxpy, solver: MOSEK); optimal value: 0.1666666649793712
        (PEPit) Primal feasibility check:
        		The solver found a Gram matrix that is positive semi-definite up to an error of 6.325029587061441e-10
        		All the primal scalar constraints are verified up to an error of 6.633613956752438e-09
        (PEPit) Dual feasibility check:
        		The solver found a residual matrix that is positive semi-definite
        		All the dual scalar values associated to inequality constraints are nonnegative up to an error of 7.0696173743789816e-09
        (PEPit) The worst-case guarantee proof is perfectly reconstituted up to an error of 7.547098305159261e-08
        (PEPit) Final upper bound (dual): 0.16666667331941884 and lower bound (primal example): 0.1666666649793712
        (PEPit) Duality gap: absolute: 8.340047652488636e-09 and relative: 5.004028642152831e-08
        *** Example file: worst-case performance of gradient descent with fixed step-sizes ***
        	PEPit guarantee:		 f(x_n)-f_* <= 0.166667 ||x_0 - x_*||^2
        	Theoretical guarantee:	 f(x_n)-f_* <= 0.166667 ||x_0 - x_*||^2

    """

    # Instantiate PEP
    problem = PEP()

    # Declare a smooth convex function
    func = problem.declare_function(SmoothConvexFunction, L=L)

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.stationary_point()
    fs = func(xs)

    # Then define the starting point x0 of the algorithm
    x0 = problem.set_initial_point()

    # Set the initial constraint that is the distance between x0 and x^*
    problem.set_initial_condition((x0 - xs) ** 2 <= 1)

    # Run n steps of the GD method
    x = x0
    for _ in range(n):
        x = x - gamma * func.gradient(x)

    # Set the performance metric to the function values accuracy
    problem.set_performance_metric(func(x) - fs)

    # Solve the PEP
    pepit_verbose = max(verbose, 0)
    pepit_tau = problem.solve(wrapper=wrapper, solver=solver, verbose=pepit_verbose)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = L / (2 * (2 * n * L * gamma + 1))

    # Print conclusion if required
    if verbose != -1:
        print('*** Example file: worst-case performance of gradient descent with fixed step-sizes ***')
        print('\tPEPit guarantee:\t\t f(x_n)-f_* <= {:.6} ||x_0 - x_*||^2'.format(pepit_tau))
        print('\tTheoretical guarantee:\t f(x_n)-f_* <= {:.6} ||x_0 - x_*||^2'.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":
    L = 3
    pepit_tau, theoretical_tau = wc_gradient_descent(L=L, gamma=1 / L, n=4, wrapper="cvxpy", solver=None, verbose=1)

```

### Included tools

A lot of common optimization methods can be studied through this framework,
using numerous steps and under a large variety of function / operator classes.

PEPit provides the following [steps](https://pepit.readthedocs.io/en/latest/api/steps.html) (often referred to as "oracles"):

- [Inexact gradient step](https://pepit.readthedocs.io/en/latest/api/steps.html#inexact-gradient-step)
- [Exact line-search step](https://pepit.readthedocs.io/en/latest/api/steps.html#exact-line-search-step)
- [Proximal step](https://pepit.readthedocs.io/en/latest/api/steps.html#proximal-step)
- [Inexact proximal step](https://pepit.readthedocs.io/en/latest/api/steps.html#inexact-proximal-step)
- [Bregman gradient step](https://pepit.readthedocs.io/en/latest/api/steps.html#bregman-gradient-step)
- [Bregman proximal step](https://pepit.readthedocs.io/en/latest/api/steps.html#bregman-proximal-step)
- [Linear optimization step](https://pepit.readthedocs.io/en/latest/api/steps.html#linear-optimization-step)
- [Epsilon-subgradient step](https://pepit.readthedocs.io/en/latest/api/steps.html#epsilon-subgradient-step)

PEPit provides the following [function classes](https://pepit.readthedocs.io/en/latest/api/functions.html) CNIs:

- [Convex](https://pepit.readthedocs.io/en/latest/api/functions.html#convex)
- [Strongly convex](https://pepit.readthedocs.io/en/latest/api/functions.html#strongly-convex)
- [Smooth](https://pepit.readthedocs.io/en/latest/api/functions.html#smooth)
- [Convex and smooth](https://pepit.readthedocs.io/en/latest/api/functions.html#convex-and-smooth)
- [Strongly convex and smooth](https://pepit.readthedocs.io/en/latest/api/functions.html#strongly-convex-and-smooth)
- [Convex and Lipschitz continuous](https://pepit.readthedocs.io/en/latest/api/functions.html#convex-and-lipschitz-continuous)
- [Convex indicator](https://pepit.readthedocs.io/en/latest/api/functions.html#convex-indicator)
- [Convex support](https://pepit.readthedocs.io/en/latest/api/functions.html#convex-support-functions)
- [Convex quadratically growing](https://pepit.readthedocs.io/en/latest/api/functions.html#convex-and-quadratically-upper-bounded)
- [Functions verifying restricted secant inequality and upper error bound](https://pepit.readthedocs.io/en/latest/api/functions.html#restricted-secant-inequality-and-error-bound)

PEPit provides the following [operator classes](https://pepit.readthedocs.io/en/latest/api/operators.html) CNIs:

- [Monotone](https://pepit.readthedocs.io/en/latest/api/operators.html#monotone)
- [Strongly monotone](https://pepit.readthedocs.io/en/latest/api/operators.html#strongly-monotone)
- [Lipschitz continuous](https://pepit.readthedocs.io/en/latest/api/operators.html#lipschitz-continuous)
- [Strongly monotone and Lipschitz continuous](https://pepit.readthedocs.io/en/latest/api/operators.html#strongly-monotone-and-lipschitz-continuous)
- [Cocoercive](https://pepit.readthedocs.io/en/latest/api/operators.html#cocoercive)


## Authors

This toolbox has been created by

- [**Baptiste Goujaud**](https://www.linkedin.com/in/baptiste-goujaud-b60060b3/) 
- [**Céline Moucer**](https://cmoucer.github.io)
- [**Julien Hendrickx**](https://perso.uclouvain.be/julien.hendrickx/index.html)
- [**François Glineur**](https://perso.uclouvain.be/francois.glineur/)
- [**Adrien Taylor**](https://adrientaylor.github.io/)
- [**Aymeric Dieuleveut**](http://www.cmap.polytechnique.fr/~aymeric.dieuleveut/)

### Acknowledgments

The authors would like to thank [**Rémi Flamary**](https://remi.flamary.com/)
for his feedbacks on preliminary versions of the toolbox,
as well as for support regarding the continuous integration.

## Contributions

All external contributions are welcome.
Please read the [contribution guidelines](https://pepit.readthedocs.io/en/latest/contributing.html).

## References

[1] Y. Drori, M. Teboulle (2014).
[Performance of first-order methods for smooth convex minimization: a novel approach.](https://arxiv.org/pdf/1206.3209.pdf)
Mathematical Programming 145(1–2), 451–482.

[2] A. Taylor, J. Hendrickx, F. Glineur (2017).
[Smooth strongly convex interpolation and exact worst-case performance of first-order methods.](https://arxiv.org/pdf/1502.05666.pdf)
Mathematical Programming, 161(1-2), 307-345.

[3] A. Taylor, J. Hendrickx, F. Glineur (2017).
[Exact worst-case performance of first-order methods for composite convex optimization.](https://arxiv.org/pdf/1512.07516.pdf)
SIAM Journal on Optimization, 27(3):1283–1313.

[4] A. Taylor, J. Hendrickx, F. Glineur (2017).
[Performance Estimation Toolbox (PESTO): automated worst-case analysis of first-order optimization methods.](https://adrientaylor.github.io/share/PESTO_CDC_2017.pdf)
In 56th IEEE Conference on Decision and Control (CDC).

[5] A. d’Aspremont, D. Scieur, A. Taylor (2021).
[Acceleration Methods.](https://arxiv.org/pdf/2101.09545.pdf)
Foundations and Trends in Optimization: Vol. 5, No. 1-2.

[6] O. Güler (1992).
[New proximal point algorithms for convex minimization.](https://epubs.siam.org/doi/abs/10.1137/0802032?mobileUi=0)
SIAM Journal on Optimization, 2(4):649–664.

[7] Y. Drori (2017).
[The exact information-based complexity of smooth convex minimization.](https://arxiv.org/pdf/1606.01424.pdf)
Journal of Complexity, 39, 1-16.

[8] E. De Klerk, F. Glineur, A. Taylor (2017).
[On the worst-case complexity of the gradient method with exact line search for smooth strongly convex functions.](https://link.springer.com/content/pdf/10.1007/s11590-016-1087-4.pdf)
Optimization Letters, 11(7), 1185-1199.

[9] B.T. Polyak (1964).
[Some methods of speeding up the convergence of iteration method.](https://www.sciencedirect.com/science/article/pii/0041555364901375)
URSS Computational Mathematics and Mathematical Physics.

[10] E. Ghadimi, H. R. Feyzmahdavian, M. Johansson (2015).
[Global convergence of the Heavy-ball method for convex optimization.](https://arxiv.org/pdf/1412.7457.pdf)
European Control Conference (ECC).

[11] E. De Klerk, F. Glineur, A. Taylor (2020).
[Worst-case convergence analysis of inexact gradient and Newton methods through semidefinite programming performance estimation.](https://arxiv.org/pdf/1709.05191.pdf)
SIAM Journal on Optimization, 30(3), 2053-2082.

[12] O. Gannot (2021).
[A frequency-domain analysis of inexact gradient methods.](https://arxiv.org/pdf/1912.13494.pdf)
Mathematical Programming.

[13] D. Kim, J. Fessler (2016).
[Optimized first-order methods for smooth convex minimization.](https://arxiv.org/pdf/1406.5468.pdf)
Mathematical Programming 159.1-2: 81-107.

[14] S. Cyrus, B. Hu, B. Van Scoy, L. Lessard (2018).
[A robust accelerated optimization algorithm for strongly convex functions.](https://arxiv.org/pdf/1710.04753.pdf)
American Control Conference (ACC).

[15] Y. Nesterov (2003).
[Introductory lectures on convex optimization: A basic course.](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.693.855&rep=rep1&type=pdf)
Springer Science & Business Media.

[16] S. Boyd, L. Xiao, A. Mutapcic (2003).
[Subgradient Methods (lecture notes).](https://web.stanford.edu/class/ee392o/subgrad_method.pdf)

[17] Y. Drori, M. Teboulle (2016).
[An optimal variant of Kelley's cutting-plane method.](https://arxiv.org/pdf/1409.2636.pdf)
Mathematical Programming, 160(1), 321-351.

[18] Van Scoy, B., Freeman, R. A., Lynch, K. M. (2018).
[The fastest known globally convergent first-order method for minimizing strongly convex functions.](http://www.optimization-online.org/DB_FILE/2017/03/5908.pdf)
IEEE Control Systems Letters, 2(1), 49-54.

[19] P. Patrinos, L. Stella, A. Bemporad (2014).
[Douglas-Rachford splitting: Complexity estimates and accelerated variants.](https://arxiv.org/pdf/1407.6723.pdf)
In 53rd IEEE Conference on Decision and Control (CDC).

[20] Y. Censor, S.A. Zenios (1992).
[Proximal minimization algorithm with D-functions.](https://link.springer.com/content/pdf/10.1007/BF00940051.pdf)
Journal of Optimization Theory and Applications, 73(3), 451-464.

[21] E. Ryu, S. Boyd (2016).
[A primer on monotone operator methods.](https://web.stanford.edu/~boyd/papers/pdf/monotone_primer.pdf)
Applied and Computational Mathematics 15(1), 3-43.

[22] E. Ryu, A. Taylor, C. Bergeling, P. Giselsson (2020).
[Operator splitting performance estimation: Tight contraction factors and optimal parameter selection.](https://arxiv.org/pdf/1812.00146.pdf)
SIAM Journal on Optimization, 30(3), 2251-2271.

[23] P. Giselsson, and S. Boyd (2016).
[Linear convergence and metric selection in Douglas-Rachford splitting and ADMM.](https://arxiv.org/pdf/1410.8479.pdf)
IEEE Transactions on Automatic Control, 62(2), 532-544.

[24] M .Frank, P. Wolfe (1956).
An algorithm for quadratic programming.
Naval research logistics quarterly, 3(1-2), 95-110.

[25] M. Jaggi (2013).
[Revisiting Frank-Wolfe: Projection-free sparse convex optimization.](http://proceedings.mlr.press/v28/jaggi13.pdf)
In 30th International Conference on Machine Learning (ICML).

[26] A. Auslender, M. Teboulle (2006).
[Interior gradient and proximal methods for convex and conic optimization.](https://epubs.siam.org/doi/pdf/10.1137/S1052623403427823)
SIAM Journal on Optimization 16.3 (2006): 697-725.

[27] H.H. Bauschke, J. Bolte, M. Teboulle (2017).
[A Descent Lemma Beyond Lipschitz Gradient Continuity: First-Order Methods Revisited and Applications.](https://cmps-people.ok.ubc.ca/bauschke/Research/103.pdf)
Mathematics of Operations Research, 2017, vol. 42, no 2, p. 330-348

[28] R. Dragomir, A. Taylor, A. d’Aspremont, J. Bolte (2021).
[Optimal complexity and certification of Bregman first-order methods.](https://arxiv.org/pdf/1911.08510.pdf)
Mathematical Programming, 1-43.

[29] A. Taylor, J. Hendrickx, F. Glineur (2018).
[Exact worst-case convergence rates of the proximal gradient method for composite convex minimization.](https://arxiv.org/pdf/1705.04398.pdf)
Journal of Optimization Theory and Applications, 178(2), 455-476.

[30] B. Polyak (1987).
Introduction to Optimization.
Optimization Software New York.

[31] L. Lessard, B. Recht, A. Packard (2016).
[Analysis and design of optimization algorithms via integral quadratic constraints.](https://arxiv.org/pdf/1408.3595.pdf)
SIAM Journal on Optimization 26(1), 57–95.

[32] D. Davis, W. Yin (2017).
[A three-operator splitting scheme and its optimization applications.](https://arxiv.org/pdf/1504.01032.pdf)
Set-valued and variational analysis, 25(4), 829-858.

[33] Taylor, A. B. (2017).
[Convex interpolation and performance estimation of first-order methods for convex optimization.](https://dial.uclouvain.be/downloader/downloader.php?pid=boreal:182881&datastream=PDF_01)
PhD Thesis, UCLouvain.

[34] H. Abbaszadehpeivasti, E. de Klerk, M. Zamani (2021).
[The exact worst-case convergence rate of the gradient method with fixed step lengths for L-smooth functions.](https://arxiv.org/pdf/2104.05468v3.pdf)
arXiv 2104.05468.

[35] J. Bolte, S. Sabach, M. Teboulle, Y. Vaisbourd (2018).
[First order methods beyond convexity and Lipschitz gradient continuity with applications to quadratic inverse problems.](https://arxiv.org/pdf/1706.06461.pdf)
SIAM Journal on Optimization, 28(3), 2131-2151.

[36] A. Defazio (2016).
[A simple practical accelerated method for finite sums.](https://proceedings.neurips.cc/paper/2016/file/4f6ffe13a5d75b2d6a3923922b3922e5-Paper.pdf)
Advances in Neural Information Processing Systems (NIPS), 29, 676-684.

[37] A. Defazio, F. Bach, S. Lacoste-Julien (2014).
[SAGA: A fast incremental gradient method with support for non-strongly convex composite objectives.](http://papers.nips.cc/paper/2014/file/ede7e2b6d13a41ddf9f4bdef84fdc737-Paper.pdf)
In Advances in Neural Information Processing Systems (NIPS).

[38] B. Hu, P. Seiler, L. Lessard (2020).
[Analysis of biased stochastic gradient descent using sequential semidefinite programs.](https://arxiv.org/pdf/1711.00987.pdf)
Mathematical programming.

[39] A. Taylor, F. Bach (2019).
[Stochastic first-order methods: non-asymptotic and computer-aided analyses via potential functions.](https://arxiv.org/pdf/1902.00947.pdf)
Conference on Learning Theory (COLT).

[40] D. Kim (2021).
[Accelerated proximal point method for maximally monotone operators.](https://arxiv.org/pdf/1905.05149v4.pdf)
Mathematical Programming, 1-31.

[41] W. Moursi, L. Vandenberghe (2019).
[Douglas–Rachford Splitting for the Sum of a Lipschitz Continuous and a Strongly Monotone Operator.](https://arxiv.org/pdf/1805.09396.pdf)
Journal of Optimization Theory and Applications 183, 179–198.

[42] G. Gu, J. Yang (2020).
[Tight sublinear convergence rate of the proximal point algorithm for maximal monotone inclusion problem.](https://epubs.siam.org/doi/pdf/10.1137/19M1299049)
SIAM Journal on Optimization, 30(3), 1905-1921.

[43] B. Halpern (1967).
[Fixed points of nonexpanding maps.](https://www.ams.org/journals/bull/1967-73-06/S0002-9904-1967-11864-0/S0002-9904-1967-11864-0.pdf)
American Mathematical Society, 73(6), 957–961.

[44] F. Lieder (2021).
[On the convergence rate of the Halpern-iteration.](http://www.optimization-online.org/DB_FILE/2017/11/6336.pdf)
Optimization Letters, 15(2), 405-418.

[45] F. Lieder (2018).
[Projection Based Methods for Conic Linear Programming Optimal First Order Complexities and Norm Constrained Quasi Newton Methods.](https://docserv.uni-duesseldorf.de/servlets/DerivateServlet/Derivate-49971/Dissertation.pdf)
PhD thesis, HHU Düsseldorf.

[46] Y. Nesterov (1983).
[A method for solving the convex programming problem with convergence rate O(1/k^2).](http://www.mathnet.ru/links/9bcb158ed2df3d8db3532aafd551967d/dan46009.pdf)
In Dokl. akad. nauk Sssr (Vol. 269, pp. 543-547).

[47] N. Bansal, A. Gupta (2019).
[Potential-function proofs for gradient methods.](https://arxiv.org/pdf/1712.04581.pdf)
Theory of Computing, 15(1), 1-32.

[48] M. Barre, A. Taylor, F. Bach (2021).
[A note on approximate accelerated forward-backward methods with absolute and relative errors, and possibly strongly convex objectives.](https://arxiv.org/pdf/2106.15536v2.pdf)
arXiv:2106.15536v2.

[49] J. Eckstein and W. Yao (2018).
[Relative-error approximate versions of Douglas–Rachford splitting and special cases of the ADMM.](https://link.springer.com/article/10.1007/s10107-017-1160-5)
Mathematical Programming, 170(2), 417-444.

[50] M. Barré, A. Taylor, A. d’Aspremont (2020).
[Complexity guarantees for Polyak steps with momentum.](https://arxiv.org/pdf/2002.00915.pdf)
In Conference on Learning Theory (COLT).

[51] D. Kim, J. Fessler (2017).
[On the convergence analysis of the optimized gradient method.](https://arxiv.org/pdf/1510.08573.pdf)
Journal of Optimization Theory and Applications, 172(1), 187-205.

[52] Steven Diamond and Stephen Boyd (2016).
[CVXPY: A Python-embedded modeling language for convex optimization.](https://arxiv.org/pdf/1603.00943.pdf)
Journal of Machine Learning Research (JMLR) 17.83.1--5 (2016).

[53] Agrawal, Akshay and Verschueren, Robin and Diamond, Steven and Boyd, Stephen (2018).
[A rewriting system for convex optimization problems.](https://arxiv.org/pdf/1709.04494.pdf)
Journal of Control and Decision (JCD) 5.1.42--60 (2018).

[54] Adrien Taylor, Bryan Van Scoy, Laurent Lessard (2018).
[Lyapunov Functions for First-Order Methods: Tight Automated Convergence Guarantees.](https://arxiv.org/pdf/1803.06073.pdf)
International Conference on Machine Learning (ICML).

[55] C. Guille-Escuret, B. Goujaud, A. Ibrahim, I. Mitliagkas (2022).
[Gradient Descent Is Optimal Under Lower Restricted Secant Inequality And Upper Error Bound.](https://arxiv.org/pdf/2203.00342.pdf)

[56] B. Goujaud, A. Taylor, A. Dieuleveut (2022).
[Optimal first-order methods for convex functions with a quadratic upper bound.](https://arxiv.org/pdf/2205.15033.pdf)

[57] W. Su, S. Boyd, E. J. Candès (2016).
[A differential equation for modeling Nesterov's accelerated gradient method: Theory and insights.](https://jmlr.org/papers/volume17/15-084/15-084.pdf)
In the Journal of Machine Learning Research (JMLR).

[58] C. Moucer, A. Taylor, F. Bach (2022).
[A systematic approach to Lyapunov analyses of continuous-time models in convex optimization.](https://arxiv.org/pdf/2205.12772.pdf)

[59] A. C. Wilson, B. Recht, M. I. Jordan (2021).
[A Lyapunov analysis of accelerated methods in optimization.](https://jmlr.org/papers/volume22/20-195/20-195.pdf)
In the Journal of Machine Learning Reasearch (JMLR), 22(113):1−34, 2021.

[60] J.M. Sanz-Serna and K. C. Zygalakis (2021)
[The connections between Lyapunov functions for some optimization algorithms and differential equations.](https://arxiv.org/pdf/2009.00673.pdf)
In SIAM Journal on Numerical Analysis, 59 pp 1542-1565.

[61] D. Scieur, V. Roulet, F. Bach and A. D'Aspremont (2017).
[Integration methods and accelerated optimization algorithms.](https://papers.nips.cc/paper/2017/file/bf62768ca46b6c3b5bea9515d1a1fc45-Paper.pdf)
In Advances in Neural Information Processing Systems (NIPS).

[62] J. Park, E. Ryu (2022).
[Exact Optimal Accelerated Complexity for Fixed-Point Iterations.](https://proceedings.mlr.press/v162/park22c/park22c.pdf)
In 39th International Conference on Machine Learning (ICML).

[63] M. Barre, A. Taylor, F. Bach (2020).
[Principled analyses and design of first-order methods with inexact proximal operators.](https://arxiv.org/pdf/2006.06041v2.pdf)

[64] Y. Drori and A. Taylor (2020).
[Efficient first-order methods for convex minimization: a constructive approach.](https://arxiv.org/pdf/1803.05676.pdf)
Mathematical Programming 184 (1), 183-220.

[65] Z. Shi, R. Liu (2016).
[Better worst-case complexity analysis of the block coordinate descent method for large scale machine learning.](https://arxiv.org/pdf/1608.04826.pdf)
In 2017 16th IEEE International Conference on Machine Learning and Applications (ICMLA).

[66] R.D. Millán, M.P. Machado (2019).
[Inexact proximal epsilon-subgradient methods for composite convex optimization problems.](https://arxiv.org/pdf/1805.10120.pdf)
Journal of Global Optimization 75.4 (2019): 1029-1060.

[67] M. Kirszbraun (1934).
Uber die zusammenziehende und Lipschitzsche transformationen.
Fundamenta Mathematicae, 22 (1934).

[68] F.A. Valentine (1943).
On the extension of a vector function so as to preserve a Lipschitz condition.
Bulletin of the American Mathematical Society, 49 (2).

[69] F.A. Valentine (1945).
A Lipschitz condition preserving extension for a vector function.
American Journal of Mathematics, 67(1).

[70] M. Kirszbraun (1934).
Uber die zusammenziehende und Lipschitzsche transformationen.
Fundamenta Mathematicae, 22 (1934).

[71] F.A. Valentine (1943).
On the extension of a vector function so as to preserve a Lipschitz condition.
Bulletin of the American Mathematical Society, 49 (2).

[72] F.A. Valentine (1945).
A Lipschitz condition preserving extension for a vector function.
American Journal of Mathematics, 67(1).

[73] E. Gorbunov, A. Taylor, S. Horváth, G. Gidel (2023).
[Convergence of proximal point and extragradient-based methods beyond monotonicity: the case of negative comonotonicity.](https://proceedings.mlr.press/v202/gorbunov23a/gorbunov23a.pdf)
International Conference on Machine Learning.

[74] A. Brøndsted, R.T. Rockafellar.
[On the subdifferentiability of convex functions.](https://www.jstor.org/stable/2033889)
Proceedings of the American Mathematical Society 16(4), 605–611 (1965)

[75] R.T. Rockafellar (1976).
[Monotone operators and the proximal point algorithm.](https://epubs.siam.org/doi/pdf/10.1137/0314056)
SIAM journal on control and optimization, 14(5), 877-898.

[76] R.D. Monteiro, B.F. Svaiter (2013).
[An accelerated hybrid proximal extragradient method for convex optimization and its implications to second-order methods.](https://epubs.siam.org/doi/abs/10.1137/110833786)
SIAM Journal on Optimization, 23(2), 1092-1125.

[77] S. Salzo, S. Villa (2012).
[Inexact and accelerated proximal point algorithms.](http://www.optimization-online.org/DB_FILE/2011/08/3128.pdf)
Journal of Convex analysis, 19(4), 1167-1192.

[78] H. H. Bauschke and P. L. Combettes (2017).
Convex Analysis and Monotone Operator Theory in Hilbert Spaces.
Springer New York, 2nd ed.

[79] B. Goujaud, C. Moucer, F. Glineur, J. Hendrickx, A. Taylor, A. Dieuleveut (2022).
[PEPit: computer-assisted worst-case analyses of first-order optimization methods in Python.](https://arxiv.org/pdf/2201.04040.pdf)
