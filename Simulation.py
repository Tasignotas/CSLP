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
import itertools
import cProfile


class Simulation:
    ''' A class that controls the entire simulation and performs events using
    the constructed bus network'''
    def __init__(self):
        self.Network = Models.Network()
        self.params = {'control' : {},
                       'general' : {},
                       'roads' : {},
                       'routes' : {}
                       }
        self.params['control']['ignoreWarnings'] = False
        self.params['control']['optimiseParameters'] = False
        self.params['control']['experimentation'] = False
        self.params['general']['board'] = []
        self.params['general']['disembarks'] = []
        self.params['general']['departs'] = []
        self.params['general']['new passengers'] = []


    def __eq__(self, another):
        return (self.Network == another.Network) and (self.params == another.params)
    
    
    def addRoad(self, stop1, stop2, throughput):
        ''' This method adds a road with specified throughput between stop1 and stop2'''
        if not ((stop1, stop2) in self.params['roads']):
            self.params['roads'][(stop1, stop2)] = throughput
        elif throughput != self.params['roads'][(stop1, stop2)]:
            raise Exception('Two different throughputs are specified for the road {0} -> {1}').format(stop1, stop2)
        
        
    def addRoute(self, routeID, stopIDs, busCount, capacity):
        ''' This method adds a new route to the network and stores the experimentation values'''
        busCount.sort()
        capacity.sort()
        self.Network.addRoute(routeID, stopIDs, busCount[0], capacity[0])
        self.params['routes'][routeID] = {'routeID' : [routeID],
                                          'buses' : busCount,
                                          'capacity' : capacity
                                          }


    def generateRouteSets(self):
        ''' This method generates all possible route experimental value combinations'''
        route_product = []
        for route in self.params['routes'].values():
            product = [x for x in apply(itertools.product, route.values())]
            route_product.append([dict(zip(route.keys(), p)) for p in product])
        return [list(set) for set in apply(itertools.product, route_product)]
        

    def generateRoadSets(self):
        ''' This method generates all possible route throughput rate combinations'''
        product = [x for x in apply(itertools.product, self.params['roads'].values())]
        return [dict(zip(self.params['roads'].keys(), p)) for p in product]
    
    
    def generateGeneralParamSets(self):
        ''' This method generates all possible general simulation parameter combinations'''
        values = [value if hasattr(value, '__iter__') else [value] for value in self.params['general'].values()]
        product = [x for x in apply(itertools.product, values)]
        return [dict(zip(self.params['general'].keys(), p)) for p in product]
    
        
    def printExperimentationParameters(self, generalParamSet, roadSet, routeSet): 
        ''' Method that prints all experimentation values of the given parameter dicts''' 
        for key in generalParamSet:
            if len(self.params['general'][key]) > 1:
                print key + ' ' + str(generalParamSet[key])
        for (stop1, stop2) in roadSet:
            if len(self.params['roads'][(stop1, stop2)]) > 1:
                print 'road {0} {1} {2}'.format(stop1, stop2, roadSet[(stop1, stop2)])
        for route in routeSet:
            outStr = ''
            for key in self.params['routes'].values()[0]:
                if len(self.params['routes'][route['routeID']][key]) > 1:
                    outStr += ' ' + key + ' ' + str(route[key])
            if outStr != '':
                print 'route ' + str(route['routeID']) + outStr
        

    def executeExperimentation(self, generalParamSets, roadSets, routeSets):
        ''' This method performs experimentation over all parameter values'''
        initialNetwork = deepcopy(self.Network)
        for generalParamSet in generalParamSets:
            for roadSet in roadSets:
                for routeSet in routeSets:
                    self.Network.changeGeneralParams(generalParamSet)
                    self.Network.changeRoadParams(roadSet)
                    self.Network.changeRouteParams(routeSet)
                    self.printExperimentationParameters(generalParamSet, roadSet, routeSet)
                    self.executeSimulationLoop(outputEvents=False)
                    self.printStatistics()
                    self.Network = deepcopy(initialNetwork)
                            
                                          
    def executeOptimisation(self, generalParamSets, roadSets, routeSets):
        ''' This method performs parameter optimisation'''
        minCost = None
        initialNetwork = deepcopy(self.Network)
        for generalParamSet in generalParamSets:
            for roadSet in roadSets:
                for routeSet in routeSets:
                    if minCost != 0:
                        self.Network.changeGeneralParams(generalParamSet)
                        self.Network.changeRoadParams(roadSet)
                        self.Network.changeRouteParams(routeSet)
                        self.executeSimulationLoop(outputEvents=False)
                        # Getting the number of missed passengers:
                        totalPassengers = sum([stop.missedPassengers for stop in self.Network.stops.values()])
                        generalParamSum = sum(generalParamSet.values())
                        roadParamSum = sum(roadSet.values())
                        routeParamSum = sum(sum([route.values() for route in routeSet], []))
                        cost = totalPassengers * (generalParamSum + roadParamSum + routeParamSum)
                        if not (minCost) or (minCost > cost):
                            minCost = cost
                            maxGeneralParamSet = generalParamSet
                            maxRoadSet = roadSet
                            maxRouteSet = routeSet
                        self.Network = deepcopy(initialNetwork)
        print 'Bus network is optimized with setting the parameters as:'
        self.printExperimentationParameters(maxGeneralParamSet, maxRoadSet, maxRouteSet)
    
    
    def printStatistics(self):
        ''' Method that prints the statistics of the most recent run of the simulation'''
        # Missed passengers:
        total = 0
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
        totalTime = 0.0
        totalBuses = 0
        for stop in self.Network.stops.values():
            print 'average queueing at stop {0} {1}'.format(stop.stopID, stop.totalQueueingTime/stop.numberOfBusesQueued)
            totalTime += stop.totalQueueingTime
            totalBuses += stop.numberOfBusesQueued
        print 'average queueing at all stops {0}'.format(totalTime/totalBuses)
        # I am not sure if there should be an empty line printed after the statistics.
        # It looks nicer, but if it messes up your output parser then just comment it out.
        print ''
        
    

    def executeSimulation(self):
        ''' This method chooses the right kind of simulation type to be run '''
        generalParamSets = self.generateGeneralParamSets()
        roadSets = self.generateRoadSets()
        routeSets = self.generateRouteSets()
        if self.params['control']['optimiseParameters']:
            self.executeOptimisation(generalParamSets, roadSets, routeSets)
        elif self.params['control']['experimentation']:
            self.executeExperimentation(generalParamSets, roadSets, routeSets)
        else:
            self.Network.changeGeneralParams(generalParamSets[0])
            self.Network.changeRoadParams(roadSets[0])
            self.Network.changeRouteParams(routeSets[0])
            self.executeSimulationLoop()
            self.printStatistics()
            

    def executeSimulationLoop(self, outputEvents=True):
        ''' This method implements the main simulation loop '''
        currentTime = 0
        while currentTime <= self.params['control']['stopTime']:
            # Getting all of the events that could occur:
            rates = self.getEventRates()
            totalRate = (self.Network.params['new passengers'] + rates['paxRTBRate'] +
                         rates['paxRTDRate'] + rates['busesRTARate'] +
                         rates['busesRTDRate'])
            delay = -(1.0/totalRate) * log10(uniform(0.0, 1.0))
            self.executeNextEvent(totalRate, rates, currentTime, outputEvents)
            currentTime += delay
        self.Network.finishTakingStatistics(self.params['control']['stopTime'])


    def getEventRates(self):
        ''' This method gets rates needed for choosing the event to execute'''
        rates = {}
        # Passengers ready to board rate:
        rates['paxRTBRate'] = len(self.Network.getPaxRTB()) * self.Network.params['board']
        # Passengers ready to disembark rate:
        rates['paxRTDRate'] = len(self.Network.getPaxRTD()) * self.Network.params['disembarks']
        # Buses ready to depart rate:
        rates['busesRTDRate'] = len(self.Network.getBusesRTD()) * self.Network.params['departs']
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
            
    
    def validateSimulation(self):
        ''' This method checks if simulation's bus network and other parameters are valid or not '''
        warnings.simplefilter('always' if self.params['control']['ignoreWarnings'] else 'error')
        # Checking if all of the rates that must be specified are there:
        try:
            if self.params['general']['board'] == []:
                raise Exception('No board rate has been specified')
            if self.params['general']['disembarks'] == []:
                raise Exception('No disembarks rate has been specified')
            if self.params['general']['departs'] == []:
                raise Exception('No departs rate has been specified')
            if self.params['general']['new passengers'] == []:
                raise Exception('No new passenger rate has been specified')
            if not('stopTime' in self.params['control']):
                raise Exception('No stop time has been specified')
        except KeyError:
            raise Exception('Some of the necessary rates of the network are not specified')
        # Checking if all routes have roads defined:
        for route in self.Network.routes.values():
            for stop1 in route.stopSequence:
                stop2 = route.getNextStop(stop1)
                try:
                    self.params['roads'][(stop1, stop2)]
                except KeyError:
                    raise Exception('The road between stops {0} and {1} is undefined'.format(stop1, stop2))
        # Checking if all roads are in some route:
        for (depStop, destStop) in self.params['roads']:
            roadUsed = False
            for route in self.Network.routes.values():
                for stop1 in route.stopSequence:
                    if depStop == stop1 and destStop == route.getNextStop(stop1):
                        roadUsed = True
            if not roadUsed:
                warnings.warn('Road between stops {0} and {1} is specified but not used'.format(depStop, destStop))
        # Checking if the simulation has experimentation parameters if we need to optimise it:
        if self.params['control']['optimiseParameters'] and not (self.params['control']['experimentation']):
            raise Exception('There are no experimentation values given although optimisation flag is set to True')



if __name__ == '__main__':
    simulation = Simulation()
    fileName = raw_input('Please enter the name of the input file: ')
    Parser.Parser.parseFile(fileName, simulation)
    simulation.validateSimulation()
    cProfile.run('simulation.executeSimulation()')
    #simulation.executeSimulation()