#!/usr/bin/env python
import rospy
import redis
import json
import math
import tf

from vision_system_msgs.msg import Description3D
from vision_system_msgs.msg import Recognitions3D

from std_msgs.msg import Header
from std_msgs.msg import ColorRGBA

from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Vector3

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray


if __name__ == '__main__':
    obj_id = 0
    r = redis.StrictRedis()

    pub = rospy.Publisher('object_markers', MarkerArray, queue_size=10)
    rospy.init_node('object_viewer', anonymous=True)
    
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        marker_array = MarkerArray()
        markers = []
        for obj in r.scan_iter(match='object:*'):
            print(obj)
            j_obj = json.loads(r.get(obj))
            
            marker = Marker()
            marker.ns = 'object'
            marker.id = obj_id
            marker.text = obj.split(':')[-1]
            
            obj_id += 1
            marker.type = 2

            scale = Vector3()
            scale.x = 0.1
            scale.y = 0.1
            scale.z = 0.1

            marker.scale = scale

            pose = Pose()
            pose.position.x = j_obj["position"]["x"]
            pose.position.y = j_obj["position"]["y"]
            pose.position.z = 0
            
            marker.pose = pose
            
            header = Header()
            header.frame_id = "map"
            marker.header = header
            
            color = ColorRGBA()
            color.r = 0
            color.g = 0
            color.b = 255
            color.a = 1
            marker.color = color
            
            markers.append(marker)
        marker_array.markers = markers
        pub.publish(marker_array)
        
        obj_id = 0
        markers = []

        rate.sleep()

    
