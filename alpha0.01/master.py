#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
import timeit
import time
from functools import partial
import cv2
import numpy as np
from cv_bridge import CvBridge

def gps_callback(data):
        print("1: ", data.pose.covariance)
        file1.write(str(data.pose.covariance) + "\n")

def rgb_callback(data): 
        # print("rgb ROS sending delay: " + str(timeit.default_timer() * (10 ** 3) - (data.header.stamp.secs * (10 ** 3) + data.header.stamp.nsecs * (10 ** -6))) + "ms")
        br = CvBridge()
        
        im = br.imgmsg_to_cv2(data, desired_encoding="bgr8")
        #cv2.imwrite("/media/nvidia/ExtremeSSD/rgb_images/" + str(time.time()) + ".jpg", im)
        timestamp1 = '%.10f' % time.time()
        
        filename = "/media/nvidia/ExtremeSSD/rgb_images/" + str(timestamp1) + ".npz"
        
        np.savez_compressed(filename, im)
        # timestamp2 = time.time()
        
        # print(im.shape)
        # im.tofile("/media/nvidia/ExtremeSSD/rgb_images/xxx.txt", sep="\t", format="%s")
        # cv2.imwrite("/media/nvidia/ExtremeSSD/rgb_images/xxx.png", im)
        # print("rgb npz save time: " + str(timestamp2-timestamp1) + "s")
        print(filename)

def depth_callback(data):
        # print("depth ROS sending delay: " + str(timeit.default_timer() * (10 ** 3) - (data.header.stamp.secs * (10 ** 3) + data.header.stamp.nsecs * (10 ** -6))) + "ms")
        br = CvBridge()
        im = br.imgmsg_to_cv2(data, desired_encoding="mono16")
        timestamp1 = '%.10f' % time.time()
        #filename = "/media/nvidia/ExtremeSSD/depth_images/" + str(timestamp1) + ".npz"
        filename = "/media/nvidia/ExtremeSSD/depth_images/" + str(data.header.seq) + ".npz"
        np.savez_compressed(filename, im)
        # timestamp2 = time.time()
        # print("depth npz save time: " + str(timestamp2-timestamp1) + "s")
        # print(filename)

def master():
	rospy.init_node('master', anonymous=True)
        # rospy.Subscriber('RGB', Image, rgb_callback)
        rospy.Subscriber('depth', Image, depth_callback)
        rospy.spin()
        
if __name__ == "__main__":
        master()
