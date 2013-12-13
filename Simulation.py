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
import itertools, operator


class Simulation:
    ''' A class that controls the entire simulation and performs events using
    the constructed bus network'''
    def __init__(self):
        self.Network = None
        self.params = {'control' : {},
                       'general' : {},
                       'roads' : {},
                       'routes' : {}
                       }
        self.params['control']['ignoreWarnings'] = False
        self.params['control']['optimiseParameters'] = False
        self.params['control']['experimentation'] = False
        self.params['general']['boardRatioList'] = []
        self.params['general']['disembarksRatioList'] = []
        self.params['general']['depRatioList'] = []
        self.params['general']['newPassRatioList'] = []


    def __eq__(self, another):
        return (self.Network == another.Network) and (self.params == another.params)
    
    
    def addRoad(self, stop1, stop2, throughput):
        ''' This method adds a road with specified throughput between stop1 and stop2'''
        if not ((stop1, stop2) in self.params['roads']):
            self.params['roads'][(stop1, stop2)] = throughput
        elif throughput != self.params['roads'][(stop1, stop2)]:
            raise Exception('Two different throughputs are specified for the road {0} -> {1}').format(stop1, stop2)
        
    
    def generateRoadSets(self):
        ''' This method generates all possible route throughput rate combinations'''
        product = [x for x in apply(itertools.product, self.params['roads'].values())]
        return [dict(zip(self.params['roads'].keys(), p)) for p in product]
    
    
    def generateGeneralParamSets(self):
        ''' This method generates all possible general simulation parameter combinations'''
        values = [value if hasattr(value, '__iter__') else [value] for value in self.params['general'].values()]
        product = [x for x in apply(itertools.product, values)]
        return [dict(zip(self.params['general'].keys(), p)) for p in product]
    
        
    def execute_experimentation(self):
    def print_experimentation_parameters(self, generalParamSet, roadSet): 
        ''' Method that prints all experimentation values of the given parameter dicts''' 
        for key in generalParamSet:
            if len(self.params['general'][key]) > 1:
                print key + ' ' + str(generalParamSet[key])
        for (stop1, stop2) in roadSet:
            if len(self.params['roads'][(stop1, stop2)]) > 1:
                print 'road {0} {1} {2}'.format(stop1, stop2, roadSet[(stop1, stop2)])
        
        ''' This method performs experimentation over all parameter values'''
        initialNetwork = deepcopy(self.Network)
        for boardRatio in self.params['general']['boardRatioList']:
            self.params['general']['boardRatio'] = boardRatio
            if len(self.params['general']['boardRatioList']) != 1:
                print 'board {0}'.format(boardRatio)
            for disembarksRatio in self.params['general']['disembarksRatioList']:
                self.params['general']['disembarksRatio'] = disembarksRatio
                if len(self.params['general']['disembarksRatioList']) != 1:
                    print 'disembarks {0}'.format(disembarksRatio)
                for depRatio in self.params['general']['depRatioList']:
                    self.params['general']['depRatio'] = depRatio
                    if len(self.params['general']['depRatioList']) != 1:
                        print 'departs {0}'.format(depRatio)
                    for newPassRatio in self.params['general']['newPassRatioList']:
                        self.newPassRatio = newPassRatio
                        if len(self.params['general']['newPassRatioList']) != 1:
                            print 'new passengers {0}'.format(newPassRatio)
                        self.execute_simulation_loop()
                        self.print_statistics()
                        self.Network = deepcopy(initialNetwork)
                            
                            
    def execute_optimisation(self):
        ''' This method performs parameter optimisation'''
        minCost = None
        initialNetwork = deepcopy(self.Network)
        for boardRatio in self.params['general']['boardRatioList']:
            self.params['general']['boardRatio'] = boardRatio
            for disembarksRatio in self.params['general']['disembarksRatioList']:
                self.params['general']['disembarksRatio'] = disembarksRatio
                for depRatio in self.params['general']['depRatioList']:
                    self.params['general']['depRatio'] = depRatio
                    for newPassRatio in self.params['general']['newPassRatioList']:
                        self.params['general']['newPassRatio'] = newPassRatio
                        if minCost != 0:
                            self.execute_simulation_loop(outputEvents=False)
                            # Getting the number of missed passengers:
                            totalPassengers = 0
                            for stop in self.Network.stops.values():
                                totalPassengers += stop.missedPassengers
                            cost = totalPassengers * (self.params['general']['boardRatio'] +
                                                      self.params['general']['disembarksRatio'] +
                                                      self.params['general']['depRatio'] +
                                                      self.params['general']['newPassRatio'])
                            if not (minCost) or (minCost > cost):
                                minCost = cost
                                params = {'boardRatio' : self.params['general']['boardRatio'],
                                          'disembarksRatio' : self.params['general']['disembarksRatio'],
                                          'depRatio' : self.params['general']['depRatio'],
                                          'newPassRatio' : self.params['general']['newPassRatio']}
                            self.Network = deepcopy(initialNetwork)
        print 'Bus network is optimized with setting the parameters as:'
        if len(self.params['general']['boardRatioList']) > 1:
            print 'board: {0}'.format(params['boardRatio'])
        if len(self.params['general']['disembarksRatioList']) > 1:
            print 'disembarks: {0}'.format(params['disembarksRatio'])
        if len(self.params['general']['depRatioList']) > 1:
            print 'departs: {0}'.format(params['depRatio'])
        if len(self.params['general']['newPassRatioList']) > 1:
            print 'new passengers: {0}'.format(params['newPassRatio'])
    
    
    def print_statistics(self):
        ''' Method that prints the statistics of the most recent run of the simulation'''
        # Missed passengers:
        total = 0.0
        for stop in self.Network.stops.values():
            print 'number of missed passengers stop {0} {1}'.format(stop.stopID, stop.missedPassengers)
            total += stop.missedPassengers
        for route in self.Network.routes.values():
            print 'number of missed passengers route {0} {1}'.format(route.routeID, route.missedPassengers)
        print 'number of missed passengers {0}'.format(total)
        # Average number of passengers:
        total = 0.0
        for route in self.Network.routes.values():
            totalPerRoute = 0.0
            for bus in route.buses:
                print 'average passengers bus {0}.{1} {2}'.format(bus.routeID, bus.busNumber, bus.averagePassengersTravelling)
                totalPerRoute += bus.averagePassengersTravelling
            print 'average passengers route {0} {1}'.format(route.routeID, totalPerRoute/len(route.buses))
            total += totalPerRoute
        print 'average passengers {0}'.format(total/len(self.Network.routes))
        # Average time spent queueing:
        total = 0.0
        for stop in self.Network.stops.values():
            print 'average queueing at stop {0} {1}'.format(stop.stopID, stop.totalQueueingTime/stop.numberOfBusesQueued)
            total += stop.totalQueueingTime/stop.numberOfBusesQueued
        print 'average queueing at all stops {0}'.format(total/len(self.Network.stops))
        
    

    def execute_simulation(self):
        ''' This method chooses the right kind of simulation type to be run '''
        generalParamSets = self.generateGeneralParamSets()
        roadSets = self.generateRoadSets()
        if self.params['control']['optimiseParameters']:
            self.execute_optimisation(generalParamSets, roadSets)
        elif (len(generalParamSets) * len(roadSets)) > 1:
            self.execute_experimentation(generalParamSets, roadSets)
        else:
            self.Network.changeParams(generalParamSets[0])
            self.Network.roads = roadSets[0]
            self.execute_simulation_loop()
            self.print_statistics()
            

    def execute_simulation_loop(self, outputEvents=True):
        ''' This method implements the main simulation loop '''
        currentTime = 0
        while currentTime <= self.params['control']['stopTime']:
            # Getting all of the events that could occur:
            rates = self.getEventRates()
            totalRate = (self.Network.params['newPassRatio'] + rates['paxRTBRate'] +
                         rates['paxRTDRate'] + rates['busesRTARate'] +
                         rates['busesRTDRate'])
            delay = -(1.0/totalRate) * log10(uniform(0.0, 1.0))
            self.executeNextEvent(totalRate, rates, currentTime, outputEvents)
            currentTime += delay


    def getEventRates(self):
        ''' This method gets rates needed for choosing the event to execute'''
        rates = {}
        # Passengers ready to board rate:
        rates['paxRTBRate'] = len(self.Network.getPaxRTB()) * self.Network.params['boardRatio']
        # Passengers ready to disembark rate:
        rates['paxRTDRate'] = len(self.Network.getPaxRTD()) * self.Network.params['disembarksRatio']
        # Buses ready to depart rate:
        rates['busesRTDRate'] = len(self.Network.getBusesRTD()) * self.Network.params['depRatio']
        # Buses ready to arrive rate:
        rates['busesRTARate'] = sum([self.Network.getThroughput(bus) for (bus, route) in self.Network.getBusesRTA()])
        #print rates
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
        warnings.simplefilter('always' if self.params['control']['ignoreWarnings'] else 'error')
        # Checking if all of the rates that must be specified are there:
        try:
            if len(self.params['general']['boardRatioList']) == 0:
                raise Exception('No board rate has been specified')
            if len(self.params['general']['disembarksRatioList']) == 0:
                raise Exception('No disembarks rate has been specified')
            if len(self.params['general']['depRatioList']) == 0:
                raise Exception('No departs rate has been specified')
            if len(self.params['general']['newPassRatioList']) == 0:
                raise Exception('No new passenger rate has been specified')
            if not(self.params['control']['stopTime']):
                raise Exception('No stop time has been specified')
        except:
            raise Exception('Some of the necessary rates of the network are not specified')
        # Checking if all routes have roads defined:
        for route in network.routes.values():
            for stop1 in route.stopSequence:
                stop2 = route.getNextStop(stop1)
                try:
                    self.params['roads'][(stop1, stop2)]
                except KeyError:
                    raise Exception('The road between stops {0} and {1} is undefined'.format(stop1, stop2))
        # Checking if all roads are in some route:
        for (depStop, destStop) in self.params['roads']:
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