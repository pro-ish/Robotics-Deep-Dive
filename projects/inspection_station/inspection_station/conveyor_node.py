import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import SetBool

from inspection_station.messages import dumps_event, loads_event


class ConveyorNode(Node):
    def __init__(self):
        super().__init__("conveyor_node")
        self.declare_parameter("line_name", "LINE-A")
        self.declare_parameter("default_speed", 0.5)

        self.enabled = True
        self.speed = float(self.get_parameter("default_speed").value)

        self.command_subscriber = self.create_subscription(
            String,
            "/inspection/plc/command",
            self.handle_plc_command,
            10,
        )
        self.state_publisher = self.create_publisher(
            String,
            "/inspection/conveyor/state",
            10,
        )
        self.enable_service = self.create_service(
            SetBool,
            "/inspection/conveyor/enable",
            self.handle_enable_request,
        )
        self.timer = self.create_timer(1.0, self.publish_state)

    def handle_plc_command(self, msg):
        event = loads_event(msg.data)
        command = event["payload"].get("command")
        part_id = event["payload"].get("part_id")

        if command == "REJECT":
            self.get_logger().warn(f"Part {part_id}: diverting to reject lane")
        elif command == "ACCEPT":
            self.get_logger().info(f"Part {part_id}: continuing down main lane")
        else:
            self.get_logger().warn(f"Unknown PLC command: {command}")

    def handle_enable_request(self, request, response):
        self.enabled = bool(request.data)
        response.success = True
        response.message = "Conveyor enabled" if self.enabled else "Conveyor stopped"
        self.publish_state()
        return response

    def publish_state(self):
        line_name = self.get_parameter("line_name").value
        msg = String()
        msg.data = dumps_event(
            source=line_name,
            event_type="conveyor_state",
            payload={
                "enabled": self.enabled,
                "speed": self.speed if self.enabled else 0.0,
            },
        )
        self.state_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ConveyorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
