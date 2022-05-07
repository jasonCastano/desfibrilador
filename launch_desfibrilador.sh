sudo chmod 777 /dev/ttyACM0
sudo chmod 777 /dev/ttyACM1
roscore &
rosrun desfibrilador gui.py &
rosrun desfibrilador ecg_signal.py &
rosrun desfibrilador comandos_modos.py &
rosrun desfibrilador lpm.py &
wait
