from .inexact_gradient import wc_inexact_gradient
from .optimized_gradient import wc_optimized_gradient
from .frank_wolfe import wc_frank_wolfe
from .proximal_point import wc_proximal_point
from .halpern_iteration import wc_halpern_iteration
from .gradient_descent import wc_gradient_descent
from .alternate_projections import wc_alternate_projections
from .averaged_projections import wc_averaged_projections
from .dykstra import wc_dykstra

__all__ = ['inexact_gradient', 'wc_inexact_gradient',
           'optimized_gradient.py', 'wc_optimized_gradient',
           'frank_wolfe.py', 'wc_frank_wolfe',
           'proximal_point.py', 'wc_proximal_point',
           'halpern_iteration.py', 'wc_halpern_iteration',
           'alternate_projections.py', 'wc_alternate_projections',
           'averaged_projections.py', 'wc_averaged_projections',
           'dykstra.py', 'wc_dykstra',
           ]
