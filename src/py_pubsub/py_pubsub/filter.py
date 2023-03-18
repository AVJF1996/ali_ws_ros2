
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32


class MinimalSubscriber(Node):
    
    def __init__(self):
        """self.A = 0.04762
        self.B = 0.04762
        self.C = 0.9048
        self.R = 0
        self.R_1 = 0
        self.Y = 0
        self.Y_1 = 0"""
        self.R_filtered=0
        self.alpha=0.95
        super().__init__('filter_RC')
        self.subscription = self.create_subscription(
            Float32,
            '/srf_1/data',
            self.listener_callback,
            1)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Float32, '/srf_1/data_filtered', 1)
        self.declare_parameter('alpha', 1)
    def listener_callback(self, msg):
        """self.R = msg.data
        self.Y  = self.A*self.R + self.B*self.R_1-self.C*self.Y_1
        self.R_1 = self.R
        self.Y_1 = self.Y"""
        self.alpha = 0.95#self.get_parameter('alpha').get_parameter_value()._double_value
        self.R_filtered=self.alpha*self.R_filtered+(1-self.alpha)*msg.data
        self.get_logger().info('I heard: "%s"' % self.R_filtered)
        msg_filtered = Float32()
        msg_filtered.data = self.R_filtered
        self.publisher_.publish(msg_filtered)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
