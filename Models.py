'''
This file contains class descriptions for all kinds of objects
used in the simulation to mimic the real world: stops, roads, passengers and etc.
'''
class Passenger:
    ''' A class representing a passenger in bus network'''
    def __init__(self, destStopID):
        self.destStopID = destStopID
        
        
class Bus:
    ''' A class representing a bus going on some route in the bus network'''
    def __init__(self, routeID, busNumber, capacity, status, location):
        self.routeID = routeID
        self.busNumber = busNumber
        self.capacity = capacity
        self.status = 'Queueing'
        self.location = location
        self.passengers = []
        
        
class Stop:
    ''' A class representing a bus stop in the bus network'''
    def __init__(self, stopID):
        self.stopID = stopID
        self.qOfBusses = []
        self.passengers = []
    
    
class Route:
    ''' A class representing a particular route in the bus network'''
    def __init__(self, stopSequence, routeID, capacity):
        self.routeID = routeID
        self.stopSequence = stopSequence
        self.capacity = capacity
        self.busses = []


class Roads:
    ''' A class representing roads with their throughput in the bus network'''
    def __init(self):
        self.roads = {}
        
        
class Network:
    ''' A class representing the entire bus network'''
    def __init__(self):
        self.routes = {}
        self.stops = {}
        self.roads = Roads
    
    
    def addRoad(self, stop1, stop2, throughput):
        ''' This method adds a road with specified throughput between two stops,
        stop1 and stop2'''
        if not (stop1 in self.roads.keys()):
            self.roads[stop1] = {}
        self.roads[stop1][stop2] = throughput


    def addRoute(self, routeID, stopIDs, busCount, capacity):
        ''' This method adds a route with its busses and stops to the network'''
        self.routes[routeID] = Route(stopIDs.split(' '), routeID, capacity)
        # Adding busses to the route:
        for i in range(0, busCount):
            self.routes[routeID].addNewBus()
