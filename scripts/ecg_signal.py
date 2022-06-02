#!/usr/bin/env python3                                                          
import serial
import sys
import time
import rospy
from std_msgs.msg import Float32, Empty, String
port = "/dev/ttyACM0"

ser = serial.Serial(port, 115200, timeout=1.0)
rospy.init_node("ecg_signal_node", anonymous=False)
ecg_pub = rospy.Publisher("/desfibrilador/ecg_signal",Float32,queue_size=1)
R_wave_iden_pub = rospy.Publisher("/desfibrilador/R_wave_iden",Empty,queue_size=1)
sinc_pub = rospy.Publisher("/desfibrilador/sinc",String,queue_size=1)
R_wave_iden_msg = Empty()
modo = String()
sinc_msg = String()
sinc_msg.data = "R"
descarga_msg = Empty()

first_R = False
sec_5 = False
second_R = False
ms_20 = False
en_sec_5 = True
en_ms_20 = True
descarga = True
new_mode_s = True
t0 = 0.0
def modo_data(data):
    global modo
    global first_R
    global sec_5
    global second_R
    global ms_20
    global en_sec_5
    global t0
    modo.data = data.data
    if(data.data == "S"):
        first_R = False
        sec_5 = False
        second_R = False
        ms_20 = False
        en_sec_5 = True
        en_ms_20 = True
        descarga = True
        new_mode_s = True
        t0 = 0.0
        #print("MODO S")
    else:
        descarga = False



rospy.Subscriber("/desfibrilador/modo",String,modo_data)
descarga_pub = rospy.Publisher("/desfibrilador/descarga_sinc",Empty,queue_size=1)

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
        ecg_data = float(read_data().rstrip("\n"))
        if(ecg_data == 100.0):
            R_wave_iden_pub.publish(R_wave_iden_msg)
            if(modo.data == "S"):
                sinc_pub.publish(sinc_msg)
                if(first_R == False and new_mode_s == True):
                    first_R = True
                    new_mode_s = False
                    #print("FIRST R")
                if(sec_5 == True and second_R == False):
                    second_R = True
                    #print("SECOND R")
        else:
            ecg_msg = Float32()
            ecg_msg.data = float(ecg_data)
            ecg_pub.publish(ecg_msg)
        if(first_R == True and en_sec_5 == True):
            t0 = time.time()
            en_sec_5 = False
        if(time.time() - t0 > 5 and sec_5 == False):
            sec_5 = True
            en_ms_20 = True
            #print(en_ms_20)
        if(sec_5 == True and second_R == True and en_ms_20 == True):
            t0 = time.time()
            en_ms_20 = False
            descarga = True
            #print("TIEMPO PARA 20 MS")
        if(time.time() - t0 > 0.02 and second_R == True and descarga == True):
            descarga_pub.publish(descarga_msg)
            #print("DESCARGA")
            descarga = False

    except ValueError:
        continue
