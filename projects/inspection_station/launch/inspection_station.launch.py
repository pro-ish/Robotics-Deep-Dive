from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="inspection_station",
                executable="camera_node",
                name="camera_node",
                parameters=[
                    {
                        "publish_period_sec": 1.0,
                        "defect_rate": 0.25,
                        "camera_id": "CAM-01",
                    }
                ],
            ),
            Node(
                package="inspection_station",
                executable="plc_node",
                name="plc_node",
                parameters=[
                    {
                        "station_name": "INSPECTION-STATION-01",
                        "confidence_threshold": 0.75,
                    }
                ],
            ),
            Node(
                package="inspection_station",
                executable="conveyor_node",
                name="conveyor_node",
                parameters=[
                    {
                        "line_name": "LINE-A",
                        "default_speed": 0.5,
                    }
                ],
            ),
            Node(
                package="inspection_station",
                executable="logger_node",
                name="logger_node",
                parameters=[
                    {
                        "log_path": "inspection_log.csv",
                    }
                ],
            ),
        ]
    )
