Hi all, thanks for checking out the CANvas automotive network mapper. You are now one step closer to knowing the crazy things that go on in your car.

Please use this code at your own risk. If used without following the processes described in the paper (i.e. please don't send diagnostic messages), there is potential to cause permanent damage. Please contact me if you require any help, especially if using a personal vehicle.

This repository is the **first** version of the components described in the CANvas paper at USENIX Security '19. It is not yet automated but these files provide core functionality. We are currently working on making this tool more usable for researchers without automotive network experience.

There are currently *two* major components:
- the source mapping module, and
- the destination mapping module.
    
The code for these modules are written for the Arduino Due and Python3.

The wiring diagrams will be made available but the parts list is below:
- Arduino Due microcontroller
- TI VP232 CAN transceiver (any transceiver should work)
- OBD-II breakout

If you produce network maps for your vehicle, please share them with me and we will create a database of these maps.

If you have any suggestions or requests, please email me (see paper) and I'm happy to work with you!
