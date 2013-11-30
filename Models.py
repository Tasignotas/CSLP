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
        self.reachableStops = []
    
    
    def addReachableStops(self, reachableStops):
        ''' Method that adds new stops to the set of reachable stops'''
        for stop in reachableStops:
            if not (stop in self.reachableStops) and not (self.stopID == stop):
                self.reachableStops.append(stop)


    def addBus(self, bus):
        ''' Method that adds a bus to the stop's queue'''
        self.qOfBusses.append(bus)
                
    
class Route:
    ''' A class representing a particular route in the bus network'''
    def __init__(self, stopSequence, routeID, capacity):
        self.routeID = routeID
        self.stopSequence = stopSequence
        self.capacity = capacity
        self.busses = []


    def addBus(self, bus):
        ''' This method adds the given bus to the route'''
        self.busses.append(bus)
        
        
    def getNewBus(self):
        ''' This method creates a new bus for the route'''
        location = self.stopSequence[len(self.busses) % len(self.stopSequence)]
        return Bus(self.routeID, len(self.busses), self.capacity, location)
        

    def getNextStop(self, currentStopID):
        ''' This method gets the next stop's ID when current stop's ID is given'''
        return self.stopSequence[(self.stopSequence.index(currentStopID) + 1) % len(self.stopSequence)]

        
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
        # Adding new stops to the network:
        for i in stopIDs:
            if not (i in self.stops.keys()):
                self.stops[i] = Stop(i)
            self.stops[i].addReachableStops(stopIDs)
        # Adding new route:
        self.routes[routeID] = Route(stopIDs, routeID, capacity)
        # Adding busses to the route:
        for i in range(0, busCount):
            bus = self.routes[routeID].getNewBus()
            self.routes[routeID].addBus(bus)
            self.stops[bus.location].addBus(bus)

    
    def addPassenger(self):
        ''' This method adds a passenger to the bus network'''
        originID = self.stops.keys()[randint(0, len(self.stops)-1)]
        destID = choice(self.stops[originID].reachableStops)
        self.stops[originID].passengers.append(Passenger(destID))
        print 'A new passenger enters at stop {0} with destination {1} at time'.format(originID, destID)

        
    def getPaxRTB(self):
        ''' This method gets all passengers that are in a stop, the bus
        at the front of the bus queue suits them and is not full'''
        paxRTB = []
        for stop in self.stops.values():
            for pax in stop.passengers:
                if stop.qOfBusses:
                    firstBus = stop.qOfBusses[0]
                    print pax.destStopID
                    print self.routes[firstBus.routeID].stopSequence
                    if (pax.destStopID in self.routes[firstBus.routeID].stopSequence) and (len(firstBus.passengers) < firstBus.capacity):
                        paxRTB.append((pax, bus))
        return paxRTB


    def getPaxRTD(self):
        ''' This method gets all passengers that are in a bus, but would like
        to get off the bus. Also, the bus is at a bus stop'''
        paxRTD = []
        for stop in self.stops.values():
            for bus in stop.qOfBusses:
                for pax in bus.passengers:
                    if (pax.destStopID == bus.location) and (bus.status == 'Queueing'):
                        paxRTD.append((pax, bus))
        return paxRTD


    def getBusesRTD(self):
        ''' This method gets all of the busses that are ready to depart from
        the stop that they are located'''
        busesRTD = []
        for stop in self.stops.values():
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
        print 'Passenger boards bus {0} at stop {1} with destination {2} at time'.format((rand_bus.routeID + '' + rand_bus.busNumber), rand_bus.location, rand_pax.destStopID)
        
        
    def disembarkPassenger(self):
        ''' This method disembarks a random passenger from the bus that he's in'''
        (rand_pax, rand_bus) = choice(self.getPaxRTD())
        rand_bus.passengers.pop(rand_bus.passengers.index(rand_pax))
        print 'Passenger disembarks bus {0} at stop {1} at time'.format((rand_bus.routeID + '' + rand_bus.busNumber), rand_bus.location)
        

    def departBus(self):
        ''' This method departs a random bus that's ready to depart'''
        (rand_bus, rand_stop) = choice(self.getBusesRTD())
        rand_stop.qOfBuses.pop(rand_stop.qOfBuses.index(rand_bus))
        rand_bus.status = 'Moving'
        print 'Bus {0} leaves stop {1} at time'.format((rand_bus.routeID + '' + rand_bus.busNumber), rand_bus.location)


    def arriveBus(self):
        ''' This method makes a random bus that's ready to arrive to arrive'''
        (rand_bus, rand_route) = choice(self.getBusesRTA())
        next_stop_id = rand_route.getNextStop(rand_bus.location)
        rand_bus.location = next_stop_id
        rand_bus.state = 'Queueing'
        self.stops[next_stop_id].qOfBuses.append(rand_bus)
        print 'Bus {0} arrives at stop {1} at time'.format((rand_bus.routeID + '' + rand_bus.busNumber), next_stop_id)