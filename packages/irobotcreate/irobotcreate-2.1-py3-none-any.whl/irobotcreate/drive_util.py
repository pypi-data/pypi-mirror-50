from sensor_packets import Angle
from sensor_packets import Distance

import time

class Drive:
    
    def __init__(self,robot):
        self._robot = robot
        # We can reuse these
        self._angle_packet = Angle()
        self._distance_packet = Distance()
                
    def turn_ccw_to_angle(self,angle_deg):        
        while True:
            self._robot.get_sensor_packet(self._angle_packet)
            if self._angle_packet.since_last_deg>=angle_deg:
                return
            time.sleep(.01)
            
    def turn_cw_to_angle(self,angle_deg): 
        self._robot.get_sensor_packet(self._angle_packet)  
        total = 0
        time.sleep(0.05)
        while True:
            self._robot.get_sensor_packet(self._angle_packet)
            total += self._angle_packet.since_last_deg 
            if total<=angle_deg:
                return
            time.sleep(.1)
    
    def drive_forward_to_distance(self, distance_mm):
        while True:
            self._robot.get_sensor_packet(self._distance_packet)
            if self._distance_packet.since_last_mm>=distance_mm:
                return
            time.sleep(.01)
            
    def drive_backward_to_distance(self, distance_mm):
        while True:
            self._robot.get_sensor_packet(self._distance_packet)
            if self._distance_packet.since_last_mm<=distance_mm:
                return
            time.sleep(.01)        

import time
from IRobotCreate import irobot_create
from IRobotCreate import sensor_packets

robot = irobot_create.Roomba('/dev/ttyUSB0')
robot_util = Drive(robot)

robot.set_mode_safe()

left = sensor_packets.LeftEncoderCounts()
right = sensor_packets.RightEncoderCounts()


#robot.get_sensor_packet(left)
#robot.get_sensor_packet(right)

#lb = left.count
#rb = right.count

robot.set_drive_spin_cw(200)
time.sleep(0.90)

# 200 for 11.44 is 3 turns
# 200 for 0.9 is 45degrees

#

robot.set_drive_stop()


robot.set_mode_passive()
robot.set_mode_stop()


        