

###APPENA APRI ROS2 FAI#########

sudo apt update
sudo apt install ros-humble-joint-state-publisher
sudo apt update
sudo apt install ros-humble-urdf-launch


#### QUESTO COMANDO PERMETTE A GAZEBO DI TROVARE LE MESHES#####
export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:/home/user/ros2_ws/src/armando_description/meshes


ros2 launch armando_gazebo armando_world.launch.py


###### UNA VOLTA AVVIATO ARMANDO_GAZEBO FAI QUESTO PER VEDERE I CONTROLLERS IN RQT##########
### LE ISTRUZIONI SULLE SLIDES A NOI PER QUALCHE MOTIVO NONFUNZIONANO MA LA SEGUENTE SI#######
ros2 run rqt_gui rqt_gui --force-discover





sudo apt-get install ros-<distro>-rqt-controller-manager
ros2 run rqt_controller_manager rqt_controller_manager

#if don't open forced the open
ros2 run rqt_gui rqt_gui --force-discover

##command position controller in CML
ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray "{
  data: [0.0, 0.0, 0.2, 0.0]
}"
