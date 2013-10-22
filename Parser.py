'''
A file containing Parser class that parses the given input. It translates input 
lines into method calls to construct the model of bus network and set the 
parameters of the simulation.
'''
import re
from Models import Network
from Simulation import Simulation


class Parser:
    ''' Class that takes the input file and constructs the initial model
    of the bus network and the simulation
    '''
    @staticmethod
    def parseFile(inputFileName, simulation):
        ''' Static method that parses the given input file'''
        inputFile = open(inputFileName, 'r')
        network = Network()
        for line in inputFile:
            Parser.__parseLine(line.strip(), network, simulation)
        return network


    @staticmethod
    def __parseLine(line, network, simulation):
        ''' Method for parsing a line of input into a method call that changes
        the network and simulation objects'''
        # Parsing arguments that affect the simulation object:
        if line.startswith('board'):
            simulation.boardRatio = float(line.split(' ')[1])
        elif line.startswith('disembarks'):
            simulation.disembarksRatio = float(line.split(' ')[1])
        elif line.startswith('departs'):
            simulation.depRatio = float(line.split(' ')[1])
        elif line.startswith('new passengers'):
            simulation.newPassRatio = float(line.split(' ')[2])
        elif line.startswith('stop time'):
            simulation.stopTime = float(line.split(' ')[2])
        elif line.startswith('ignore warnings'):
            simulation.ignoreWarnings = True
        elif line.startswith('optimise parameters'):
            simulation.optimiseParams = True
        # Parsing arguments that affect the network object:
        elif line.startswith('route'):
            matches = re.search('route\s([0-9]*)\sstops\s([0-9 ]*)\sbuses\s([0-9]*)\scapacity\s([0-9]*)', line).groups()
            network.addRoute(int(matches[0]), map(int, str(matches[1]).split(' ')), int(matches[2]), int(matches[3]))
        elif line.startswith('road'):
            args = line.split(' ')
            network.addRoad(int(args[1]), int(args[2]), float(args[3]))
