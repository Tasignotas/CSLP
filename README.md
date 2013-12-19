==========================
CSLP
==========================

Computer Science Large practical project.
I have built a program in python that simulates bus traffic, lets the user experiment with various parameters of the bus network and find the optimal parameter configuration.


==========================
How to run the simulation?
==========================

In order to run the simulation, simply type:


python Simulation.py


Then, when the output prompting for the name of the input file appears, type the name of the input file that you wish to use. A sample data file Data.txt is included. You can run the simulation using Data.txt by entering:


Data.txt


Then, depending on the input, the output from the simulation will appear on the screen and the simulation will eventually terminate.


==========================
Tests
==========================


There are 21 test cases included that check various parts of the program. If you wish to run them, type:


python Tests.py


==========================
Profiling
==========================

I used cProfiler to profile the executeSimulation() method which is where the fun happens. I ran cProfiler on DICE using the project configuration after the 3927a00 commit. The simulation ran for 47.037 seconds in total. The biggest drag on the simulation are the methods that calculate possible events, especially getPaxRTB and getBusesRTD methods. Although it would be wise not to recalculate all of the possible events each time and update the lists of possible events, for now I just decided to optimise those two methods and see what I can achieve. So, with my improvements (commit b9b691a) the simulation runs in 40 seconds.
