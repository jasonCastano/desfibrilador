#!/usr/bin/env python3                                                          
import serial
import sys
import rospy
from std_msgs.msg import Int16, String
port = "/dev/ttyACM1"

ser = serial.Serial(port, 115200, timeout=1.0)
rospy.init_node("comandos_modos_node", anonymous=False)
modo_pub = rospy.Publisher("/desfibrilador/modo",String,queue_size=1)
carga_pub = rospy.Publisher("/desfibrilador/carga",String,queue_size=1)
descargas_pub = rospy.Publisher("/desfibrilador/descargas",Int16,queue_size=1)
def read_data():
        error = True
        data = []
        while(error==True):
            try:
                msg = ser.readline()
                data_msg = msg.decode('ascii')
                data = data_msg.split(",")
                error = False
            except UnicodeDecodeError:
                error = True
        return data

while True:
    try:
        modo_data = read_data()
        if(modo_data[0] == "M"):
            modo = String()
            modo.data = str(modo_data[1])
            modo_pub.publish(modo)
            modo_pub.publish(modo)
        elif(modo_data[0] == "C"):
            carga = String()
            carga.data = str(modo_data[1])
            carga_pub.publish(carga)
            carga_pub.publish(carga)
        elif(modo_data[0] == "D"):
            descargas = Int16()
            descargas.data = int(modo_data[1])
            descargas_pub.publish(descargas)
            descargas_pub.publish(descargas)
    except ValueError:
        continue



