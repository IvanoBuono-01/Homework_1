from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory
armando_description_dir = get_package_share_directory('armando_description')
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit


def generate_launch_description():
    declared_arguments = []
    
    path_armando = os.path.join(
        get_package_share_directory('armando_description'))
        
    xacro_armando = os.path.join(path_armando, "urdf", "armando.urdf.xacro")
    robot_description_armando_xacro = {"robot_description": Command(['xacro ', xacro_armando, '     joint_a3_pos:=2.0', ' joint_a4_pos:=0.2'])}
        

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description_armando_xacro,
                    {"use_sim_time": True},
            ],
    )

    declared_arguments.append(DeclareLaunchArgument('gz_args', default_value='-r -v 1 empty.sdf',
                              description='Arguments for gz_sim'),)


    gazebo_ignition = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [PathJoinSubstitution([FindPackageShare('ros_gz_sim'),
                                    'launch',
                                    'gz_sim.launch.py'])]),
            launch_arguments={'gz_args': LaunchConfiguration('gz_args')}.items()
    )


    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-name', 'iiwa',
                   '-allow_renaming', 'true',],
    )
 
    ign = [gazebo_ignition, gz_spawn_entity]

    joint_state_broadcaster_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    position_controller_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=["position_controller", "--controller-manager", "/controller_manager"],
    )




    delay_joint_state_broadcaster = (
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=gz_spawn_entity,
                on_exit=[joint_state_broadcaster_spawner],
            )
        )
    )



    
    #Launch the ros2 controllers after the model spawns in Gazebo 
    delay_joint_traj_controller = (
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=gz_spawn_entity,
                on_exit=[position_controller_spawner],
            )
        )
    )



    nodes_to_start = [
        robot_state_publisher_node,  
        *ign,
        delay_joint_traj_controller, 
        delay_joint_state_broadcaster
    ]

    return LaunchDescription(declared_arguments + nodes_to_start) 
