'''
A file containing Parser class that parses the given input. It translates input 
lines into method calls to construct the model of bus network and set the 
parameters of the simulation.
'''
import re
from Models import Network

class Parser:
    ''' Class that takes the input file and constructs the initial model
    of the bus network and the simulation
    '''
    @staticmethod
    def parseFile(inputFileName):
        ''' Static method that parses the given input file'''
        inputFile = open(inputFileName, 'r')
        network = Network
        simulation = Simulation
        for line in inputFile:
            parseLine(line.strip(), network, simulation)
        return network, simulation
