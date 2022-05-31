sudo chmod 777 /dev/ttyACM0
sudo chmod 777 /dev/ttyACM1
rosrun desfibrilador ecg_signal.py &
rosrun desfibrilador lpm.py &
rosrun desfibrilador comandos_modos.py &
rosrun desfibrilador gui.py &
wait
