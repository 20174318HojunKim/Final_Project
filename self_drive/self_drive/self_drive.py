import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class SelfDrive(Node):
    def __init__(self):
        super().__init__('self_drive')
        lidar_qos_profile = QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
                                       history=rclpy.qos.HistoryPolicy.KEEP_LAST,
                                       depth=1)
        vel_qos_profile = QoSProfile(depth=10)
        self.sub_scan = self.create_subscription(
            LaserScan,
            '/scan',
            self.subscribe_scan,
            lidar_qos_profile)
        self.pub_velo = self.create_publisher(Twist, '/cmd_vel', vel_qos_profile)
        self.step = 0


    def subscribe_scan(self, scan):
        twist = Twist()
        if (0 < scan.ranges[350] < 0.25 or 0 < scan.ranges[10] < 0.25 or 0 < scan.ranges[0] < 0.25) or (0 < scan.ranges[340] < 0.25 or 0 < scan.ranges[20] < 0.25):
            twist.linear.x = 0.
            twist.angular.z = -1.5
            self.get_logger().info(f"scan: {scan.ranges[0]}, stop and turning")
        elif scan.ranges[0] > 0.25 and scan.ranges[90] > 0.25 and scan.ranges[270] > 0.25:
            twist.linear.x = 0.2
            twist.angular.z = 0.
            self.get_logger().info(f"scan: {scan.ranges[0]}, forward")
        else:
            turning = False
            if (0 < scan.ranges[45] < 0.18 or 0 < scan.ranges[55] < 0.18 or 0 < scan.ranges[35] < 0.18 or 0 < scan.ranges[25] < 0.18):
                twist.linear.x = 0.2
                twist.angular.z = -0.22
            elif (scan.ranges[90] > 0.15 or 0 > scan.ranges[80] > 0.16 or scan.ranges[70] > 0.17 or scan.ranges[60] > 0.18) or (scan.ranges[50] > 0.2 or 0 > scan.ranges[40] > 0.2):
                twist.linear.x = 0.2
                twist.angular.z = 0.22
            else:
                twist.linear.x = 0.2
                twist.angular.z = 0.
            if  scan.ranges[60] > 0.25 or scan.ranges[50] > 0.25 or scan.ranges[40] > 0.25:
                turning = True
            if turning:
                if (0 < scan.ranges[145] < 0.25 or 0 < scan.ranges[135] < 0.25 or 0 < scan.ranges[125] < 0.25) or (0 < scan.ranges[115] < 0.25 or 0 < scan.ranges[105] < 0.25 or 0 < scan.ranges[95] < 0.25) or (0 < scan.ranges[85] < 0.25 or 0 < scan.ranges[75] < 0.25 or 0 < scan.ranges[65] < 0.25) or (0 < scan.ranges[55] < 0.25 or 0 < scan.ranges[45] < 0.25):
                    twist.linear.x = 0.2
                    twist.angular.z = 1.5
                    self.get_logger().info(f"scan: {scan.ranges[0]}, turning")
                else:
                    turning = False
        self.pub_velo.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = SelfDrive()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
