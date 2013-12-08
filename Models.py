'''
This file contains class descriptions for all kinds of objects
used in the simulation to mimic the real world: stops, roads, passengers and etc.
'''
import random




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
        self.qOfBuses = []
        self.passengers = []
        self.reachableStops = []
        self.missedPassengers = 0
    
    
    def addReachableStops(self, reachableStops):
        ''' Method that adds new stops to the set of reachable stops'''
        for stop in reachableStops:
            if not (stop in self.reachableStops) and not (self.stopID == stop):
                self.reachableStops.append(stop)


    def addBus(self, bus):
        ''' Method that adds a bus to the stop's queue'''
        self.qOfBuses.append(bus)
                
    
class Route:
    ''' A class representing a particular route in the bus network'''
    def __init__(self, stopSequence, routeID, capacity):
        self.routeID = routeID
        self.stopSequence = stopSequence
        self.capacity = capacity
        self.buses = []
        self.missedPassengers = 0


    def addBus(self, bus):
        ''' This method adds the given bus to the route'''
        self.buses.append(bus)
        
        
    def getNewBus(self):
        ''' This method creates a new bus for the route'''
        location = self.stopSequence[len(self.buses) % len(self.stopSequence)]
        return Bus(self.routeID, len(self.buses), self.capacity, location)
        

    def getNextStop(self, currentStopID):
        ''' This method gets the next stop's ID when current stop's ID is given'''
        return self.stopSequence[(self.stopSequence.index(currentStopID) + 1) % len(self.stopSequence)]

        
class Network:
    ''' A class representing the entire bus network'''
    def __init__(self):
        self.routes = {}
        self.stops = {}
        self.roads = {}
        random.seed(0)
        
    
    def addRoad(self, stop1, stop2, throughput):
        ''' This method adds a road with specified throughput between two stops,
        stop1 and stop2'''
        if not (stop1 in self.roads.keys()):
            self.roads[stop1] = {}
        self.roads[stop1][stop2] = throughput


    def addRoute(self, routeID, stopIDs, busCount, capacity):
        ''' This method adds a route with its buses and stops to the network'''
        # Adding new stops to the network:
        for i in stopIDs:
            if not (i in self.stops.keys()):
                self.stops[i] = Stop(i)
            self.stops[i].addReachableStops(stopIDs)
        # Adding new route:
        self.routes[routeID] = Route(stopIDs, routeID, capacity)
        # Adding buses to the route:
        for i in range(0, busCount):
            bus = self.routes[routeID].getNewBus()
            self.routes[routeID].addBus(bus)
            self.stops[bus.location].addBus(bus)

    
    def addPassenger(self, time, outputEvent):
        ''' This method adds a passenger to the bus network'''
        originID = self.stops.keys()[random.randint(0, len(self.stops)-1)]
        destID = random.choice(self.stops[originID].reachableStops)
        self.stops[originID].passengers.append(Passenger(destID))
        if outputEvent:
            print 'A new passenger enters at stop {0} with destination {1} at time {2}'.format(originID, destID, time)

    
    def getThroughput(self, bus):
        ''' This method gets the throughput of the road segment
            that the bus is currently on '''
        originStopID = bus.location
        destinationStopID = self.routes[bus.routeID].getNextStop(originStopID)
        return self.roads[originStopID][destinationStopID]
        
    def getPaxRTB(self):
        ''' This method gets all passengers that are in a stop, the bus
        at the front of the bus queue suits them and is not full'''
        paxRTB = []
        for stop in self.stops.values():
            for pax in stop.passengers:
                if stop.qOfBuses:
                    firstBus = stop.qOfBuses[0]
                    if (pax.destStopID in self.routes[firstBus.routeID].stopSequence) and (len(firstBus.passengers) < firstBus.capacity):
                        paxRTB.append((pax, firstBus))
        return paxRTB


    def getPaxRTD(self):
        ''' This method gets all passengers that are in a bus, but would like
        to get off the bus. Also, the bus is at a bus stop'''
        paxRTD = []
        for stop in self.stops.values():
            for bus in stop.qOfBuses:
                for pax in bus.passengers:
                    if (pax.destStopID == bus.location) and (bus.status == 'Queueing'):
                        paxRTD.append((pax, bus))
        return paxRTD


    def getBusesRTD(self):
        ''' This method gets all of the buses that are ready to depart from
        the stop that they are located'''
        busesRTD = []
        for stop in self.stops.values():
            for bus in stop.qOfBuses:
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
        ''' This method gets all of the buses that are ready to arrive at
        the stop that they are located at'''
        busesRTA = []
        for route in self.routes.values():
            for bus in route.buses:
                if bus.status == 'Moving':
                    busesRTA.append((bus, route))
        return busesRTA

    
    def boardPassenger(self, time, outputEvent):
        ''' This method adds a random passenger to the bus
        that he wishes to board'''
        (rand_pax, rand_bus) = random.choice(self.getPaxRTB())
        rand_bus.passengers.append(rand_pax)
        self.stops[rand_bus.location].passengers.pop(self.stops[rand_bus.location].passengers.index(rand_pax))
        if outputEvent:
            print 'Passenger boards bus {0} at stop {1} with destination {2} at time {3}'.format(str(rand_bus.routeID) + '.' + str(rand_bus.busNumber), rand_bus.location, rand_pax.destStopID, time)
        
        
    def disembarkPassenger(self, time, outputEvent):
        ''' This method disembarks a random passenger from the bus that he's in'''
        (rand_pax, rand_bus) = random.choice(self.getPaxRTD())
        rand_bus.passengers.pop(rand_bus.passengers.index(rand_pax))
        if outputEvent:
            print 'Passenger disembarks bus {0} at stop {1} at time {2}'.format(str(rand_bus.routeID) + '.' + str(rand_bus.busNumber), rand_bus.location, time)
        

    def departBus(self, time, outputEvent):
        ''' This method departs a random bus that's ready to depart'''
        (rand_bus, rand_stop) = random.choice(self.getBusesRTD())
        rand_stop.qOfBuses.pop(rand_stop.qOfBuses.index(rand_bus))
        rand_bus.status = 'Moving'
        self.calculateMissedPassengers(rand_bus, rand_stop)
        if outputEvent:
            print 'Bus {0} leaves stop {1} at time {2}'.format(str(rand_bus.routeID) + '.' + str(rand_bus.busNumber), rand_bus.location, time)


    def arriveBus(self, time, outputEvent):
        ''' This method makes a random bus that's ready to arrive to arrive'''
        (rand_bus, rand_route) = random.choice(self.getBusesRTA())
        next_stop_id = rand_route.getNextStop(rand_bus.location)
        rand_bus.location = next_stop_id
        rand_bus.status = 'Queueing'
        self.stops[next_stop_id].qOfBuses.append(rand_bus)
        if outputEvent:
            print 'Bus {0} arrives at stop {1} at time {2}'.format(str(rand_bus.routeID) + '.' + str(rand_bus.busNumber), next_stop_id, time)
            
            
    def calculateMissedPassengers(self, bus, stop):
        ''' This method calculates and adds the missed passengers to the stop and route'''
        missed = 0
        stopSequence = self.routes[bus.routeID].stopSequence
        for pax in stop.passengers:
            if (pax.destStopID in stopSequence):
                missed += 1
        stop.missedPassengers += missed
        self.routes[bus.routeID].missedPassengers += missed
        