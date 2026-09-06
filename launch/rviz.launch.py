import os

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    version = LaunchConfiguration('version')
    lidar = LaunchConfiguration('lidar')

    xacro_path = os.path.join(
        get_package_share_path('ayg_description'),
        'urdf',
        'ayg.xacro',
    )

    rviz2_config_file_path = PathJoinSubstitution([
        get_package_share_path('ayg_description').as_posix(),
        'config',
        version,
        'config.rviz',
    ])

    ayg_description = ParameterValue(
        Command(['xacro ', xacro_path, ' version:=', version, ' lidar:=', lidar]),
        value_type=str,
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

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz2_config_file_path],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'version',
            default_value='1.2',
            description='Ayg model version: 1.2 or 1.3 '
                        '(mirrors ayg.xacro\'s `version` arg default).',
        ),
        DeclareLaunchArgument(
            'lidar',
            default_value='true',
            description='Whether to include the lidar_link sensor frame '
                        '(the Head mount itself is always present). Only '
                        'meaningful for version:=1.3.',
        ),
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz2_node
    ])
