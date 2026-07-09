import csv
from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from inspection_station.messages import loads_event


class LoggerNode(Node):
    def __init__(self):
        super().__init__("logger_node")
        self.declare_parameter("log_path", "inspection_log.csv")

        log_path = self.get_parameter("log_path").value
        self.log_path = Path(str(log_path))
        self.ensure_header()

        self.subscriptions = [
            self.create_subscription(
                String,
                "/inspection/camera/result",
                self.log_event,
                10,
            ),
            self.create_subscription(
                String,
                "/inspection/plc/command",
                self.log_event,
                10,
            ),
            self.create_subscription(
                String,
                "/inspection/conveyor/state",
                self.log_event,
                10,
            ),
        ]

    def ensure_header(self):
        if self.log_path.exists():
            return
        with self.log_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "source", "event_type", "payload"])

    def log_event(self, msg):
        event = loads_event(msg.data)
        with self.log_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    event["timestamp"],
                    event["source"],
                    event["event_type"],
                    event["payload"],
                ]
            )
        self.get_logger().info(f"Logged {event['event_type']} from {event['source']}")


def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
