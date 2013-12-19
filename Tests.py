import Parser
import Models
import Simulation
import unittest
from mock import Mock
from mock import patch


class ParserTests(unittest.TestCase):

    
    def setUp(self):
        self.simulation = Simulation.Simulation()
    
    
    def testBoard1(self):
        ''' Tests if the board parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('board experiment 0.5 0.6 0.7', self.simulation)
        self.assertEqual(self.simulation.params['general']['board'], [0.5, 0.6, 0.7])
        
        
    def testBoard2(self):
        ''' Tests if the board parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('board 0.5', self.simulation)
        self.assertEqual(self.simulation.params['general']['board'], [0.5])
        
        
    def testBoard3(self):
        ''' Tests if the board parameters are parsed correctly by the parser'''
        self.assertRaises(Exception, Parser.Parser._parseLine, 'board ', self.simulation)
        self.assertRaises(Exception, Parser.Parser._parseLine, 'board 0.5 0.6 0.7', self.simulation)
        

    def testDisembarks1(self):
        ''' Tests if the disembarks parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('disembarks experiment 0.5 0.6 0.7', self.simulation)
        self.assertEqual(self.simulation.params['general']['disembarks'], [0.5, 0.6, 0.7])
        
        
    def testDisembarks2(self):
        ''' Tests if the disembarks parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('disembarks 0.5', self.simulation)
        self.assertEqual(self.simulation.params['general']['disembarks'], [0.5])
        
        
    def testDisembarks3(self):
        ''' Tests if the disembarks parameters are parsed correctly by the parser'''
        self.assertRaises(Exception, Parser.Parser._parseLine, 'disembarks 0.5 0.6 0.7', self.simulation)
        
        
    def testDeparts1(self):
        ''' Tests if the departs parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('departs experiment 0.5 0.6 0.7', self.simulation)
        self.assertEqual(self.simulation.params['general']['departs'], [0.5, 0.6, 0.7])
        
        
    def testDeparts2(self):
        ''' Tests if the departs parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('departs 0.5', self.simulation)
        self.assertEqual(self.simulation.params['general']['departs'], [0.5])
        
        
    def testDeparts3(self):
        ''' Tests if the departs parameters are parsed correctly by the parser'''    
        self.assertRaises(Exception, Parser.Parser._parseLine, 'departs 0.5 0.6 0.7', self.simulation)
        
        
    def testNewPassengers1(self):
        ''' Tests if the new passengers parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('new passengers experiment 0.5 0.6 0.7', self.simulation)
        self.assertEqual(self.simulation.params['general']['new passengers'], [0.5, 0.6, 0.7])
        
        
    def testNewPassengers2(self):
        ''' Tests if the new passengers parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('new passengers 0.5', self.simulation)
        self.assertEqual(self.simulation.params['general']['new passengers'], [0.5])
        
    
    def testNewPassengers3(self):
        ''' Tests if the new passengers parameters are parsed correctly by the parser'''
        self.assertRaises(Exception, Parser.Parser._parseLine, 'new passengers 0.5 0.6 0.7', self.simulation)
        
    
    def testStopTime(self):
        ''' Tests if the stop time parameters are parsed correctly by the parser'''
        Parser.Parser._parseLine('stop time 111.1', self.simulation)
        self.assertEqual(self.simulation.params['control']['stopTime'], 111.1)
        
    
    def testIgnoreWarnings(self):
        ''' Tests if the ignore warnings flag was set as expected'''
        Parser.Parser._parseLine('ignore warnings', self.simulation)
        self.assertEqual(self.simulation.params['control']['ignoreWarnings'], True)


    def testOptimiseParameters(self):
        ''' Tests if the ignore warnings flag was set as expected'''
        Parser.Parser._parseLine('optimise parameters', self.simulation)
        self.assertEqual(self.simulation.params['control']['optimiseParameters'], True)


    def testInvalidLine(self):
        '''Tests if error is thrown for an invalid input line'''
        self.assertRaises(Exception, Parser.Parser._parseLine, 'a wrong line', self.simulation)
        
    
    def testCommentOrEmptyLine(self):
        '''Tests if comments and empty lines are ignored'''
        Parser.Parser._parseLine('#comment', self.simulation)
        self.assertEqual(self.simulation, Simulation.Simulation())
        self.assertEqual(self.simulation.Network, Models.Network())
        Parser.Parser._parseLine('', self.simulation)
        self.assertEqual(self.simulation, Simulation.Simulation())
        self.assertEqual(self.simulation.Network, Models.Network())
        

    def testRoad(self):
        ''' Tests if the road parameters are parsed correctly by the parser:
            1. Checks if the addRoad method is called with correct parameters
            2. Checks if an exception is raised with incorrectly structured input'''
        with patch.object(self.simulation, 'addRoad') as mock:
            Parser.Parser._parseLine('road 1 2 0.3', self.simulation)
        mock.assert_called_with(1, 2, [0.3])
        with patch.object(self.simulation, 'addRoad') as mock:
            Parser.Parser._parseLine('road 1 2 experiment 0.3 0.5 0.8', self.simulation)
        mock.assert_called_with(1, 2, [0.3, 0.5, 0.8])
        self.assertRaises(Exception, Parser.Parser._parseLine, 'road 1 2 4', self.simulation)
        
        
    def testRoute(self):
        ''' Tests if the route parameters are parsed correctly by the parser:
            1. Checks if the addRoute method is called with correct parameters
            2. Checks if an exception is raised with incorrectly structured input'''
        with patch.object(self.simulation, 'addRoute') as mock:
            Parser.Parser._parseLine('route 1 stops 1 2 3 buses 4 capacity 50', self.simulation)
        mock.assert_called_with(1, [1, 2, 3], [4], [50])
        with patch.object(self.simulation, 'addRoute') as mock:
            Parser.Parser._parseLine('route 1 stops 1 2 3 buses experiment 4 5 6 capacity 50', self.simulation)
        mock.assert_called_with(1, [1, 2, 3], [4, 5, 6], [50])
        with patch.object(self.simulation, 'addRoute') as mock:
            Parser.Parser._parseLine('route 1 stops 1 2 3 buses 4 capacity experiment 50 500', self.simulation)
        mock.assert_called_with(1, [1, 2, 3], [4], [50, 500])
        with patch.object(self.simulation, 'addRoute') as mock:
            Parser.Parser._parseLine('route 1 stops 1 2 3 buses experiment 4 5 9 capacity experiment 50 55 100', self.simulation)
        mock.assert_called_with(1, [1, 2, 3], [4, 5, 9], [50, 55, 100])
        self.assertRaises(Exception, Parser.Parser._parseLine, 'route 1 stops 1 2 3 buses experiment capacity 50', self.simulation)


class SimulationTests(unittest.TestCase):
    ''' This test case is going to be checking 3 main things:
        1. Is the initial network constructed correctly?
        2. Are the possible events and their rates calculated correctly?
        3. Are the events carried out properly - is the resulting network correct?
    '''
    
    def setUp(self):
        ''' Constructing the test simulation'''
        self.simulation = Simulation.Simulation()
        Parser.Parser._parseLine('route 1 stops 1 2 3 buses 4 capacity 50', self.simulation)
        Parser.Parser._parseLine('route 2 stops 3 5 8 buses 2 capacity 10', self.simulation)
        Parser.Parser._parseLine('road 1 2 0.3', self.simulation)
        Parser.Parser._parseLine('road 2 3 0.7', self.simulation)
        Parser.Parser._parseLine('road 3 1 0.2', self.simulation)
        Parser.Parser._parseLine('road 3 5 0.3', self.simulation)
        Parser.Parser._parseLine('road 5 3 0.1', self.simulation)
        Parser.Parser._parseLine('road 5 8 0.6', self.simulation)
        Parser.Parser._parseLine('road 8 3 0.8', self.simulation)
        Parser.Parser._parseLine('stop time 111.1', self.simulation)
        Parser.Parser._parseLine('new passengers 0.5', self.simulation)
        Parser.Parser._parseLine('departs 0.5', self.simulation)
        Parser.Parser._parseLine('disembarks 0.5', self.simulation)
        Parser.Parser._parseLine('board 0.3', self.simulation)
        ''' Constructing an equivalent simulation manually'''
        self.expectedSimulation = Simulation.Simulation()
        self.expectedSimulation.params['general']['board'] = [0.3]
        self.expectedSimulation.params['general']['disembarks'] = [0.5]
        self.expectedSimulation.params['general']['departs'] = [0.5]
        self.expectedSimulation.params['general']['new passengers'] = [0.5]
        self.expectedSimulation.params['control']['stopTime'] = 111.1
        self.expectedSimulation.Network.params['board'] = 0.3
        self.expectedSimulation.Network.params['disembarks'] = 0.5
        self.expectedSimulation.Network.params['departs'] = 0.5
        self.expectedSimulation.Network.params['new passengers'] = 0.5
        self.expectedSimulation.Network.routes = {
                                             1 : Models.Route([1, 2, 3], 1, 50),
                                             2 : Models.Route([3, 5, 8], 2, 10)
                                             }
        self.expectedSimulation.Network.routes[1].buses = [Models.Bus(1, 0, 50, 1),
                                                      Models.Bus(1, 1, 50, 2),
                                                      Models.Bus(1, 2, 50, 3),
                                                      Models.Bus(1, 3, 50, 1)]
        self.expectedSimulation.Network.routes[2].buses = [Models.Bus(2, 0, 10, 3),
                                                      Models.Bus(2, 1, 10, 5)]
        self.expectedSimulation.params['roads'] = {
                                            (1, 2) : [0.3],
                                            (2, 3) : [0.7],
                                            (3, 1) : [0.2],
                                            (3, 5) : [0.3],
                                            (5, 3) : [0.1],
                                            (5, 8) : [0.6],
                                            (8, 3) : [0.8]
                                            }
        self.expectedSimulation.params['routes'] = {
                                               1 : {
                                                    'routeID' : [1],
                                                    'buses' : [4],
                                                    'capacity' : [50]
                                                    },
                                               2 : {
                                                    'routeID' : [2],
                                                    'buses' : [2],
                                                    'capacity' : [10]
                                                    }
                                               }
        self.expectedSimulation.Network.stops = {
                                            1: Models.Stop(1),
                                            2: Models.Stop(2),
                                            3: Models.Stop(3),
                                            5: Models.Stop(5),
                                            8: Models.Stop(8)
                                            }
        self.expectedSimulation.Network.stops[1].numberOfBusesQueued = 2
        self.expectedSimulation.Network.stops[2].numberOfBusesQueued = 1
        self.expectedSimulation.Network.stops[3].numberOfBusesQueued = 2
        self.expectedSimulation.Network.stops[5].numberOfBusesQueued = 1
        self.expectedSimulation.Network.stops[8].numberOfBusesQueued = 0
        self.expectedSimulation.Network.stops[1].reachableStops = [2, 3]
        self.expectedSimulation.Network.stops[2].reachableStops = [1, 3]
        self.expectedSimulation.Network.stops[3].reachableStops = [1, 2, 5, 8]
        self.expectedSimulation.Network.stops[5].reachableStops = [3, 8]
        self.expectedSimulation.Network.stops[8].reachableStops = [3, 5]
        self.expectedSimulation.Network.stops[1].qOfBuses = [self.expectedSimulation.Network.routes[1].buses[0],
                                                        self.expectedSimulation.Network.routes[1].buses[3]]
        self.expectedSimulation.Network.stops[2].qOfBuses = [self.expectedSimulation.Network.routes[1].buses[1]]
        self.expectedSimulation.Network.stops[3].qOfBuses = [self.expectedSimulation.Network.routes[1].buses[2],
                                                        self.expectedSimulation.Network.routes[2].buses[0]]
        self.expectedSimulation.Network.stops[5].qOfBuses = [self.expectedSimulation.Network.routes[2].buses[1]]
        self.assertTrue(self.expectedSimulation == self.simulation)


    def testInitialNetwork(self):
        ''' This method will check if the constructed network looks as expected'''
        self.assertEqual(self.expectedSimulation, self.simulation)       


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParserTests))
    suite.addTest(unittest.makeSuite(SimulationTests))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)