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


    @staticmethod
    def __parseLine(line, network, simulation):
        ''' Method for parsing a line of input into a method call that changes
        the network and simulation objects'''
        # Parsing arguments that affect the simulation object:
        if line.startswith('board'):
            simulation.setBoardRatio(line.split(' ')[1])
        elif line.startswith('disembarks'):
            simulation.setDisembarksRatio(line.split(' ')[1])
        elif line.startswith('departs'):
            simulation.setDepRatio(line.split(' ')[1])
        elif line.startswith('new passengers'):
            simulation.setNewPassRatio(line.split(' ')[2])
        elif line.startswith('stop time'):
            simulation.setStopTime(line.split(' ')[2])
        elif line.startswith('ignore warnings'):
            simulation.setIgnoreWarn()
        elif line.startswith('optimise parameters'):
            simulation.optimiseParams()
        # Parsing arguments that affect the network object:
        elif line.startswith('route'):
            matches = re.search('''route\s([0-9]*)\sstops\s([0-9 ]*)\sbuses\s
                                ([0-9]*)\scapacity\s([0-9]*)''', line)
            network.addRoute(matches[0], matches[1], matches[2], matches[3])
        elif line.startswith('road'):
            args = line.split(' ')
            network.addRoad(args[1], args[2], args[3])