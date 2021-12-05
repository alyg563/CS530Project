# Fall Detector and Messaging System Program
# Program Contributors: Alyssa Garcia, Sawyer Thompson, Alexander Ray, Shane Tasker
# README Author: Shane Tasker

# Summary
# Our project is a fall detector and messaging system integrated into one product. When the user runs the program, it asks for your name, your emergency provider, your emergency    # contact’s phone number, your current location (address), your gmail address, and your password. When a person falls, the fall detector portion of the program will automatically  # detect that the person is falling. It then will issue a call to the messaging program, which then messages the emergency contact with a message: “Name has fallen! Come help     # him at this location! Address”.

# Source Code Structure 
# A lot of the fall detection code was brought in from Sensehat's example code
# At the top of the program is all of the necessary imports, as well as all the variables and all of the register variable definitions needed for the program to work.
# Next is the ICM20948 class, the class that makes the fall detection work. This class consists of the initialization which assigns a lot of values and calls several functions,    # the icm mag read function, the icm read secondary function, the icm gyro offset function, the read (byte, block, u16) functions, the write byte function, the imu AHRS update,   # the icm check function, the icm mag check function, and the icm calculate average value (for Gyro, Acceleration, and Mag) function.
# Next is the Fall Detector Function. This function first calls the icm's (gyro, acceleration, and mag) read functions, the calculate average value function, and the imu AHRS      # update function. This finds all of the gyro, mag, and most importantly, acceleration values and updates them to be their most recent value. It then stores the pitch, roll and    # yaw, as well as converting the acceleration to the correct unit. Finally, it finds the x, y, and z acceleration magnitudes in order to calculate and return the value we are      # looking for, the downward acceleration magnitude, or how fast the device (and therefore the person) is falling.
# Next up is the text function, which sends out an emergency text when called. It first formats the message as a text message that is sent from the user's email address to the      # emergency contact's phone number with a message containing the necessary information.Finally, it sends out the text. 
# Next, there is the main code. It then sets the Fall Threshold and creates the detector. It asks you for important information that will enable it to send the text, which include # the emergency contact number and their Internet Service Provider.
# Finally, there is the main while loop that runs while the fall detector hasn't detected the person falling. It calls the detectFall function, and if the value returned is        # greater than the Fall Threshold (in units of G's), it calls the text function and exits the while loop.

# How to use the prototype
# On the Raspberry PI, you run "sudo python3 CS_530_Project.py". Then, you input the requested values, which include  your name, your emergency provider, your emergency contact’s  # phone number, your current location (address), your gmail address, and your password. Then, you leave the program running, and it will continue running through the detectFall   # function until it detects a fall, and once it does this, it calls the text function, which then will send a text message to the emergency contact.      
