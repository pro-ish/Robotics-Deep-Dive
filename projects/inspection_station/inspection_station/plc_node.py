import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger

from inspection_station.messages import dumps_event, loads_event


class PlcNode(Node):
    def __init__(self):
        super().__init__("plc_node")
        self.declare_parameter("station_name", "INSPECTION-STATION-01")
        self.declare_parameter("confidence_threshold", 0.75)

        self.accept_count = 0
        self.reject_count = 0

        self.result_subscriber = self.create_subscription(
            String,
            "/inspection/camera/result",
            self.handle_camera_result,
            10,
        )
        self.command_publisher = self.create_publisher(
            String,
            "/inspection/plc/command",
            10,
        )
        self.reset_service = self.create_service(
            Trigger,
            "/inspection/plc/reset_counts",
            self.handle_reset_counts,
        )

    def handle_camera_result(self, msg):
        event = loads_event(msg.data)
        payload = event["payload"]
        part_id = payload["part_id"]
        passed = bool(payload["passed"])
        confidence = float(payload["confidence"])
        threshold = float(self.get_parameter("confidence_threshold").value)

        command = "ACCEPT" if passed and confidence >= threshold else "REJECT"

        if command == "ACCEPT":
            self.accept_count += 1
        else:
            self.reject_count += 1

        command_msg = String()
        command_msg.data = dumps_event(
            source=self.get_parameter("station_name").value,
            event_type="plc_command",
            payload={
                "part_id": part_id,
                "command": command,
                "confidence": confidence,
                "accept_count": self.accept_count,
                "reject_count": self.reject_count,
            },
        )
        self.command_publisher.publish(command_msg)
        self.get_logger().info(
            f"Part {part_id}: command={command} "
            f"accepted={self.accept_count} rejected={self.reject_count}"
        )

    def handle_reset_counts(self, request, response):
        del request
        self.accept_count = 0
        self.reject_count = 0
        response.success = True
        response.message = "PLC accept/reject counts reset"
        self.get_logger().info(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = PlcNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
