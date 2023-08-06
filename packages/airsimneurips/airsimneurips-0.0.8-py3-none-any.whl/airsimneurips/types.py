"""Summary
"""
from __future__ import print_function
import msgpackrpc #install as admin: pip install msgpack-rpc-python
import numpy as np #pip install numpy

class MsgpackMixin:

    """Summary
    """
    
    def __repr__(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        from pprint import pformat
        return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)

    def to_msgpack(self, *args, **kwargs):
        """Summary
        
        Args:
            *args: Description
            **kwargs: Description
        
        Returns:
            TYPE: Description
        """
        return self.__dict__

    @classmethod
    def from_msgpack(cls, encoded):
        """Summary
        
        Args:
            encoded (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        obj = cls()
        #obj.__dict__ = {k.decode('utf-8'): (from_msgpack(v.__class__, v) if hasattr(v, "__dict__") else v) for k, v in encoded.items()}
        obj.__dict__ = { k : (v if not isinstance(v, dict) else getattr(getattr(obj, k).__class__, "from_msgpack")(v)) for k, v in encoded.items()}
        #return cls(**msgpack.unpack(encoded))
        return obj


class ImageType:    

    """Summary
    
    Attributes:
        DepthPerspective (int): Description
        DepthPlanner (int): Description
        DepthVis (int): Description
        DisparityNormalized (int): Description
        Infrared (int): Description
        Scene (int): Description
        Segmentation (int): Description
        SurfaceNormals (int): Description
    """
    
    Scene = 0
    DepthPlanner = 1
    DepthPerspective = 2
    DepthVis = 3
    DisparityNormalized = 4
    Segmentation = 5
    SurfaceNormals = 6
    Infrared = 7

class DrivetrainType:

    """Summary
    
    Attributes:
        ForwardOnly (int): Description
        MaxDegreeOfFreedom (int): Description
    """
    
    MaxDegreeOfFreedom = 0
    ForwardOnly = 1
    
class LandedState:

    """Summary
    
    Attributes:
        Flying (int): Description
        Landed (int): Description
    """
    
    Landed = 0
    Flying = 1

class Vector3r(MsgpackMixin):

    """Summary
    
    Attributes:
        x_val (float): Description
        y_val (float): Description
        z_val (float): Description
    """
    
    x_val = 0.0
    y_val = 0.0
    z_val = 0.0

    def __init__(self, x_val = 0.0, y_val = 0.0, z_val = 0.0):
        """Summary
        
        Args:
            x_val (float, optional): Description
            y_val (float, optional): Description
            z_val (float, optional): Description
        """
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val

    @staticmethod
    def nanVector3r():
        """Summary
        
        Returns:
            TYPE: Description
        """
        return Vector3r(np.nan, np.nan, np.nan)

    def __add__(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return Vector3r(self.x_val + other.x_val, self.y_val + other.y_val, self.z_val + other.z_val)

    def __sub__(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return Vector3r(self.x_val - other.x_val, self.y_val - other.y_val, self.z_val - other.z_val)

    def __truediv__(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(other) in [int, float] + np.sctypes['int'] + np.sctypes['uint'] + np.sctypes['float']:
            return Vector3r( self.x_val / other, self.y_val / other, self.z_val / other)
        else: 
            raise TypeError('unsupported operand type(s) for /: %s and %s' % ( str(type(self)), str(type(other))) )

    def __mul__(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(other) in [int, float] + np.sctypes['int'] + np.sctypes['uint'] + np.sctypes['float']:
            return Vector3r(self.x_val*other, self.y_val*other, self.z_val*other)
        else: 
            raise TypeError('unsupported operand type(s) for *: %s and %s' % ( str(type(self)), str(type(other))) )

    def dot(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(self) == type(other):
            return self.x_val*other.x_val + self.y_val*other.y_val + self.z_val*other.z_val
        else:
            raise TypeError('unsupported operand type(s) for \'dot\': %s and %s' % ( str(type(self)), str(type(other))) )

    def cross(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(self) == type(other):
            cross_product = np.cross(self.to_numpy_array(), other.to_numpy_array())
            return Vector3r(cross_product[0], cross_product[1], cross_product[2])
        else:
            raise TypeError('unsupported operand type(s) for \'cross\': %s and %s' % ( str(type(self)), str(type(other))) )

    def get_length(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return ( self.x_val**2 + self.y_val**2 + self.z_val**2 )**0.5

    def distance_to(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return ( (self.x_val-other.x_val)**2 + (self.y_val-other.y_val)**2 + (self.z_val-other.z_val)**2 )**0.5

    def to_Quaternionr(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return Quaternionr(self.x_val, self.y_val, self.z_val, 0)

    def to_numpy_array(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return np.array([self.x_val, self.y_val, self.z_val], dtype=np.float32)


class Quaternionr(MsgpackMixin):

    """Summary
    
    Attributes:
        w_val (float): Description
        x_val (float): Description
        y_val (float): Description
        z_val (float): Description
    """
    
    w_val = 0.0
    x_val = 0.0
    y_val = 0.0
    z_val = 0.0

    def __init__(self, x_val = 0.0, y_val = 0.0, z_val = 0.0, w_val = 1.0):
        """Summary
        
        Args:
            x_val (float, optional): Description
            y_val (float, optional): Description
            z_val (float, optional): Description
            w_val (float, optional): Description
        """
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val
        self.w_val = w_val

    @staticmethod
    def nanQuaternionr():
        """Summary
        
        Returns:
            TYPE: Description
        """
        return Quaternionr(np.nan, np.nan, np.nan, np.nan)

    def __add__(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(self) == type(other):
            return Quaternionr( self.x_val+other.x_val, self.y_val+other.y_val, self.z_val+other.z_val, self.w_val+other.w_val )
        else:
            raise TypeError('unsupported operand type(s) for +: %s and %s' % ( str(type(self)), str(type(other))) )

    def __mul__(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(self) == type(other):
            t, x, y, z = self.w_val, self.x_val, self.y_val, self.z_val
            a, b, c, d = other.w_val, other.x_val, other.y_val, other.z_val
            return Quaternionr( w_val = a*t - b*x - c*y - d*z,
                                x_val = b*t + a*x + d*y - c*z,
                                y_val = c*t + a*y + b*z - d*x,
                                z_val = d*t + z*a + c*x - b*y)
        else:
            raise TypeError('unsupported operand type(s) for *: %s and %s' % ( str(type(self)), str(type(other))) )

    def __truediv__(self, other): 
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(other) == type(self): 
            return self * other.inverse()
        elif type(other) in [int, float] + np.sctypes['int'] + np.sctypes['uint'] + np.sctypes['float']:
            return Quaternionr( self.x_val / other, self.y_val / other, self.z_val / other, self.w_val / other)
        else: 
            raise TypeError('unsupported operand type(s) for /: %s and %s' % ( str(type(self)), str(type(other))) )

    def dot(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(self) == type(other):
            return self.x_val*other.x_val + self.y_val*other.y_val + self.z_val*other.z_val + self.w_val*other.w_val
        else:
            raise TypeError('unsupported operand type(s) for \'dot\': %s and %s' % ( str(type(self)), str(type(other))) )

    def cross(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(self) == type(other):
            return (self * other - other * self) / 2
        else:
            raise TypeError('unsupported operand type(s) for \'cross\': %s and %s' % ( str(type(self)), str(type(other))) )

    def outer_product(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if type(self) == type(other):
            return ( self.inverse()*other - other.inverse()*self ) / 2
        else:
            raise TypeError('unsupported operand type(s) for \'outer_product\': %s and %s' % ( str(type(self)), str(type(other))) )

    def rotate(self, other):
        """Summary
        
        Args:
            other (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
            ValueError: Description
        """
        if type(self) == type(other):
            if other.get_length() == 1:
                return other * self * other.inverse()
            else:
                raise ValueError('length of the other Quaternionr must be 1')
        else:
            raise TypeError('unsupported operand type(s) for \'rotate\': %s and %s' % ( str(type(self)), str(type(other))) )        

    def conjugate(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return Quaternionr(-self.x_val, -self.y_val, -self.z_val, self.w_val)

    def star(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.conjugate()

    def inverse(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.star() / self.dot(self)

    def sgn(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self/self.get_length()

    def get_length(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return ( self.x_val**2 + self.y_val**2 + self.z_val**2 + self.w_val**2 )**0.5

    def to_numpy_array(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return np.array([self.x_val, self.y_val, self.z_val, self.w_val], dtype=np.float32)


class Pose(MsgpackMixin):

    """Summary
    
    Attributes:
        orientation (TYPE): Description
        position (TYPE): Description
    """
    
    position = Vector3r()
    orientation = Quaternionr()

    def __init__(self, position_val = Vector3r(), orientation_val = Quaternionr()):
        """Summary
        
        Args:
            position_val (TYPE, optional): Description
            orientation_val (TYPE, optional): Description
        """
        self.position = position_val
        self.orientation = orientation_val

    @staticmethod
    def nanPose():
        """Summary
        
        Returns:
            TYPE: Description
        """
        return Pose(Vector3r.nanVector3r(), Quaternionr.nanQuaternionr())


class CollisionInfo(MsgpackMixin):

    """Summary
    
    Attributes:
        has_collided (bool): Description
        impact_point (TYPE): Description
        normal (TYPE): Description
        object_id (int): Description
        object_name (str): Description
        penetration_depth (float): Description
        position (TYPE): Description
        time_stamp (float): Description
    """
    
    has_collided = False
    normal = Vector3r()
    impact_point = Vector3r()
    position = Vector3r()
    penetration_depth = 0.0
    time_stamp = 0.0
    object_name = ""
    object_id = -1

class YawMode(MsgpackMixin):

    """Summary
    
    Attributes:
        is_rate (bool): Description
        yaw_or_rate (float): Description
    """
    
    is_rate = True
    yaw_or_rate = 0.0
    def __init__(self, is_rate = True, yaw_or_rate = 0.0):
        """Summary
        
        Args:
            is_rate (bool, optional): Description
            yaw_or_rate (float, optional): Description
        """
        self.is_rate = is_rate
        self.yaw_or_rate = yaw_or_rate

class ImageRequest(MsgpackMixin):

    """Summary
    
    Attributes:
        camera_name (str): Description
        compress (bool): Description
        image_type (TYPE): Description
        pixels_as_float (bool): Description
    """
    
    camera_name = '0'
    image_type = ImageType.Scene
    pixels_as_float = False
    compress = False

    def __init__(self, camera_name, image_type, pixels_as_float = False, compress = True):
        """Summary
        
        Args:
            camera_name (TYPE): Description
            image_type (TYPE): Description
            pixels_as_float (bool, optional): Description
            compress (bool, optional): Description
        """
        # todo: in future remove str(), it's only for compatibility to pre v1.2
        self.camera_name = str(camera_name)
        self.image_type = image_type
        self.pixels_as_float = pixels_as_float
        self.compress = compress


class ImageResponse(MsgpackMixin):

    """Summary
    
    Attributes:
        camera_orientation (TYPE): Description
        camera_position (TYPE): Description
        compress (bool): Description
        height (int): Description
        image_data_float (float): Description
        image_data_uint8 (TYPE): Description
        image_type (TYPE): Description
        message (str): Description
        pixels_as_float (float): Description
        time_stamp (TYPE): Description
        width (int): Description
    """
    
    image_data_uint8 = np.uint8(0)
    image_data_float = 0.0
    camera_position = Vector3r()
    camera_orientation = Quaternionr()
    time_stamp = np.uint64(0)
    message = ''
    pixels_as_float = 0.0
    compress = True
    width = 0
    height = 0
    image_type = ImageType.Scene

class KinematicsState(MsgpackMixin):

    """Summary
    
    Attributes:
        angular_acceleration (TYPE): Description
        angular_velocity (TYPE): Description
        linear_acceleration (TYPE): Description
        linear_velocity (TYPE): Description
        orientation (TYPE): Description
        position (TYPE): Description
    """
    
    position = Vector3r()
    orientation = Quaternionr()
    linear_velocity = Vector3r()
    angular_velocity = Vector3r()
    linear_acceleration = Vector3r()
    angular_acceleration = Vector3r()


class RCData(MsgpackMixin):

    """Summary
    
    Attributes:
        is_initialized (bool): Description
        is_valid (bool): Description
        pitch (TYPE): Description
        roll (TYPE): Description
        switch1 (TYPE): Description
        switch2 (TYPE): Description
        switch3 (TYPE): Description
        switch4 (TYPE): Description
        switch5 (TYPE): Description
        switch6 (TYPE): Description
        switch7 (TYPE): Description
        switch8 (TYPE): Description
        throttle (TYPE): Description
        timestamp (int): Description
        yaw (TYPE): Description
    """
    
    timestamp = 0
    pitch, roll, throttle, yaw = (0.0,)*4 #init 4 variable to 0.0
    switch1, switch2, switch3, switch4 = (0,)*4
    switch5, switch6, switch7, switch8 = (0,)*4
    is_initialized = False
    is_valid = False
    def __init__(self, timestamp = 0, pitch = 0.0, roll = 0.0, throttle = 0.0, yaw = 0.0, switch1 = 0,
                 switch2 = 0, switch3 = 0, switch4 = 0, switch5 = 0, switch6 = 0, switch7 = 0, switch8 = 0, is_initialized = False, is_valid = False):
        """Summary
        
        Args:
            timestamp (int, optional): Description
            pitch (float, optional): Description
            roll (float, optional): Description
            throttle (float, optional): Description
            yaw (float, optional): Description
            switch1 (int, optional): Description
            switch2 (int, optional): Description
            switch3 (int, optional): Description
            switch4 (int, optional): Description
            switch5 (int, optional): Description
            switch6 (int, optional): Description
            switch7 (int, optional): Description
            switch8 (int, optional): Description
            is_initialized (bool, optional): Description
            is_valid (bool, optional): Description
        """
        self.timestamp = timestamp
        self.pitch = pitch 
        self.roll = roll
        self.throttle = throttle 
        self.yaw = yaw 
        self.switch1 = switch1 
        self.switch2 = switch2 
        self.switch3 = switch3 
        self.switch4 = switch4 
        self.switch5 = switch5
        self.switch6 = switch6 
        self.switch7 = switch7 
        self.switch8 = switch8 
        self.is_initialized = is_initialized
        self.is_valid = is_valid

class GeoPoint(MsgpackMixin):

    """Summary
    
    Attributes:
        altitude (float): Description
        latitude (float): Description
        longitude (float): Description
    """
    
    latitude = 0.0
    longitude = 0.0
    altitude = 0.0

class MultirotorState(MsgpackMixin):

    """Summary
    
    Attributes:
        collision (TYPE): Description
        gps_location (TYPE): Description
        kinematics_estimated (TYPE): Description
        landed_state (TYPE): Description
        rc_data (TYPE): Description
        timestamp (TYPE): Description
    """
    
    collision = CollisionInfo();
    kinematics_estimated = KinematicsState()
    gps_location = GeoPoint()
    timestamp = np.uint64(0)
    landed_state = LandedState.Landed
    rc_data = RCData()

class ProjectionMatrix(MsgpackMixin):

    """Summary
    
    Attributes:
        matrix (list): Description
    """
    
    matrix = []

class CameraInfo(MsgpackMixin):

    """Summary
    
    Attributes:
        fov (int): Description
        pose (TYPE): Description
        proj_mat (TYPE): Description
    """
    
    pose = Pose()
    fov = -1
    proj_mat = ProjectionMatrix()

class TrajectoryTrackerGains():

    """Summary
    
    Attributes:
        kd_along_track (TYPE): Description
        kd_cross_track (TYPE): Description
        kd_vel_along_track (TYPE): Description
        kd_vel_cross_track (TYPE): Description
        kd_vel_z (TYPE): Description
        kd_yaw (TYPE): Description
        kd_z_track (TYPE): Description
        kp_along_track (TYPE): Description
        kp_cross_track (TYPE): Description
        kp_vel_along_track (TYPE): Description
        kp_vel_cross_track (TYPE): Description
        kp_vel_z (TYPE): Description
        kp_yaw (TYPE): Description
        kp_z_track (TYPE): Description
    """
    
    def __init__(self,
                kp_cross_track = 7.5, 
                kd_cross_track = 0.0, 
                kp_vel_cross_track = 5.0, 
                kd_vel_cross_track = 0.0, 
                kp_along_track = 0.4, 
                kd_along_track = 0.0, 
                kp_vel_along_track = 0.04, 
                kd_vel_along_track = 0.0, 
                kp_z_track = 2.0, 
                kd_z_track = 0.0, 
                kp_vel_z = 0.4, 
                kd_vel_z = 0.0, 
                kp_yaw = 3.0, 
                kd_yaw = 0.1):
        """Summary
        
        Args:
            kp_cross_track (float, optional): Description
            kd_cross_track (float, optional): Description
            kp_vel_cross_track (float, optional): Description
            kd_vel_cross_track (float, optional): Description
            kp_along_track (float, optional): Description
            kd_along_track (float, optional): Description
            kp_vel_along_track (float, optional): Description
            kd_vel_along_track (float, optional): Description
            kp_z_track (float, optional): Description
            kd_z_track (float, optional): Description
            kp_vel_z (float, optional): Description
            kd_vel_z (float, optional): Description
            kp_yaw (float, optional): Description
            kd_yaw (float, optional): Description
        """
        self.kp_cross_track = kp_cross_track
        self.kd_cross_track = kd_cross_track
        self.kp_vel_cross_track = kp_vel_cross_track
        self.kd_vel_cross_track = kd_vel_cross_track
        self.kp_along_track = kp_along_track
        self.kd_along_track = kd_along_track
        self.kp_vel_along_track = kp_vel_along_track
        self.kd_vel_along_track = kd_vel_along_track
        self.kp_z_track = kp_z_track
        self.kd_z_track = kd_z_track
        self.kp_vel_z = kp_vel_z
        self.kd_vel_z = kd_vel_z
        self.kp_yaw = kp_yaw
        self.kd_yaw = kd_yaw

    def to_list(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return [self.kp_cross_track, self.kd_cross_track, self.kp_vel_cross_track, self.kd_vel_cross_track, 
                self.kp_along_track, self.kd_along_track, self.kp_vel_along_track, self.kd_vel_along_track, 
                self.kp_z_track, self.kd_z_track, self.kp_vel_z, self.kd_vel_z, self.kp_yaw, self.kd_yaw]