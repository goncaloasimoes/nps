#!/usr/bin/python

import sys, getopt
import unittest
import time
# pylint: disable=import-error
from src.Simulator import Simulator
from src.Parameters.IntervalParameter import IntervalParameter
from src.Parameters.ListParameter import ListParameter
from src.Models.SIR import SIR

# TODO: Needs testing.
def main(argv):
    size      = 1000
    model     = 'rSIR_V_T'
    steps     = 300
    network   = 'BA'
    beta      = None
    gamma     = None
    delta     = None
    theta     = None
    timescale = None
    try:
        opts, _ = getopt.getopt( argv, "",[
            'size=',
            'model=',
            'steps=',
            'network=',
            'beta=',
            'gamma=',
            'delta=',
            'theta=',
            'timescale=',
        ] )
    except getopt.GetoptError:
        print( 'test.py TODO' )
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print( 'TOOD: help' )
            sys.exit()
        elif opt == "--size":
            size = arg
        elif opt == "--model":
            model = arg
        elif opt == "--steps":
            steps = arg
        elif opt == "--network":
            network = arg
        elif opt == "--beta":
            beta = arg
        elif opt == "--gamma":
            gamma = arg
        elif opt == "--delta":
            delta = arg
        elif opt == "--theta":
            theta = arg
        elif opt == "--timescale":
            timescale = arg

    #TODO: accept the values for parameters (beta, gamma, etc)
    parameters = {
        'sizes':         [int(size)],
        'steps':         int(steps),
        'save_location': './Data/Example/',
        'filename':      'new',
        'show_legend':   True,
        'beta':          parse_arg( 'beta', beta ), #IntervalParameter('beta', .0, 0.95, .05),
        'gamma':         parse_arg( 'gamma', gamma ), #IntervalParameter('gamma', .1, .1, .1),
        'delta':         parse_arg( 'delta', delta ), #IntervalParameter('delta', .3, .3, .3),
        'theta':         parse_arg( 'theta', theta ), #IntervalParameter('theta', .1, .1, .1),
        'timescale':     parse_arg( 'timescale', timescale ), #ListParameter('timescale', [ 0, 0.5 ]),#1, 2, 4, 8 ] ),
        'vaccinate':     1,
        'infect':        1,
    }

    start = time.time()
    s = Simulator( model, [ network ], { 'vac': [ 'Random' ] }, parameters, 'SaveLast' )
    s.simulate()

    end = time.time()
    print('total:', end - start)

def parse_arg( name, arg ):
    if arg.isnumeric():
        #TODO: add a type of parameter that only has a single value 
        return IntervalParameter( name, int(arg), int(arg), 1.0 )

    try:
        arg = float(arg)
        #TODO: add a type of parameter that only has a single value 
        return IntervalParameter( name, arg, arg, 1.0 )
    except ValueError:
        pass

    split = arg.split(',')
    if len(split) > 1:
        return ListParameter( name, [float(i) for i in split] )

    split = arg.split(':')
    if len(split) == 3:
        return IntervalParameter( name, float(split[0]), float(split[1]), float(split[2]) )

    print( 'Problem with arg ' + name)
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])