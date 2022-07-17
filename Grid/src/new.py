

#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

x = 0
y = 0
yaw = 0

def takepose(pose_message):
    global x, y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def go_to_goalpose(x_goal, y_goal):
    global x, y, yaw
    
    velocity_message = Twist()

    while True:
        K_linear = 0.5
        distance = 1   #abs(math.sqrt((((x_goal - x) ** 2) + ((y_goal - y) ** 2))))

        linear_speed = 1
        angular_speed=1
        while angular_speed>=0.25:
            K_angular = 4.0
            desired_angle_goal = math.atan2(y_goal - y, x_goal-x)
            angular_speed = (desired_angle_goal - yaw) * K_angular
            velocity_message.linear.x = 0
            velocity_message.angular.z = 0.5
            rospy.loginfo(velocity_message)
            velocity_publisher.publish(velocity_message)

        while distance >=0.5:
            distance = abs(math.sqrt((((x_goal - x) ** 2) + ((y_goal - y) ** 2))))
            linear_speed = distance * K_linear
            velocity_message.linear.x = 3
            velocity_message.angular.z = 0
            rospy.loginfo(velocity_message)
            velocity_publisher.publish(velocity_message)
        velocity_message.linear.x = 3
        velocity_message.angular.z = 0
        velocity_publisher.publish(velocity_message)
        if (distance <= 0.5):
            break

    
if __name__ == "__main__":
    try:
        rospy.init_node("turtlesim_motion_pose", anonymous=True)

        cmd_vel_topic = "/turtle1/cmd_vel"
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, takepose)
        time.sleep(2)

        go_to_goalpose(5,5 )
        go_to_goalpose(2,2 )

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated")
