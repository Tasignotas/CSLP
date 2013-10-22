'''
This file contains class descriptions for all kinds of objects
used in the simulation to mimic the real world: stops, roads, passengers and etc.
'''


from random import randint, choice


class Passenger:
    ''' A class representing a passenger in bus network'''
    def __init__(self, destStopID):
        self.destStopID = destStopID
        
        
class Bus:
    ''' A class representing a bus going on some route in the bus network'''
    def __init__(self, routeID, busNumber, capacity, location):
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
        self.reachableStops = {}
    
    
    def addReachableStops(self, reachableStops):
        ''' Method that adds new stops to the set of reachable stops'''
        for stop in reachableStops:
            if not (stop in self.reachableStops) and not (self.stopID == stop):
                self.reachableStops.add(stop)
                
    
class Route:
    ''' A class representing a particular route in the bus network'''
    def __init__(self, stopSequence, routeID, capacity):
        self.routeID = routeID
        self.stopSequence = stopSequence
        self.capacity = capacity
        self.busses = []

    def addBus(self):
        ''' This method adds a new bus to the route'''
        location = len(self.busses) % len(self.stopSequence)
        self.busses.append(Bus(self.routeID, len(self.busses), self.capacity,
                           location))
        
        
class Network:
    ''' A class representing the entire bus network'''
    def __init__(self):
        self.routes = {}
        self.stops = {}
        self.roads = {}
    
    
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
            self.routes[routeID].addBus()
        # Adding new stops to the network:
        for i in stopIDs.split(' '):
            if not (i in self.stops.keys()):
                self.stops[i] = Stop(i)
            self.stops[i].addReachableStops(stopIDs.split(' '))
    
    
    def addPassenger(self):
        ''' This method adds a passenger to the bus network'''
        originID = self.stops.keys()[randint(0, len(self.stops)-1)]
        destID = choice(self.stops[originID].reachableStops())
        self.stops[originID].passengers.append(Passenger(destID))

        
    def getPaxRTB(self):
        ''' This method gets all passengers that are in a stop, the bus
        at the front of the bus queue suits them and is not full'''
        paxRTB = []
        for stop in self.stops:
            for pax in self.stops[stop].passengers:
                firstBus = self.stops[stop].qOfBusses[0]
                if firstBus:
                    if (pax.destStopID in self.routes[firstBus.routeID].stopSequence) and (len(firstBus.passengers) < firstBus.capacity):
                        paxRTB.append((pax, bus))
        return paxRTB


    def getPaxRTD(self):
        ''' This method gets all passengers that are in a bus, but would like
        to get off the bus. Also, the bus is at a bus stop'''
        paxRTD = []
        for stop in self.stops:
            for bus in stop.qOfBusses:
                for pax in bus.passengers:
                    if (pax.destStopID == bus.location) and (bus.status == 'Queueing'):
                        paxRTD.append((pax, bus))


    def getBusesRTD(self):
        ''' This method gets all of the busses that are ready to depart from
        the stop that they are located'''
        busesRTD = []
        for stop in self.stops:
            for bus in stop.qOfBusses:
                noneToDisembark = True
                noneToBoard = True
                # Checking if there is any passenger that wants to get onboard:
                for pax in stop.passengers:
                    if (pax.destStopID in self.routes[bus.routeID].stopSequence) and (len(bus.passengers) < bus.capacity):
                        noneToBoard = False
                # Checking if there is any passenger that wants to disembark:
                for pax in bus.passengers:
                    if (pax.destStopID == bus.location) and (bus.status == 'Queueing'):
                        noneToDisembark = False
                if noneToBoard and noneToDisembark:
                    busesRTD.append((bus, stop))
        return busesRTD


    def getBusesRTA(self):
        ''' This method gets all of the busses that are ready to arrive at
        the stop that they are located at'''
        busesRTA = []
        for route in self.routes:
            for bus in route.busses:
                if bus.status == 'Moving':
                    busesRTA.append((bus, route))
        return busesRTA

    
    def boardPassenger(self):
        ''' This method adds a random passenger to the bus
        that he wishes to board'''
        (rand_pax, rand_bus) = choice(self.getPaxRTB())
        rand_bus.passengers.append(rand_pax)
        self.stops[rand_bus.location].passengers.pop(self.stops[rand_bus.location].passengers.index(rand_pax))