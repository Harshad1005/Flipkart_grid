#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
vel_msg = Twist()
class TurtleBot:
    
    def __init__(self,topic,topic_next):       
        rospy.init_node("bot_controller", anonymous=True)
        self.velocity_publisher = rospy.Publisher(topic,Twist, queue_size=10)
        self.vel_pub = rospy.Publisher(topic_next,Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/bot/pose',Pose, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def end(self):
        vel_msg.linear.x=0
        vel_msg.linear.y=0
        vel_msg.linear.z=0
        vel_msg.angular.x=0
        vel_msg.angular.y=0
        vel_msg.angular.z=0
        self.velocity_publisher.publish(vel_msg)
        self.velocity_publisher.publish(vel_msg)
        self.rate.sleep()

    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
       return constant * (self.steering_angle(goal_pose) - self.pose.theta)


    def flip_now(self):
        vel_msg.linear.z = 1
        self.velocity_publisher.publish(vel_msg)
        rospy.sleep(1)
        vel_msg.linear.z= 0
        self.velocity_publisher.publish(vel_msg)

    def turnright(self):
        self.rate.sleep()
        currentangle=self.pose.theta
        # self.rate.sleep()
        while self.pose.theta - currentangle <128:
            print(self.pose.theta - currentangle)
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = -1
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        self.rate.sleep()

    def turnleft(self):
        self.rate.sleep()
        currentangle=self.pose.theta
        # self.rate.sleep()
        while self.pose.theta - currentangle < 280:
            print(self.pose.theta - currentangle)
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 1
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        self.rate.sleep()

    def move2goal(self,x,y):
        goal_pose = Pose()
        goal_pose.x = x      #"Set your x goal: 
        goal_pose.y = y      #"Set your y goal: 
        distance_tolerance = 80  #"Set your tolerance: "
        while True:
            while self.euclidean_distance(goal_pose) >= distance_tolerance:
                vel_msg.linear.x = 0.5  # self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = 0  # self.angular_vel(goal_pose)
                self.velocity_publisher.publish(vel_msg)
            # Stopping our robot after the movement is over.
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

            if self.euclidean_distance(goal_pose) <=distance_tolerance :
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0
                self.velocity_publisher.publish(vel_msg)
                rospy.sleep(1)
                vel_msg.linear.x= 0.5
                vel_msg.linear.y=0
                vel_msg.linear.z=0
                vel_msg.angular.x=0
                vel_msg.angular.y=0
                vel_msg.angular.z=0
                self.vel_pub.publish(vel_msg)

                break
        
if __name__ == '__main__':
    try:
        bot_1 = TurtleBot("/bot1/cmd_vel","/bot2/cmd_vel")
        bot_2 = TurtleBot("/bot2/cmd_vel","/bot3/cmd_vel")
        bot_3 = TurtleBot("/bot3/cmd_vel","/bot4/cmd_vel")
        bot_4 = TurtleBot("/bot4/cmd_vel","/bot5/cmd_vel")
        # bot_1.move2goal(537, 627)
        # print("Reached to goal")
        # bot_1.move2goal(777, 670)
        # print("Reached to goal")
        # # bot_1.flip_now()
        # print("Reached to goal")
        # bot_1.move2goal(777, 670)
        # print("Reached to goal")
        # bot_1.move2goal(777, 670)
        # print("Reached to goal")
        # bot_2.flip_now()

        bot_2.turnleft()
        bot_2.end()
        print("END")
        bot_2.turnright()
        bot_2.end()
        print("END")

        # bot_2.turnleft()
        # print("Reached to goal")
        # bot_2.move2goal(778,539)
        # print("Reached to goal")
        # print("Reached to goal")
        # bot_2.move2goal(778,539)
        # print("Reached to goal")
        # bot_2.move2goal(778,539)
        # print("Reached to goal")
        # bot_3.move2goal(621,214)
        # print("Reached to goal")
        # bot_3.move2goal(621,214)
        # print("Reached to goal")
        # bot_3.flip_now()
        # print("Reached to goal")
        # bot_3.move2goal(621,214)
        # print("Reached to goal")
        # bot_3.move2goal(621,214)
        # print("Reached to goal")
        # bot_4.move2goal(714, 313)
        # bot_4.move2goal(724, 628)
        # print("Reached to goal")
        # bot_4.turn(-2)
        # bot_4.end()
        # bot_4.move2goal(979, 627)

        # bot_4.move2goal(1197, 609)
        # print("Reached to goal")
        # # bot_4.flip_now()
        # bot_4.turn(2)
        # bot_4.end()
        # bot_4.turn(2)
        # bot_4.end()
        # bot_4.move2goal(727, 691)
        # print("Reached to goal")
        # bot_4.turn(2)
        # bot_4.end()
        # bot_4.move2goal(711, 172)
        # print("Reached to goal")

        exit

    except rospy.ROSInterruptException:
        pass