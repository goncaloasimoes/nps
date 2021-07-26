import time
from src.Simulator import Simulator
from src.Parameters.IntervalParameter import IntervalParameter
from src.Parameters.ListParameter import ListParameter
import winsound

parameters = {
    'sizes':         [1000],
    'steps':         1000,
    'save_location': './Data/BA/',
    'filename':      'new',
    'show_legend':   True,
    'beta':          IntervalParameter('beta', 0, 0.80, 0.1),
    'gamma':         IntervalParameter('gamma', .1, .1, .1),
    'delta':         IntervalParameter('delta', .1, .1, .1),
    'theta':         IntervalParameter('theta', 0.8, .8, 1),
    'zeta':          IntervalParameter('zeta', 0, .80, .1),
    'timescale':     ListParameter( 'timescale', [ 0.5, 1, 2, 4 ] ),
    'vaccinate':     IntervalParameter('vaccinate', 1, 1, 0.05 ),
    'infect':        IntervalParameter('infect', 1, 1, 1),
}

start = time.time()
s = Simulator( 'rSIR_csV', [ 'SameBA' ], { 'inf': [ 'Random' ], 'vac': [ 'Acquaintance' ] }, parameters, 'SaveLast' )
s.simulate()

end = time.time()
print('total:', end - start)