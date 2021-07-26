# Choose the strategy to get given its string name
# pylint: disable=relative-beyond-top-level
from . import Random
from pydoc import locate

# TODO:
known_strategies = {
    'RandomVac': Random.Random,
}

def get_strategy(name):
    if name in known_strategies:
        return known_strategies[name]
    strategy_class = locate(".src.Strategies." + name + '.' + name)
    if strategy_class == None:
        raise Exception('Strategy ' + name + ' does not exist.')
    return strategy_class