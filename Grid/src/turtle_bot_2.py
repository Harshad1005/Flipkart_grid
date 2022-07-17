#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from math import pow, atan2, sqrt

global goal 
bot = Pose()
vel_msg = Twist()
def pose_update(message):
    bot.position.x = message.position.x
    bot.position.y = message.position.y
    bot.orientation.w = message.orientation.w

def steering_angle(goal):
    goal =Pose()
    return atan2(goal.position.y - bot.position.y,
                     goal.position.x - bot.position.x)

def angle(goal):
    return (steering_angle(goal) - bot.orientation.w)

def distance(goal):
    goal =Pose()
    return sqrt(pow((goal.position.x - bot.position.x), 2) +
                pow((goal.position.y - bot.position.y), 2))

def go(x,y):
    goal = Pose()
    goal.position.x = x
    goal.position.y = y

    
    while True:
        # while angle(goal) >=10 or angle(goal) <=10:
        #     vel_msg.linear.x = 0
        #     vel_msg.linear.y = 0
        #     vel_msg.linear.z = 0
        #     vel_msg.angular.x = 0
        #     vel_msg.angular.y = 0
        #     vel_msg.angular.z = 1.5
        #     vel_publisher.publish(vel_msg)
        while distance(goal)>=50:
            rospy.loginfo(distance(goal))
            vel_msg.linear.x = 0.5
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            vel_publisher.publish(vel_msg)
        if distance(goal)<100:
            vel_msg.linear.x=0
            vel_publisher.publish(vel_msg)
            break


rospy.Subscriber("/bot1/pose",Pose, pose_update)

rospy.init_node("mukesh")
vel_publisher= rospy.Publisher("/cmd_vel",Twist,queue_size=5)



if __name__ == '__main__':
    try:
        
        go(300,200)
        print("reached at the point given")
        go(281,366)
        print("reached at the point given")
        go(52,365)
        print("reached at the point given")
        # go(1,10)
        # print("reached at the point given")
        # go(1,1)
        # print("reached at the point given")
        exit
        
        
        

    except rospy.ROSInterruptException:
        pass

