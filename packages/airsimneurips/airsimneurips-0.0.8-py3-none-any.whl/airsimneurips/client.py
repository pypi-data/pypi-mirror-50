"""Summary
"""
from __future__ import print_function

from .utils import *
from .types import *

import msgpackrpc
import numpy as np
import msgpack
import time
import math
import logging

class MultirotorClient(object):

    """Summary
    
    Attributes:
        client (TYPE): Description
    """
    
    def __init__(self, ip = "", port = 41451, timeout_value = 3600):
        """Summary
        
        Args:
            ip (str, optional): Description
            port (int, optional): Description
            timeout_value (int, optional): Description
        """
        if (ip == ""):
            ip = "127.0.0.1"
        self.client = msgpackrpc.Client(msgpackrpc.Address(ip, port), timeout = timeout_value, pack_encoding = 'utf-8', unpack_encoding = 'utf-8')
        
    # -----------------------------------  Common vehicle APIs ---------------------------------------------
    def reset(self):
        """Summary
        """
        self.client.call('reset')

    def ping(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.client.call('ping')

    def getClientVersion(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return 1 # sync with C++ client

    def getServerVersion(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.client.call('getServerVersion')

    def getMinRequiredServerVersion(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return 1 # sync with C++ client

    def getMinRequiredClientVersion(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.client.call('getMinRequiredClientVersion')

    # basic flight control
    def enableApiControl(self, is_enabled, vehicle_name = ''):
        """Summary
        
        Args:
            is_enabled (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('enableApiControl', is_enabled, vehicle_name)

    def isApiControlEnabled(self, vehicle_name = ''):
        """Summary
        
        Args:
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('isApiControlEnabled', vehicle_name)

    def armDisarm(self, arm, vehicle_name = ''):
        """Summary line.
        
        Extended description of function.
        
        Args:
            arm (bool): Description of arg1
            vehicle_name (str): Description of arg2
        
        Returns:
            bool: Description of return value
        
        """
        return self.client.call('armDisarm', arm, vehicle_name)
 
    def simPause(self, is_paused):
        """Summary
        
        Args:
            is_paused (TYPE): Description
        """
        self.client.call('simPause', is_paused)

    def simIsPause(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.client.call("simIsPaused")

    def simContinueForTime(self, seconds):
        """Summary
        
        Args:
            seconds (TYPE): Description
        """
        self.client.call('simContinueForTime', seconds)

    def confirmConnection(self):
        """Summary
        """
        if self.ping():
            print("Connected!")
        else:
             print("Ping returned false!")
        server_ver = self.getServerVersion()
        client_ver = self.getClientVersion()
        server_min_ver = self.getMinRequiredServerVersion()
        client_min_ver = self.getMinRequiredClientVersion()
    
        ver_info = "Client Ver:" + str(client_ver) + " (Min Req: " + str(client_min_ver) + \
              "), Server Ver:" + str(server_ver) + " (Min Req: " + str(server_min_ver) + ")"

        if server_ver < server_min_ver:
            print(ver_info, file=sys.stderr)
            print("AirSim server is of older version and not supported by this client. Please upgrade!")
        elif client_ver < client_min_ver:
            print(ver_info, file=sys.stderr)
            print("AirSim client is of older version and not supported by this server. Please upgrade!")
        else:
            print(ver_info)
        print('')

    # camera control
    # simGetImage returns compressed png in array of bytes
    # image_type uses one of the ImageType members
    def simGetImage(self, camera_name, image_type, vehicle_name = ''):
        """Summary
        
        Args:
            camera_name (TYPE): Description
            image_type (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        # todo: in future remove below, it's only for compatibility to pre v1.2
        camera_name = str(camera_name)

        # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
        result = self.client.call('simGetImage', camera_name, image_type, vehicle_name)
        if (result == "" or result == "\0"):
            return None
        return result

    # camera control
    # simGetImage returns compressed png in array of bytes
    # image_type uses one of the ImageType members
    def simGetImages(self, requests, vehicle_name = ''):
        """Summary
        
        Args:
            requests (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        responses_raw = self.client.call('simGetImages', requests, vehicle_name)
        return [ImageResponse.from_msgpack(response_raw) for response_raw in responses_raw]

    def simGetCollisionInfo(self, vehicle_name = ''):
        """Summary
        
        Args:
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return CollisionInfo.from_msgpack(self.client.call('simGetCollisionInfo', vehicle_name))

    def simSetVehiclePose(self, pose, ignore_collison, vehicle_name = ''):
        """Summary
        
        Args:
            pose (TYPE): Description
            ignore_collison (TYPE): Description
            vehicle_name (str, optional): Description
        """
        self.client.call('simSetVehiclePose', pose, ignore_collison, vehicle_name)

    def simGetVehiclePose(self, vehicle_name = ''):
        """Summary
        
        Args:
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        pose = self.client.call('simGetVehiclePose', vehicle_name)
        return Pose.from_msgpack(pose)

    def simGetObjectPose(self, object_name):
        """Summary
        
        Args:
            object_name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        pose = self.client.call('simGetObjectPose', object_name)
        return Pose.from_msgpack(pose)

    def simSetObjectPose(self, object_name, pose, teleport = True):
        """Summary
        
        Args:
            object_name (TYPE): Description
            pose (TYPE): Description
            teleport (bool, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('simSetObjectPose', object_name, pose, teleport)

    def simListSceneObjects(self, name_regex = '.*'):
        """Summary
        
        Args:
            name_regex (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('simListSceneObjects', name_regex)

    def simLoadLevel(self, level_name):
        """Summary
        
        Args:
            level_name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('simLoadLevel', level_name)

    def simSetSegmentationObjectID(self, mesh_name, object_id, is_name_regex = False):
        """Summary
        
        Args:
            mesh_name (TYPE): Description
            object_id (TYPE): Description
            is_name_regex (bool, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('simSetSegmentationObjectID', mesh_name, object_id, is_name_regex)

    def simGetSegmentationObjectID(self, mesh_name):
        """Summary
        
        Args:
            mesh_name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('simGetSegmentationObjectID', mesh_name)

    def simPrintLogMessage(self, message, message_param = "", severity = 0):
        """Summary
        
        Args:
            message (TYPE): Description
            message_param (str, optional): Description
            severity (int, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('simPrintLogMessage', message, message_param, severity)

    def simGetCameraInfo(self, camera_name, vehicle_name = ''):
        """Summary
        
        Args:
            camera_name (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        # TODO: below str() conversion is only needed for legacy reason and should be removed in future
        return CameraInfo.from_msgpack(self.client.call('simGetCameraInfo', str(camera_name), vehicle_name))

    def simSetCameraOrientation(self, camera_name, orientation, vehicle_name = ''):
        """Summary
        
        Args:
            camera_name (TYPE): Description
            orientation (TYPE): Description
            vehicle_name (str, optional): Description
        """
        # TODO: below str() conversion is only needed for legacy reason and should be removed in future
        self.client.call('simSetCameraOrientation', str(camera_name), orientation, vehicle_name)

    def simGetGroundTruthKinematics(self, vehicle_name = ''):
        """Summary
        
        Args:
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        kinematics_state = self.client.call('simGetGroundTruthKinematics', vehicle_name)
        return KinematicsState.from_msgpack(kinematics_state)
    simGetGroundTruthKinematics.__annotations__ = {'return': KinematicsState}

    def cancelLastTask():
        """Summary
        """
        self.client.call('cancelLastTask')

    def waitOnLastTask(timeout_sec = float('nan')):
        """Summary
        
        Args:
            timeout_sec (TYPE, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call('waitOnLastTask', timeout_sec)

# -----------------------------------  Multirotor APIs ---------------------------------------------

    def takeoffAsync(self, timeout_sec = 20, vehicle_name = ''):
        """Summary
        
        Args:
            timeout_sec (int, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('takeoff', timeout_sec, vehicle_name)  

    def landAsync(self, timeout_sec = 60, vehicle_name = ''):
        """Summary
        
        Args:
            timeout_sec (int, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('land', timeout_sec, vehicle_name)   

    def goHomeAsync(self, timeout_sec = 3e+38, vehicle_name = ''):
        """Summary
        
        Args:
            timeout_sec (float, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('goHome', timeout_sec, vehicle_name)

    # APIs for control
    def moveByRollPitchYawZAsync(self, roll, pitch, yaw, z, duration, vehicle_name = ''):
        """Summary
        
        Args:
            roll (TYPE): Description
            pitch (TYPE): Description
            yaw (TYPE): Description
            z (TYPE): Description
            duration (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveByRollPitchYawZ', roll, -pitch, -yaw, z, duration, vehicle_name)

    def moveByRollPitchYawThrottleAsync(self, roll, pitch, yaw, throttle, duration, vehicle_name = ''):
        """Summary
        
        Args:
            roll (TYPE): Description
            pitch (TYPE): Description
            yaw (TYPE): Description
            throttle (TYPE): Description
            duration (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveByRollPitchYawThrottle', roll, -pitch, -yaw, throttle, duration, vehicle_name)

    def moveByRollPitchYawrateThrottleAsync(self, roll, pitch, yaw_rate, throttle, duration, vehicle_name = ''):
        """Summary
        
        Args:
            roll (TYPE): Description
            pitch (TYPE): Description
            yaw_rate (TYPE): Description
            throttle (TYPE): Description
            duration (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveByRollPitchYawrateThrottle', roll, -pitch, -yaw_rate, throttle, duration, vehicle_name)

    def moveByRollPitchYawrateZAsync(self, roll, pitch, yaw_rate, z, duration, vehicle_name = ''):
       """Summary
       
       Args:
           roll (TYPE): Description
           pitch (TYPE): Description
           yaw_rate (TYPE): Description
           z (TYPE): Description
           duration (TYPE): Description
           vehicle_name (str, optional): Description
       
       Returns:
           TYPE: Description
       """
       return self.client.call_async('moveByRollPitchYawrateZ', roll, -pitch, -yaw_rate, z, duration, vehicle_name)

    def moveByAngleRatesZAsync(self, roll_rate, pitch_rate, yaw_rate, z, duration, vehicle_name = ''):
        """Summary
        
        Args:
            roll_rate (TYPE): Description
            pitch_rate (TYPE): Description
            yaw_rate (TYPE): Description
            z (TYPE): Description
            duration (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveByAngleRatesZ', roll_rate, -pitch_rate, -yaw_rate, z, duration, vehicle_name)

    def moveByAngleRatesThrottleAsync(self, roll_rate, pitch_rate, yaw_rate, throttle, duration, vehicle_name = ''):
        """Summary
        
        Args:
            roll_rate (TYPE): Description
            pitch_rate (TYPE): Description
            yaw_rate (TYPE): Description
            throttle (TYPE): Description
            duration (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveByAngleRatesThrottle', roll_rate, -pitch_rate, -yaw_rate, throttle, duration, vehicle_name)

    def moveByVelocityAsync(self, vx, vy, vz, duration, drivetrain = DrivetrainType.MaxDegreeOfFreedom, yaw_mode = YawMode(), vehicle_name = ''):
        """Summary
        
        Args:
            vx (TYPE): Description
            vy (TYPE): Description
            vz (TYPE): Description
            duration (TYPE): Description
            drivetrain (TYPE, optional): Description
            yaw_mode (TYPE, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveByVelocity', vx, vy, vz, duration, drivetrain, yaw_mode, vehicle_name)

    def moveByVelocityZAsync(self, vx, vy, z, duration, drivetrain = DrivetrainType.MaxDegreeOfFreedom, yaw_mode = YawMode(), vehicle_name = ''):
        """Summary
        
        Args:
            vx (TYPE): Description
            vy (TYPE): Description
            z (TYPE): Description
            duration (TYPE): Description
            drivetrain (TYPE, optional): Description
            yaw_mode (TYPE, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveByVelocityZ', vx, vy, z, duration, drivetrain, yaw_mode, vehicle_name)

    def moveOnPathAsync(self, path, velocity, timeout_sec = 3e+38, drivetrain = DrivetrainType.MaxDegreeOfFreedom, yaw_mode = YawMode(), 
        lookahead = -1, adaptive_lookahead = 1, vehicle_name = ''):
        """Summary
        
        Args:
            path (TYPE): Description
            velocity (TYPE): Description
            timeout_sec (float, optional): Description
            drivetrain (TYPE, optional): Description
            yaw_mode (TYPE, optional): Description
            lookahead (TYPE, optional): Description
            adaptive_lookahead (int, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveOnPath', path, velocity, timeout_sec, drivetrain, yaw_mode, lookahead, adaptive_lookahead, vehicle_name)

    def setTrajectoryTrackerGains(self, gains, vehicle_name = ''):
        """Summary
        
        Args:
            gains (TYPE): Description
            vehicle_name (str, optional): Description
        """
        self.client.call('setTrajectoryTrackerGains', gains, vehicle_name)

    def moveOnSplineAsync(self, path, vel_max=15.0, acc_max=7.5, add_curr_odom_position_constraint=True, add_curr_odom_velocity_constraint=True, viz_traj=True, vehicle_name = ''):
        """Summary
        
        Args:
            path (TYPE): Description
            vel_max (float, optional): Description
            acc_max (float, optional): Description
            add_curr_odom_position_constraint (bool, optional): Description
            add_curr_odom_velocity_constraint (bool, optional): Description
            viz_traj (bool, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveOnSpline', path, add_curr_odom_position_constraint, add_curr_odom_velocity_constraint, vel_max, acc_max, viz_traj, vehicle_name)

    def moveOnSplineVelConstraintsAsync(self, path, velocities, vel_max=15.0, acc_max=7.5, add_curr_odom_position_constraint=True, add_curr_odom_velocity_constraint=True, viz_traj=True, vehicle_name = ''):
        """Summary
        
        Args:
            path (TYPE): Description
            velocities (TYPE): Description
            vel_max (float, optional): Description
            acc_max (float, optional): Description
            add_curr_odom_position_constraint (bool, optional): Description
            add_curr_odom_velocity_constraint (bool, optional): Description
            viz_traj (bool, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveOnSplineVelConstraints', path, velocities, add_curr_odom_position_constraint, add_curr_odom_velocity_constraint, vel_max, acc_max, viz_traj, vehicle_name)

    def moveToPositionAsync(self, x, y, z, velocity, timeout_sec = 3e+38, drivetrain = DrivetrainType.MaxDegreeOfFreedom, yaw_mode = YawMode(), 
        lookahead = -1, adaptive_lookahead = 1, vehicle_name = ''):
        """Summary
        
        Args:
            x (TYPE): Description
            y (TYPE): Description
            z (TYPE): Description
            velocity (TYPE): Description
            timeout_sec (float, optional): Description
            drivetrain (TYPE, optional): Description
            yaw_mode (TYPE, optional): Description
            lookahead (TYPE, optional): Description
            adaptive_lookahead (int, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveToPosition', x, y, z, velocity, timeout_sec, drivetrain, yaw_mode, lookahead, adaptive_lookahead, vehicle_name)

    def moveToZAsync(self, z, velocity, timeout_sec = 3e+38, yaw_mode = YawMode(), lookahead = -1, adaptive_lookahead = 1, vehicle_name = ''):
        """Summary
        
        Args:
            z (TYPE): Description
            velocity (TYPE): Description
            timeout_sec (float, optional): Description
            yaw_mode (TYPE, optional): Description
            lookahead (TYPE, optional): Description
            adaptive_lookahead (int, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('moveToZ', z, velocity, timeout_sec, yaw_mode, lookahead, adaptive_lookahead, vehicle_name)

    def moveToYawAsync(self, yaw, timeout_sec = 3e+38, margin = 5, vehicle_name = ''):
        """Summary
        
        Args:
            yaw (TYPE): Description
            timeout_sec (float, optional): Description
            margin (int, optional): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('rotateToYaw', yaw, timeout_sec, margin, vehicle_name)

    def moveByYawRateAsync(self, yaw_rate, duration, vehicle_name = ''):
        """Summary
        
        Args:
            yaw_rate (TYPE): Description
            duration (TYPE): Description
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('rotateByYawRate', yaw_rate, duration, vehicle_name)

    def hoverAsync(self, vehicle_name = ''):
        """Summary
        
        Args:
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.client.call_async('hover', vehicle_name)

    def plot_transform(self, pose_list, vehicle_name = ''):
        """Summary
        
        Args:
            pose_list (TYPE): Description
            vehicle_name (str, optional): Description
        """
        self.client.call('plot_tf', pose_list, 10.0, vehicle_name) 
      
    # query vehicle state
    def getMultirotorState(self, vehicle_name = ''):
        """Summary
        
        Args:
            vehicle_name (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        return MultirotorState.from_msgpack(self.client.call('getMultirotorState', vehicle_name))
    getMultirotorState.__annotations__ = {'return': MultirotorState}
