from .Parameters.Parameters import Parameters
from .Parameters.IntervalParameter import IntervalParameter
from .Parameters.ListParameter import ListParameter
from .Networks.NetworkGetter import get_network
from .Strategies.StrategyGetter import get_strategy
from .Models.ModelGetter import get_model
from .DataProcessing.DataProcessorGetter import get_data_processor
from .DataProcessing.MultipleProcessing import MultipleProcessing
import random
import time
import statistics

''' Class for simulating propagation/infection events in networks. '''
class Simulator:

    ''' Default sizes to simulate. '''
    default_sizes       = [1000]

    ''' Default steps to run for a simulation.
        Steps define how many times a simulation is ran for each possible combination of the
        passed values.
    '''
    default_steps       = 100

    ''' Parameters for the simulation that do not require special treatment. '''
    basic_parameters    = {}

    ''' Parameters for the simulation that can have multiple values and need to be handled
        differently.
    '''
    interval_parameters = None

    ################################################################################################
    #                                        Initialization                                        #
    #                                                                                              #
    #                          Functions for initializing the simulator.                           #
    #                                                                                              #
    ################################################################################################

    def __init__(self, model, networks, strategies, parameters, data_processors = 'None'):
        self.model = get_model(model)()
        self._init_parameters(parameters)
        self._init_networks(networks)
        self._init_strategies(strategies)
        self._init_data_processor(data_processors)

    def _init_networks(self, networks):
        if not isinstance(networks, list):
            self.networks = [networks]
        else:
            self.networks = networks
        
        for idx, network in enumerate(self.networks):
            self.networks[idx] = get_network(network)

    def _init_strategies(self, strategies):
        self.strategies = {
            'inf': [],
            'vac': [],
        }
        # TODO: Validate dict with purposes and they are arrays for each purpsoe
        # TODO: if for each purpose, check if it is array, if not then turn into array
        if 'inf' not in strategies or len(strategies['inf']) == 0:
            strategies['inf'] = [ 'Random' ]

        for purpose, strats in strategies.items():
            for strat in strats:
                self.strategies[purpose].append(
                    get_strategy(strat)(self.model, purpose, self.basic_parameters)
                )

    def _init_parameters(self, parameters):
        non_interval_parameters = {
            key: value for key, value in parameters.items() 
                if not isinstance(value, (IntervalParameter, ListParameter))
        }
        for key, value in non_interval_parameters.items():
            self.basic_parameters[key] = value
            parameters.pop(key, None)

        # Check necessary attributes if they need default values.
        for necessary in ['sizes', 'steps']:
            if necessary not in self.basic_parameters:
                self.basic_parameters[necessary] = getattr(self, 'default_%s' % necessary)

        self.interval_parameters = Parameters(parameters)
        print("\nParameters Received")
        for key, value in self.basic_parameters.items():
            # TODO: make this better
            if len(key) > 6:
                print("%s \t%s" % (key, value))
            else:
                print("%s \t\t%s" % (key, value))

        print(self.interval_parameters)
        #TODO: missing networks,strategies, etc
        print('No combinations %i' % self.interval_parameters.number_of_combinations())
        print('------------------------------------------------------------')

    def _init_data_processor(self, data_processors):
        if isinstance(data_processors, list):
            self.data_processor = MultipleProcessing(data_processors, self.basic_parameters)
        else:
            self.data_processor = get_data_processor(data_processors)(self.basic_parameters)


    ################################################################################################
    #                                   Simulation                                                 #
    #                                                                                              #
    #                       Functions for running the simulations.                                 #
    #                                                                                              #
    ################################################################################################

    def simulate(self):
        for network in self.networks:
            for size in self.basic_parameters['sizes']:
                for strategy in self.strategies: 
                    self._combinatorial_simulation(network, size, strategy)
                    break #TODO: problem with our 'inf' and 'vac' for strategies, Find a solution for this

    def _combinatorial_simulation(self, network, size, strategy):
        ''' For all value combinations of the parameters, perform a simulation for each. '''
        # Do various simulations using the combinations of all the parameters
        self.data_processor.start_combination_processing()

        while self.interval_parameters.is_next_parameter_available():
            values = self.interval_parameters.get_next_values()
            print( '\033[91mCombination:\033[0m', values)
            self._simulate_for_set_of_param_values(network, size, strategy, values)

        self.data_processor.end_combination_processing()
        self.interval_parameters.reset_all()

    def _simulate_for_set_of_param_values(self, network_class, size, strategy, param_values):
        ''' Simulate all step repeats. '''
        pair_initiators, self_transitions = self._get_pair_and_self_transitions()
        self.model.set_parameters(param_values.get_values())

        times = []
        time_taken = 0
        self._start_set_processing(network_class, size, strategy, param_values)
        for step in range(self.basic_parameters['steps']):

            start = time.time()

            # Initialize network
            network = self._create_and_init_network(network_class, size, param_values)

            self._start_step_processing(step, network, size, strategy, param_values)

            # Make set of nodes that initiate the transitions or are part of single transitions
            watched_states = self._get_watched_states(pair_initiators, self_transitions)
            watched        = self._get_watched(network, pair_initiators, self_transitions)

            self._simulate_one(network, watched, watched_states, step)

            times.append( (time.time() - start) )
            if len(times)%10 == 0:
                time_taken = statistics.median(times)

            self._end_step_processing(step, network, size, strategy, param_values)

            if time_taken == 0.0:
                print( " Time: Calculating..." + ' '*50, end ="\r")
                continue
            time_split = divmod( time_taken * (self.basic_parameters['steps'] - step), 60 )
            if time_split[0] == 0.0:
                print( " Time: %.0fs" % (time_split[1]) + ' '*50, end ="\r")
            else:
                print( " Time: %dm %.0fs" % (time_split[0],time_split[1]) + ' '*50, end ="\r")

        self._end_set_processing(network_class, size, strategy, param_values)

        # TODO: Review these, some of them might already be done.

        ## TODO: when adding to changed_nodes in simulate_one,
        #       check whether node already has a change and don't add it.
        #       OR have a way of tiebreak between them defined in the model class

        ## FIXME: What to do if node 1 and 2 try to change the other one.
        ## FIXME: Say node 1 infects node 2 but node 2 makes node 1 recover. Do both happen?

        ## FIXME: (***) When there can be multiple self transitions, which one goes first?
        ##          Since if the first one suceeds then the rest won't matter. 
        ##          Do we do it by the same order everytime, or random everytime?
        ## FIXME: Dealing with complex contagions?

    def _simulate_one(self, network, watched, watched_states, step):
        ''' Do one full simulation. '''
        # FIXME: process data changed watched_nodes => watched
        self._process_data(network, watched, step) # Get initial data
        time_step = 0
        while not self.model.end_condition(time_step, network):
            # Empty the list of nodes to change.
            #   Both transitions can happen in the same step (meaning one node can infect its neighbors and also recover)
            change_nodes = {}
            states_to_update = self.model.get_states_to_update(network)

            # Go through lists of nodes.
            watched = list(watched)
            random.shuffle(watched)
            for transition in watched:
                # Pair transition
                if type(transition) is tuple:
                    #TODO: have the state in the watched nodes, so we dont have to call the network
                    node     = transition[0]
                    neighbor = transition[1]
                    state = network.get_node_with_attr(node)['state']
                    if state in states_to_update:
                        # If node/neighbor already changed, then continue.
                        # TODO: choose randomly whether to keep this change or get a new one
                        if node in change_nodes or neighbor in change_nodes:
                            continue
                        self._do_pair_transition(node, state, neighbor, network, change_nodes)

                # Self transition
                elif type(transition) is int:
                    #TODO: have the state in the watched nodes, so we dont have to call the network
                    state = network.get_node_with_attr(transition)['state']
                    if state in states_to_update:
                        if transition in change_nodes:
                            continue
                        self._do_self_transition(transition, state, network, change_nodes)
            watched = set(watched)

            # Update the network and the watched_nodes with the changes 
            self._update_states_and_watched(watched, watched_states, change_nodes, network)
            # TODO: change name, pass time_step and above
            self._process_data(network, watched, step)

            time_step += 1


    ################################################################################################
    #                             Network Creation and States                                      #
    #                                                                                              #
    #                Functions for creating a network and dealing with its states.                 #
    #                                                                                              #
    ################################################################################################

    def _create_and_init_network(self, network_class, size, param_values):
        ''' Create the network, initialize it's states and perform the initial infection event. '''
        # Create Network
        network = network_class(size)
        # Initialize states in Network (where do we get the values/function to initialize)
        network.initialize_states(self.model.basic_init()) #TODO: pass model and extra params to define how to initialize
        #   Does this initialization already create the spreader states?
        #   How is this then affected by the strategy if applied right after?
        #   Perhaps we need to apply the strategy before the initialization if valid?
        # If valid, apply strategy here (check param/function of strategy)
        # Apply Vaccinate strategies
        #FIXME: this was rushed to get results. 
        for strategy in self.strategies['vac']:
            strategy.apply_strategy(network, param_values.get_value('vaccinate'))

        # Apply Infection Strategies
        for strategy in self.strategies['inf']:
            strategy.apply_strategy(network, param_values.get_value('infect'))

        # Apply other strategies passed TODO: should this be before infection? So infection is always the last
        #TODO: test this
        for purpose, strategies in self.strategies.items():
            if purpose in [ 'inf', 'vac' ]:
                continue
            for strategy in strategies:
                strategy.apply_strategy(network)
        return network

    def _get_watched_states(self, pair_initiators, self_transitions):
        ''' Get a list of the states that need to be watched, since they initiate transitions (pair or self). '''
        in_pair = set(pair_initiators)
        in_self = set(self_transitions)
        diff = in_self - in_pair
        return pair_initiators + list(diff)

    def _update_states_and_watched(self, watched, watched_states, changes, network):
        ''' Update the watched nodes with the new changes. '''
        # Apply changes to network.
        for node, new_state in changes.items():
            network.set_node_state(node, new_state)

        # Remove transitions from watched that are no longer valid.
        to_remove_transitions = set()
        for transition in watched:
            if (
                type(transition) is tuple
                and ( transition[0] in changes or transition[1] in changes )
            ):
                to_remove_transitions.add(transition)
            elif type(transition) is int and transition in changes:
                to_remove_transitions.add(transition)
        watched.difference_update(to_remove_transitions)

        transitions = self.model.get_transitions()
        # Add new transitions that are now possible given the changes.
        to_add_transitions = set()
        for node, new_state in changes.items():
            # Check self transitions
            if transitions.check_if_self_transition_exists( new_state ):
                watched.add( node )

            # Check if node has pair transitions
            if not transitions.check_if_state_has_pair_transitions( new_state ):
                continue

            # Check those pair transitions
            for neighbor in network.neighbors( node ):
                neighbor_state = network.get_node_with_attr( neighbor )['state']
                # Check bothways, set makes sure there are no duplicates
                if transitions.check_if_receiver_available( new_state, neighbor_state ):
                    watched.add( (node, neighbor) )
                if ( 
                    transitions.check_if_state_has_pair_transitions( neighbor_state )
                    and transitions.check_if_receiver_available( neighbor_state, new_state )
                ):
                    watched.add( (neighbor, node) )

        watched.update(to_add_transitions)

    def _get_watched(self, network, pair_initiators, self_transitions ):
        ''' TODO: '''
        watched     = set()
        transitions = self.model.get_transitions()
        nodes = set([x for x,y in network.graph.nodes(data=True) if y['state'] in self_transitions])
        for node in nodes:
            watched.add( node )

        nodes = set([x for x,y in network.graph.nodes(data=True) if y['state'] in pair_initiators])
        for node in nodes:
            node_state = network.get_node_with_attr(node)['state']

            # Check neighbors for self transitions
            for neighbor in network.neighbors( node ):
                neighbor_state = network.get_node_with_attr(neighbor)['state']
                if transitions.check_if_receiver_available( node_state, neighbor_state ):
                    watched.add((node, neighbor))
        
        return watched


    ################################################################################################
    #                                   Transitions                                                #
    #                                                                                              #
    #                       Functions for dealing with transitions.                                #
    #                                                                                              #
    ################################################################################################

    def _get_pair_and_self_transitions(self):
        ''' Get pair transitions and self transitions of the model. '''
        transitions = self.model.get_transitions()
        #### TODO: 1 and 2 should probably be done outside the loop, only need to save them once
        return [
            # 1 Make list with transitions of two (i.e. IS => II)
            transitions.get_all_pair_initiators(),
            # 2 Make list with single transitions (i.e. I => R)
            transitions.get_all_self_transitions()
        ]

    def _do_pair_transition(self, node, state, neighbor, network, change_nodes):
        ''' Perform a single pair transition. '''
        transitions = self.model.get_transitions()
        # TODO: if there is already a change for this neighbor, randomly pick if we should keep it.
        neighbor_state = network.get_node_with_attr(neighbor)['state']

        # If there is then, call the function
        new_state, new_neighbor_state = transitions.call_pair_transition_function(
            node, state,
            neighbor, neighbor_state,
            network
        )
        # If there is a change in states, then add it to changes
        if neighbor_state != new_neighbor_state:
            change_nodes[neighbor] = new_neighbor_state
        if state != new_state:
            change_nodes[node] = new_state

    def _do_self_transition(self, node, state, network, change_nodes):
        ''' Do a node's self transition. '''
        # TODO: if there is already a change for this state, randomly pick if we should keep it.

        #   If there is, call the function
        new_state = self.model.get_transitions().call_self_transition_function(node, state, network)
        #   If there is a change in state, then add to list made in 8 
        if new_state != state:
            change_nodes[node] = new_state


    ################################################################################################
    #                                   Processing                                                 #
    #                                                                                              #
    #                   Functions for dealing with processing/processors.                          #
    #                                                                                              #
    ################################################################################################

    def _process_data(self, network, watched_nodes, step):
        self.data_processor.process({
            'model'        : self.model,
            'network'      : network,
            'watched_nodes': watched_nodes,
            'step'         : step,
        })

    def _start_set_processing(self, network_class, size, strategy, param_values):
        self._set_processing(True, network_class, size, strategy, param_values)

    def _end_set_processing(self, network_class, size, strategy, param_values):
        self._set_processing(False, network_class, size, strategy, param_values)

    def _set_processing(self, start, network_class, size, strategy, param_values):
        data = {
            'model':         self.model,
            'network_class': network_class,
            'size':          size,
            'strategy':      strategy,
            'param_values':  param_values
        }
        if start:
            self.data_processor.start_set_processing(data)
        else:
            self.data_processor.end_set_processing(data)

    ## TODO: Maybe these dont need all these values
    def _start_step_processing(self, step, network, size, strategy, param_values):
        self._step_processing(True, step, network, size, strategy, param_values)

    def _end_step_processing(self, step, network, size, strategy, param_values):
        self._step_processing(False, step, network, size, strategy, param_values)

    def _step_processing(self, start, step, network, size, strategy, param_values):
        data = {
            'model'       : self.model,
            'network'     : network,
            'size'        : size,
            'strategy'    : strategy,
            'param_values': param_values,
            'step'        : step,
        }
        if start:
            self.data_processor.start_step_processing(data)
        else:
            self.data_processor.end_step_processing(data)