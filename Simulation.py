'''
This class will perform events on the constructed bus network: it will simulate
passenger and bus movement/queueing in the network
'''
import Parser
from random import uniform
from math import log10

class Simulation:
    ''' A class that controls the entire simulation and performs events using
    the constructed bus network'''
    def __init__(self):
        self.ignoreWarnings = False
        self.optimiseParameters = False


    def execute_simulation_loop(self):
        ''' This method implements the main simulation loop '''
        currentTime = 0
        while currentTime <= self.stopTime:
            # Getting all of the events that could occur:
            rates = self.getEventRates()
            totalRate = (self.newPassRatio + rates[paxRTBRate] +
                         rates[paxRTDRate] + rates[busesRTARate] +
                         rates[busesRTLRate])
            delay = -(1.0/totalRate) * log10(uniform(0.0, 1.0))
            self.executeNextEvent(totalRate, rates)
            currentTime += delay


    def getEventRates(self):
        ''' This method gets rates needed for choosing the event to execute'''
        rates = {}
        # Passengers ready to board rate:
        rates[paxRTBRate] = len(self.Network.getPaxRTB()) * self.boardRatio
        # Passengers ready to disembark rate:
        rates[paxRTDRate] = len(self.Network.getPaxRTD()) * self.disembarksRatio
        # Buses ready to depart rate:
        rates[busesRTDRate] = len(self.Network.getBusesRTD()) * self.depRatio
        # Buses ready to arrive rate:
        rates[busesRTARate] = sum([self.Network.getThroughput(bus) for bus in self.Network.getBusesRTA()])
        return rates
