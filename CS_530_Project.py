# CS 530- Fall Detection Program
# Authors:
# Shane Tasker, Alyssa Garcia, Sawyer Thompson, Alexander Ray

#Import statements
import time

fallVelocity = 0
fallen = false

#Main while loop that constantly queries the accelerometer for current velocity,
# and makes a call if it is determined that a person is falling
while not fallen:
    contactInfo = "" #Store user inputted contact info
    acceleration = detectFall() #Call fall detection function which interfaces with accelerometer
    if acceleration > 1: # If object or person is falling
        call(contactInfo) # Make emergency call
        fallen = true # exit loop
    #Potentially have small delay in program to not query accelerometer a ridiculous number of times
    time.sleep(0.1)

#Detect and return current acceleration
def detectFall():
    acceleration = input from accelerometer #Store current acceleration
    return acceleration #Return value found

#Make emergency call based on inputted contact info
def call(contactInfo):
    make call to contactInfo number or send email to contactInfo email

