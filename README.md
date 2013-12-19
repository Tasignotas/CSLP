==========================
CSLP Bus traffic simulation project by S1137931
==========================

Computer Science Large practical project.
I have built a program in python that simulates bus traffic, lets the user experiment with various parameters of the bus network and find the optimal parameter configuration.


==========================
Design of the simulation
==========================

The two main components of the simulation are the Simulation object and the Network object that the Simulation object controls. The Network object stores the current configuration of the bus network, it has passengers that move on various routes between stops, the Network object "knows" how to add new passengers to itself, move buses, depart passengers and so on. The Simulation object controls the flow of the simulation: it sets up the Network object before the beginning of the simulation, "asks" to generate and perform new events, prints statistics of the Network.

The code is split among 4 main files:


Tests.py - includes unit tests for parser and simulation. The tests were written using unittest framework with Mock

Parser.py - includes a parser object which parses the input file and issues calls to the Simulation object. In this way the Simulation object collects all of the parameters for the simulation.

Models.py - includes the definition of every object in the bus network: Passenger, Bus, Route, Road, Stop and Network objects. Network object contains methods that the Simulation object uses to "communicate" with the Network.

Simulation.py - includes the definition and methods of the Simulation object which sets up the Network object and executes the simulation by "asking" the Network object to get all possible events and picks the event that should be performed next by the Network.


==========================
Environment
==========================

This project has been developed on Ubuntu 13.10 with Python 2.7.5 using Eclipse 4.3.0. Since this needs to run on DICE that uses a sligtly older Python 2.6.6, I was always ssh'ed into DICE, pulled the code from a private github repository and retested it thoroughly for compatibility.

I used various native python libararies except for Mock that needs to be downloaded seperately. I clearly remember that during one of the lectures you spoke about adding the whole library to the project. However, I don't remember if you criticised adding the library to the project or encouraged it... Either way, the library is included and I hope that even if it's a bad thing, it doesn't create you a lot of additional work.

==========================
How to run the simulation?
==========================

In order to run the simulation, simply type:


$ python Simulation.py


Then, when the output prompting for the name of the input file appears, type the name of the input file that you wish to use. A sample data file Data.txt is included. You can run the simulation using Data.txt by entering:


$ Data.txt


Then, depending on the input, the output from the simulation will appear on the screen and the simulation will eventually terminate.


==========================
Tests
==========================


There are 21 test cases included that check the input parser and the actions of the Simulation object. If you wish to run them, type:


$ python Tests.py


==========================
Profiling
==========================

I used cProfiler to profile the executeSimulation() method which is where the fun happens. I ran cProfiler on DICE using the project configuration after the 3927a00 commit. The simulation ran for 47.037 seconds in total. The biggest drag on the simulation are the methods that calculate possible events, especially getPaxRTB and getBusesRTD methods. Although it would be wise not to recalculate all of the possible events each time and update the lists of possible events, for now I just decided to optimise those two methods and see what I can achieve. So, with my improvements (commit b9b691a) the simulation runs in 40 seconds.


=========================
Missing requirements
=========================

I am very sorry, but I couldn't figure out how to effectively calculate the "Average waiting passengers" statistic. Therefore, it is not included in the statistics bit.
