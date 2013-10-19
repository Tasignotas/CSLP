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
