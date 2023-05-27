# Simulators-for-SPS
---------------------------------
May 27th, Coding Instruction Update:

The coding has been enhanced using Object-Oriented Programming (OOP), making it easier to extend. Everyone is welcome to utilize the new developed simulator for SPS evaluation. Please access it in the folder "OOP_for_SPS". Compared to the original version, this simulator runs longer because of the fine granularity, but provides convinence for extension. 

We highly recommend trying our newly developed OOP version, as it offers significant advantages for extending the simulator to accommodate new scenarios or applications. 
Besides the convenience provided by objective-oriented programming, this version provides a finer granularity, operating at the millisecond level instead of interval-level simulation. With this enhanced simulator, you can further develop and implement a wide range of new applications supported by the latest standard, including both aperiodic and periodic traffic. 

In addition, the new version uses the argparse.ArgumentParser class in Python, which provides a convenient way to parse command-line arguments and options. 

---------------------------------
This is a simulator for semi-persistent scheduling in C-V2X Mode 4.
Default parameter settings are based on the standard for 20Hz beacon broadcasting. 
The transmit power, beacon range, beacon rate, Reselection Counter range, accessible resource ratio (related to sensing range) can be modified in the simulations.py file.


