from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time

# Connect to the Pixhawk
connection_string = '/dev/ttyTHS1'
vehicle = connect('udp:127.0.0.1:14551',wait_ready=True)

# Get the home location
home_location = vehicle.location.global_relative_frame

# Print home location
print("Home Location: Latitude = %.7f, Longitude = %.7f" % (home_location.lat, home_location.lon))

# # Close the vehicle connection
# print("Armed: %s" % vehicle.armed)

# # Arm the vehicle
# # Copter should arm in GUIDED mode
# vehicle.mode = VehicleMode("GUIDED")
# vehicle.armed = True
# # vehicle.armed = True

# # Wait for the arm operation to complete (optional)
# if vehicle.armed:
#     print("Vehicle is armed.")
def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print ("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print (" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print( " Waiting for arming...")
        time.sleep(1)

    print ("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print ("Reached target altitude")
            break
        time.sleep(1)

arm_and_takeoff(20)
# Close the vehicle connection
vehicle.close()
