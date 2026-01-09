import os

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    urdf_path = os.path.join(
        get_package_share_path('ayg_description'),
        'urdf',
        'ayg.xacro',
    )

    ayg_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str,
    )

    # Declare launch arguments (with defaults for Studio)
    mesh_server_port_arg = DeclareLaunchArgument(
        'mesh_server_port',
        default_value='8080',
        description='Port for the mesh HTTP server'
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': ayg_description}]
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    mesh_server_node = Node(
        package="ayg_description",
        executable="mesh_server",
        arguments=['--port', LaunchConfiguration('mesh_server_port')],
    )

    return LaunchDescription([
        mesh_server_port_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        mesh_server_node,
    ])
