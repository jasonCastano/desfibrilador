#!/usr/bin/env python3                                                          
import serial
import sys
import rospy
from std_msgs.msg import Int16
port = "/dev/ttyACM0"

ser = serial.Serial(port, 115200, timeout=1.0)
rospy.init_node("ecg_signal_node", anonymous=False)
ecg_pub = rospy.Publisher("/desfibrilador/ecg_signal",Int16,queue_size=1)
def read_data():
        error = True
        while(error==True):
            try:
                msg = ser.readline()
                ecg_msg = msg.decode('ascii')
                error = False
            except UnicodeDecodeError:
                error = True
        return ecg_msg

while True:
    try:
        ecg_data = read_data()
        ecg_msg = Int16()
        ecg_msg.data = int(ecg_data)
        ecg_pub.publish(ecg_msg)
    except ValueError:
        continue



