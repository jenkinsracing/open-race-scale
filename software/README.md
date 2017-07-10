# Software  
The software is currently designed in two parts.  
1. Core - The core code runs on the RPi3 and communicates with HX711 to receive weights from the loadcells. It does limited calculations with those weights to give standard weighing information. This data (will be) published to a Bluetooth RFComm channel for clients to read.
2. App - The app code at this time runs a local GUI which instantiates the core code. Bluetooth is currently not implemented, however in the future this code will be reused in two ways: local mode for a GUI running on the same RPi3 that is connected to the loadcells, and client mode where the app will operate as a Bluetooth client on a smart phone.  
  
Notes: Both the core and the app can be run on a development PC for testing. See the doc strings in the code for details.  
  
Python 3.x REQUIRED  
  
Core Dependencies: pybluez  
App Dependencies: kivy, pygame, cython  
  
  
Proof of Concept GUI with kivy:  
![POC](https://github.com/jenkinsracing/open-race-scale/blob/master/software/poc-screenshot.png)
