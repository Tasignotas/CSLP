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


if __name__ == '__main__':
    unittest.main()