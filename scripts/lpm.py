#!/usr/bin/env python3

import rospy
import time 
from std_msgs import Int16, Empty

rospy.init_node("lpm_node",anonymous=False)
lpm_pub = rospy.Publisher("/desfibrilador/lpm", Int16, queue_size=1)
start_node = True
first_time = True

lpm = 0
t0 = 0.0

def R_wave_iden(data):
    lpm = lpm + 1
    if(first_time):
        t0 = time.time
        first_time = False
    if(time.time - t0 > 10 and start_node):
        lpm_msg = Int16()
        lpm_msg.data = lpm*6
        lpm_pub.publish(lpm_msg)
        start_node = False
    if(time.time - t0 > 60):
        lpm_msg = Int16()
        lpm_msg.data = lpm
        lpm_pub.publish(lpm_msg)
        lpm = 0
        t0 = time.time

if __name__ == '__main__':
    rospy.Subscriber("/desfibrilador/R_wave_iden",Empty,R_wave_iden)
    rospy.spin()

    
    
