#!/usr/bin/env python
import sys
import physics as p
import pygame as pg
import pid
import rospy
import math as m
import numpy as np
from geometry_msgs.msg import Pose, Twist
from sbsim.msg import goalmsg
import controller as c
from std_msgs.msg import Int32
from std_msgs.msg import Float64
from sbsim.msg import dirvect
from sbsim.msg import dribble
import random as rnd
import geometry as g
import time

r10p = g.point(0,0)
r11p = g.point(0,0)
r20p = g.point(0,0)
r21p = g.point(0,0)

def r10pcallback(msg):
    global r10p
    r10p.x = msg.position.x
    r10p.y = msg.position.y
    return 0

def r11pcallback(msg):
    global r11p
    r11p.x = msg.position.x
    r11p.y = msg.position.y
    return 0

def r20pcallback(msg):
    global r20p
    r20p.x = msg.position.x
    r20p.y = msg.position.y
    return 0

def r21pcallback(msg):
    global r21p
    r21p.x = msg.position.x
    r21p.y = msg.position.y
    return 0

def run():
    global r10p
    global r11p
    global r20p
    global r21p
    r10pub = rospy.Publisher('/robot1n0/vtg', dirvect, queue_size = 10)
    rospy.Subscriber('/robot1n0/pose',Pose,r10pcallback)
    rospy.Subscriber('/robot1n1/pose',Pose,r11pcallback)
    rospy.Subscriber('/robot2n0/pose',Pose,r20pcallback)
    rospy.Subscriber('/robot2n1/pose',Pose,r21pcallback)
    rate = rospy.Rate(3)
    while(True):
        print 'Enter the go to coordinates'
        x = input('Enter x\n')
        y = input('Enter y\n')
        gtg = g.point(x,y)
        print gtg
        ango = 10000000000
        while(True):
            ango,ang = g.findmingrad(own = r10p,op1 = r20p,op2 = r21p,te1 = r11p,goal = gtg,ango = ango)
            v = dirvect()
            v.speed = 40
            v.vtheta = ang
            v.status = 1
            r10pub.publish(v)
            rate.sleep()
            if (abs(r10p.x - x)<38 and  abs(r10p.y - y)<38):
                v.speed = 40
                v.vtheta = ang
                v.status = 0
                r10pub.publish(v)
                break

if __name__ == '__main__':
    rospy.init_node('testplanner',anonymous=True)
    run()