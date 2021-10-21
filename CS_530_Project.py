# CS 530- Fall Detection Program
# Authors:
# Shane Tasker, Alyssa Garcia, Sawyer Thompson, Alexander Ray

# Import statements
import time
from sense_hat import SenseHat

fallVelocity = 0
fallen = False
sense = SenseHat()


# Detect and return current acceleration
def detect_fall():
    raw = sense.get_accelerometer_raw()
    acceleration = raw.get("y")  # Store current acceleration
    return acceleration  # Return value found


# Make emergency call based on inputted contact info
def call(contact_info):
    x = 5
    # Make call to contactInfo number or send email to contactInfo email


# Main while loop that constantly queries the accelerometer for current velocity,
# and makes a call if it is determined that a person is falling
contactInfo = ""  # Store user inputted contact info
while not fallen:
    y_acceleration = detect_fall()  # Call fall detection function which interfaces with accelerometer
    if y_acceleration > 1:  # If object or person is falling
        call(contactInfo)  # Make emergency call
        fallen = True  # exit loop
        # Potentially have small delay in program to not query accelerometer a ridiculous number of times
        time.sleep(0.1)



