# Robot Learning Deep Dive #1: My First ROS 2 Publisher Node

I have used ROS 2 before, but I am starting again from the basics.

The first time ROS 2 really mattered to me was at Columbia, in Professor Matei Ciocarlie's Robot Learning course. That class had ten tough problems, the kind that make you realize robot software is not just about writing code that runs. It is about understanding the context, defining the problem, respecting the constraints, and only then deciding what the code should do.

That class also taught me something about vibe coding: it can be powerful, but it is not magic. If you do not understand the system you are working inside, you can generate code that looks plausible and still be completely lost. Robotics makes that very obvious. The robot does not care if the code sounds right. It cares whether the assumptions are right.

I also learned how quickly coding knowledge gets rusty. Even knowledge you once fought hard to earn can fade if you do not use it. So this series is partly a technical notebook and partly an endeavor to keep the robot generalist in me alive.

This first post starts small: one ROS 2 publisher node, one topic, one turtle moving in a circle.

The first real lesson was not about robots moving through space. It was about how robot programs find each other.

In ROS 2, a robot is usually not one big program. It is a collection of smaller programs called nodes. Each node does one job. One node might read a camera. Another might control motors. Another might decide where the robot should go next.

The important part is how those nodes communicate.

They do not need to know each other directly. Instead, they meet through topics.

## The First Mental Model

Here is the simplest version:

```text
[publisher node] -> /some_topic -> [subscriber node]
```

The publisher sends messages to a topic. The subscriber listens to that topic. ROS 2 handles the connection.

For the classic `turtlesim` demo, the topic is:

```text
/turtle1/cmd_vel
```

That topic receives velocity commands. If a node publishes the right kind of message there, the turtle moves.

So the real relationship is not:

```text
my node controls turtlesim directly
```

It is:

```text
my node publishes Twist messages to /turtle1/cmd_vel
turtlesim subscribes to /turtle1/cmd_vel
ROS 2 delivers the messages
```

That clicked for me.

## The Message Type

The `/turtle1/cmd_vel` topic uses:

```text
geometry_msgs/msg/Twist
```

A `Twist` message has two main parts:

```text
linear
angular
```

For `turtlesim`, the useful fields are:

```text
linear.x   # move forward or backward
angular.z  # rotate left or right
```

So if I publish:

```yaml
linear:
  x: 2.0
angular:
  z: 1.0
```

the turtle moves forward while turning. In other words, it drives in a circle.

## The First Python Publisher

Here is the first ROS 2 node I built:

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

This node does one simple thing every half second:

```text
create a Twist message
set forward speed
set turning speed
publish it to /turtle1/cmd_vel
```

And because `turtlesim_node` is subscribed to that topic, the turtle moves.

## The Debugging Lesson

I also learned a very Windows-specific ROS 2 lesson.

My setup uses `pixi`, so I cannot just open any terminal and expect ROS 2 programs to work. The terminal needs the pixi environment first. Then it needs the ROS 2 setup script. Then, for my own package, it needs my workspace overlay.

The working pattern is:

```cmd
cd /d C:\pixi_ws
pixi shell
cd /d C:\Users\DELL\ros2_ws
call C:\pixi_ws\ros2-windows\setup.bat
call install\setup.bat
```

The word `call` matters on Windows. This is not Linux, so `source install/setup.bash` is the wrong spell here.

For built-in ROS 2 packages like `turtlesim`, I only need:

```cmd
call C:\pixi_ws\ros2-windows\setup.bat
ros2 run turtlesim turtlesim_node
```

For my own package, I also need:

```cmd
call install\setup.bat
ros2 run my_turtle_controller circle_publisher
```

## The Most Useful Command So Far

This command helped make the whole system visible:

```cmd
ros2 topic info /turtle1/cmd_vel --verbose
```

When the turtle was running but my publisher was not, ROS 2 showed:

```text
Publisher count: 0
Subscription count: 1
```

That meant:

```text
turtlesim is listening
my publisher is not running
```

Once both are running, the goal is:

```text
Publisher count: 1
Subscription count: 1
```

That is a beautiful little moment: two separate programs, connected by a topic.

## What I Understand Now

The first big ROS 2 idea is loose coupling.

A publisher does not need to know who receives its messages. A subscriber does not need to know who sent them. They only need to agree on:

```text
topic name
message type
ROS domain/environment
```

That is the beginning of how robot systems scale from a turtle in a window to real machines with sensors, actuators, navigation, and autonomy.

Small node. Small topic. Real architecture.
