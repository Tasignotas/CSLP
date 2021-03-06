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
        for line in inputFile:
            Parser._parseLine(line.strip(), simulation)


    @staticmethod
    def _parseLine(line, simulation):
        ''' Method for parsing a line of input into a method call that changes
        the network and simulation objects'''
        ''' Parsing arguments that affect the simulation object.
            I wrote rigorous regexes that accept exactly the form of the input that has been specified in the assignment
            If it can't match the expected input, it will raise an informative error.
        '''
        try:
            if line.startswith('board'):
                if simulation.params['general']['board'] != []:
                    raise Exception("The board rate can be specified only once per input file!")
                if 'experiment' in line:
                    match = re.match('board\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['board'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                    simulation.params['control']['experimentation'] = True
                else:
                    match = re.match('board\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['board'] = [float(match.group(1))]
            elif line.startswith('disembarks'):
                if simulation.params['general']['disembarks'] != []:
                    raise Exception("The disembarks rate can be specified only once per input file!")
                if 'experiment' in line:
                    match = re.match('disembarks\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['disembarks'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                    simulation.params['control']['experimentation'] = True
                else:
                    match = re.match('disembarks\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['disembarks'] = [float(match.group(1))]
            elif line.startswith('departs'):
                if simulation.params['general']['departs'] != []:
                    raise Exception("The departs rate can be specified only once per input file!")
                if 'experiment' in line:
                    match = re.match('departs\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['departs'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                    simulation.params['control']['experimentation'] = True
                else:
                    match = re.match('departs\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['departs'] = [float(match.group(1))]
            elif line.startswith('new passengers'):
                if simulation.params['general']['new passengers'] != []:
                    raise Exception("The new passengers rate can be specified only once per input file!")
                if 'experiment' in line:
                    match = re.match('new\spassengers\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.params['general']['new passengers'] = [float(number) for number in (match.group(1).split(' ')[1:])]
                    simulation.params['control']['experimentation'] = True
                else:
                    match = re.match('new\spassengers\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.params['general']['new passengers'] = [float(match.group(1))]
            elif line.startswith('stop time'):
                if 'stop time' in simulation.params['control']:
                    raise Exception("The stop time can be specified only once per input file!")
                match = re.match('stop\stime\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                simulation.params['control']['stopTime'] = float(match.group(1))
            elif line == 'ignore warnings':
                if simulation.params['control']['ignoreWarnings']:
                    raise Exception("Ignore warnings flag can be specified only once per input file!")
                simulation.params['control']['ignoreWarnings'] = True
            elif line == 'optimise parameters':
                if simulation.params['control']['optimiseParameters']:
                    raise Exception("Optimise parameters flag can be specified only once per input file!")
                simulation.params['control']['optimiseParameters'] = True
            # Parsing arguments that affect the network object:
            elif line.startswith('route'):
                match = re.search('route\s(0|[1-9][0-9]*)\sstops((\s(0|[1-9][0-9]*))+)\sbuses\s(experiment((\s(0|[1-9][0-9]*))+)|(0|[1-9][0-9]*))\scapacity\s(experiment((\s(0|[1-9][0-9]*))+)|(0|[1-9][0-9]*))$', line)
                simulation.addRoute(int(match.group(1)), map(int, match.group(2).strip().split(' ')), map(int, match.group(5).replace('experiment', '').strip().split(' ')), map(int, match.group(10).replace('experiment', '').strip().split(' ')))
                if 'experiment' in line:
                    simulation.params['control']['experimentation'] = True
            elif line.startswith('road'):
                if 'experiment' in line:
                    match = re.match('road\s(0|[1-9][0-9]*)\s(0|[1-9][0-9]*)\sexperiment((\s(0|[1-9][0-9]*)\.[0-9]+)+)$', line)
                    simulation.addRoad(int(match.group(1)), int(match.group(2)), [float(number) for number in (match.group(3).split(' ')[1:])])
                    simulation.params['control']['experimentation'] = True
                else:
                    match = re.match('road\s(0|[1-9][0-9]*)\s(0|[1-9][0-9]*)\s((0|[1-9][0-9]*)\.[0-9]+)$', line)
                    simulation.addRoad(int(match.group(1)), int(match.group(2)), [float(match.group(3))])
            elif line.startswith('#') or (line == ''):
                return
            else:
                raise Exception('"{0}" could not be recognised as a valid input line'.format(line))
        except AttributeError, KeyError:
            raise Exception('Line "{0}" could not be parsed because the values specified are incorrect'.format(line))
