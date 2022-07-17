#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist


l=0.13
d=0.07


def flip():
    msg.linear.z=1
    rospy.loginfo("FLIPPED")

def left(v,w):
    x=((2*v)-(w*l))/d
    return round(x)


    
def right(v,w):
    x=((2*v)+(w*l))/d
    return round(x)

def callback(message):
    linear=message.linear.x
    angular=message.angular.z
    cal_left=left(linear,angular)
    cal_right=right(linear,angular)
    if abs(cal_left)==2:
        cal_left+=1
        cal_right+=1

    msg.linear.x=cal_left
    msg.linear.y=cal_right

    if message.linear.z==1:
        flip()

    rospy.loginfo(msg.linear.x)
    rospy.loginfo(msg.linear.y)
    pub.publish(msg)
    msg.linear.z=0





msg=Twist()
rospy.init_node("drive_1")
pub=rospy.Publisher("/bot1/drive",Twist,queue_size=10)
rospy.Subscriber("/bot1/cmd_vel",Twist,callback)

rospy.spin()

