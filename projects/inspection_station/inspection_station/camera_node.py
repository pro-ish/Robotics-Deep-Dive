import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from inspection_station.messages import dumps_event


class CameraNode(Node):
    def __init__(self):
        super().__init__("camera_node")
        self.declare_parameter("publish_period_sec", 1.0)
        self.declare_parameter("defect_rate", 0.25)
        self.declare_parameter("camera_id", "CAM-01")

        period = self.get_parameter("publish_period_sec").value
        self.publisher = self.create_publisher(String, "/inspection/camera/result", 10)
        self.timer = self.create_timer(float(period), self.publish_result)
        self.part_id = 0

    def publish_result(self):
        self.part_id += 1
        defect_rate = float(self.get_parameter("defect_rate").value)
        camera_id = self.get_parameter("camera_id").value

        passed = random.random() > defect_rate
        confidence = random.uniform(0.82, 0.99) if passed else random.uniform(0.55, 0.88)

        msg = String()
        msg.data = dumps_event(
            source=camera_id,
            event_type="inspection_result",
            payload={
                "part_id": self.part_id,
                "passed": passed,
                "confidence": round(confidence, 3),
            },
        )
        self.publisher.publish(msg)
        self.get_logger().info(
            f"Part {self.part_id}: {'PASS' if passed else 'FAIL'} "
            f"confidence={confidence:.3f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
