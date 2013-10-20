'''
This class will perform events on the constructed bus network: it will simulate
passenger and bus movement/queueing in the network
'''
class Simulation:
    ''' A class that controls the entire simulation and performs events using
    the constructed bus network'''
    def __init__(self):
        self.ignoreWarnings = False
        self.optimiseParameters = False
