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
            Parser._parseLine(line.strip(), network, simulation)
        return network


    @staticmethod
    def _parseLine(line, network, simulation):
        ''' Method for parsing a line of input into a method call that changes
        the network and simulation objects'''
        # Parsing arguments that affect the simulation object:
        try:
            if line.startswith('board'):
                if 'experiment' in line:
                    match = re.match('board\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['boardRatioList'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                else:
                    match = re.match('board\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['boardRatioList'] = [float(match.group(1))]
            elif line.startswith('disembarks'):
                if 'experiment' in line:
                    match = re.match('disembarks\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['disembarksRatioList'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                else:
                    match = re.match('disembarks\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['disembarksRatioList'] = [float(match.group(1))]
            elif line.startswith('departs'):
                if 'experiment' in line:
                    match = re.match('departs\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['depRatioList'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                else:
                    match = re.match('departs\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['depRatioList'] = [float(match.group(1))]
            elif line.startswith('new passengers'):
                if 'experiment' in line:
                    match = re.match('new\spassengers\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['newPassRatioList'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                else:
                    match = re.match('new\spassengers\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['newPassRatioList'] = [float(match.group(1))]
            elif line.startswith('stop time'):
                    match = re.match('stop\stime\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['control']['stopTime'] = float(match.group(1))
            elif line == 'ignore warnings':
                simulation.params['control']['ignoreWarnings'] = True
            elif line == 'optimise parameters':
                simulation.params['control']['optimiseParameters'] = True
            # Parsing arguments that affect the network object:
            elif line.startswith('route'):
                matches = re.search('route\s([0-9]*)\sstops\s([0-9 ]*)\sbuses\s([0-9]*)\scapacity\s([0-9]*)', line).groups()
                network.addRoute(int(matches[0]), map(int, str(matches[1]).split(' ')), int(matches[2]), int(matches[3]))
            elif line.startswith('road'):
                if 'experiment' in line:
                    match = re.match('road\s(0|[1-9][0-9]*)\s(0|[1-9][0-9]*)\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.addRoad(int(match.group(1)), int(match.group(2)), [float(number) for number in (match.group(3).split(' ')[1:])])
                else:
                    match = re.match('road\s(0|[1-9][0-9]*)\s(0|[1-9][0-9]*)\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.addRoad(int(match.group(1)), int(match.group(2)), [float(match.group(3))])
            elif line.startswith('#') or (line == ''):
                return
            else:
                raise Exception('"{0}" could not be recognised as a valid input line'.format(line))
        except:
            raise Exception('Line "{0}" could not be parsed because the values specified are incorrect'.format(line))
