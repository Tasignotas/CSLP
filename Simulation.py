'''
This class will perform events on the constructed bus network: it will simulate
passenger and bus movement/queueing in the network
'''
import Parser
import Models
import warnings
from random import uniform
from math import log10
from copy import deepcopy


class Simulation:
    ''' A class that controls the entire simulation and performs events using
    the constructed bus network'''
    def __init__(self):
        self.ignoreWarnings = False
        self.optimiseParameters = False
        
        
    def execute_experimentation(self):
        ''' This method performs experimentation over all parameter values'''
        initialNetwork = deepcopy(self.Network)
        for boardRatio in self.boardRatioList:
            self.boardRatio = boardRatio
            if len(self.boardRatioList) != 1:
                print 'board {0}'.format(boardRatio)
            for disembarksRatio in self.disembarksRatioList:
                self.disembarksRatio = disembarksRatio
                if len(self.disembarksRatioList) != 1:
                    print 'disembarks {0}'.format(disembarksRatio)
                for depRatio in self.depRatioList:
                    self.depRatio = depRatio
                    if len(self.depRatioList) != 1:
                        print 'departs {0}'.format(depRatio)
                    for newPassRatio in self.newPassRatioList:
                        self.newPassRatio = newPassRatio
                        if len(self.newPassRatioList) != 1:
                            print 'new passengers {0}'.format(newPassRatio)
                        self.execute_simulation_loop()
                        self.print_statistics()
                        self.Network = deepcopy(initialNetwork)
                            
    
    def print_statistics(self):
        ''' Method that prints the statistics of the most recent run of the simulation'''
        print 'Statistics:'
        

    def execute_simulation(self):
        ''' This method chooses the right kind of simulation type to be run '''
        if self.optimiseParameters:
            self.execute_optimisation()
        elif (len(self.boardRatioList) * len(simulation.disembarksRatioList) * len(simulation.depRatioList) *
              len(simulation.newPassRatioList)) > 1:
            self.execute_experimentation()
        else:
            self.execute_simulation_loop()
            self.print_statistics()
            

    def execute_simulation_loop(self, outputEvents=True):
        ''' This method implements the main simulation loop '''
        currentTime = 0
        while currentTime <= self.stopTime:
            # Getting all of the events that could occur:
            rates = self.getEventRates()
            totalRate = (self.newPassRatio + rates['paxRTBRate'] +
                         rates['paxRTDRate'] + rates['busesRTARate'] +
                         rates['busesRTDRate'])
            delay = -(1.0/totalRate) * log10(uniform(0.0, 1.0))
            self.executeNextEvent(totalRate, rates, currentTime, outputEvents)
            currentTime += delay


    def getEventRates(self):
        ''' This method gets rates needed for choosing the event to execute'''
        rates = {}
        # Passengers ready to board rate:
        rates['paxRTBRate'] = len(self.Network.getPaxRTB()) * self.boardRatio
        # Passengers ready to disembark rate:
        rates['paxRTDRate'] = len(self.Network.getPaxRTD()) * self.disembarksRatio
        # Buses ready to depart rate:
        rates['busesRTDRate'] = len(self.Network.getBusesRTD()) * self.depRatio
        # Buses ready to arrive rate:
        rates['busesRTARate'] = sum([self.Network.getThroughput(bus) for (bus, route) in self.Network.getBusesRTA()])
        print rates
        return rates


    def executeNextEvent(self, totalRate, rates, time, outputEvents):
        ''' This method chooses and executes an event, based on event rates'''
        choice = uniform(0, totalRate)
        if choice < rates['paxRTBRate']:
            self.Network.boardPassenger(time, outputEvents)
        elif choice < (rates['paxRTBRate'] + rates['paxRTDRate']):
            self.Network.disembarkPassenger(time, outputEvents)
        elif choice < (rates['paxRTBRate'] + rates['paxRTDRate'] +
                       rates['busesRTDRate']):
            self.Network.departBus(time, outputEvents)
        elif choice < (rates['paxRTBRate'] + rates['paxRTDRate'] +
                       rates['busesRTDRate'] + rates['busesRTARate']):
            self.Network.arriveBus(time, outputEvents)
        else:
            self.Network.addPassenger(time, outputEvents)
            
    
    def validateAndLoadNetwork(self, network):
        ''' This method checks if simulation's bus network is valid or not '''
        warnings.simplefilter('always' if self.ignoreWarnings else 'error')
        # Checking if all routes have roads defined and they are positive:
        for route in network.routes.values():
            for stop1 in route.stopSequence:
                stop2 = route.getNextStop(stop1)
                try:
                    if network.roads[stop1][stop2] <= 0:
                        raise Exception('The road throughput between stops {0} and {1} is <= 0'.format(stop1, stop2))
                except KeyError:
                    raise Exception('The road between stops {0} and {1} is undefined'.format(stop1, stop2))
        # Checking if all roads are in some route:
        for depStop in network.roads:
            for destStop in network.roads[depStop]:
                roadUsed = False
                for route in network.routes.values():
                    for stop1 in route.stopSequence:
                        if depStop == stop1 and destStop == route.getNextStop(stop1):
                            roadUsed = True
                if not roadUsed:
                    warnings.warn('Road between stops {0} and {1} is specified but not used'.format(depStop, destStop))
        # If no errors were raised, we load the network for the simulation:
        self.Network = network


if __name__ == '__main__':
    simulation = Simulation()
    fileName = raw_input('Please enter the name of the input file: ')
    network = Parser.Parser.parseFile(fileName, simulation)
    simulation.validateAndLoadNetwork(network)
    simulation.execute_simulation()