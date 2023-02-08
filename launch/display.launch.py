
from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription 
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    r2d2_file_path = get_package_share_path('r2d2_gmapping')
    default_model_path = r2d2_file_path / 'urdf/r2d2.urdf'
    default_rviz_config_path = r2d2_file_path / 'rviz/urdf.rviz'
    
    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path), description='path to robot urdf file')

    rviz_arg = DeclareLaunchArgument(name='rviz_config', default_value=str(default_rviz_config_path), description='Absolute path to rviz config file')

    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]), value_type=str)

    robot_state_publisher_node = Node(package='robot_state_publisher',
                                    executable='robot_state_publisher',
                                    parameters=[{'robot_description': robot_description}])

    rviz_node = Node(package='rviz2',
                    executable='rviz2',
                    name='rviz2',
                    output='screen',
                    arguments=['-d', LaunchConfiguration('rviz_config')])
    
    return LaunchDescription([
        model_arg,
        rviz_arg,
        robot_state_publisher_node,
        rviz_node
    ])