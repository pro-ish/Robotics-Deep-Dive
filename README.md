# ROS 2 From The Basics

This repo is my beginner ROS 2 learning workspace. The first milestone is a simple Python publisher node that drives `turtlesim` in a circle.

## What This Demonstrates

- Creating a ROS 2 Python package
- Writing a publisher node with `rclpy`
- Publishing `geometry_msgs/msg/Twist` messages
- Connecting to the built-in `turtlesim_node` through the `/turtle1/cmd_vel` topic
- Debugging topic publisher/subscriber discovery with `ros2 topic info`

## Core Idea

The publisher node does not directly know about `turtlesim_node`.

Instead:

```text
circle_publisher publishes Twist messages to /turtle1/cmd_vel
turtlesim_node subscribes to /turtle1/cmd_vel
ROS 2 delivers the messages
```

ROS 2 connects nodes when the topic name and message type match.

## Package Layout

The package should live under:

```text
C:\Users\DELL\ros2_ws\src\my_turtle_controller
```

The publisher node is:

```text
my_turtle_controller/circle_publisher.py
```

The executable is registered in `setup.py`:

```python
'circle_publisher = my_turtle_controller.circle_publisher:main'
```

## Publisher Node

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CirclePublisher(Node):
    def __init__(self):
        super().__init__("circle_publisher")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.5, self.publish_velocity)

    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.publisher.publish(msg)
        self.get_logger().info("Publishing velocity command")


def main(args=None):
    rclpy.init(args=args)
    node = CirclePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

## Build

This Windows setup uses pixi from:

```text
C:\pixi_ws
```

Build the package with:

```cmd
cd /d C:\Users\DELL\ros2_ws
pixi run -m C:\pixi_ws colcon build --packages-select my_turtle_controller
```

## Run

Terminal 1:

```cmd
cd /d C:\pixi_ws
pixi shell
cd /d C:\Users\DELL\ros2_ws
call C:\pixi_ws\ros2-windows\setup.bat
ros2 run turtlesim turtlesim_node
```

Terminal 2:

```cmd
cd /d C:\pixi_ws
pixi shell
cd /d C:\Users\DELL\ros2_ws
call C:\pixi_ws\ros2-windows\setup.bat
call install\setup.bat
ros2 run my_turtle_controller circle_publisher
```

## Inspect The Topic

```cmd
ros2 topic info /turtle1/cmd_vel --verbose
```

Expected when both nodes are running:

```text
Publisher count: 1
Subscription count: 1
```

## Windows Notes

Use:

```cmd
call install\setup.bat
```

Do not use:

```bash
source install/setup.bash
```

This workspace is running on Windows, not a Linux Bash ROS 2 install.
