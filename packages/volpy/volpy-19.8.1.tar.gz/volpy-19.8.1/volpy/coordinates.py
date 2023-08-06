# Defines the different types of coordinates that application can work with
import numpy as np
import utm
from enum import Enum

class CoordinateSystem(Enum):
    GEOGRAPHIC = 0
    UTM = 1
    CARTESIAN = 2

class GeographicCoordinate():
    def __init__(self, latitude, longitude, elevation):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation # above sea level

class UtmCoordinate():
    def __init__(self, northing, easting, zone_number, zone_letter, elevation):
        self.northing = northing
        self.easting = easting
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.elevation = elevation

    @classmethod
    def create_from_geographic(cls, latitude, longitude, elevation):
        """ creates an instance in UTM from a geographic coordinate"""
        (northing, easting, zone_number, zone_letter) = utm.from_latlon(
            latitude,
            longitude)
        return cls(northing, easting, zone_number, zone_letter, elevation)

class CartesianCoordinate():
    """
    Classical cartesian coordinate system with x, y, z axes.
    """
    def __init__(self, x: np.float64, y: np.float64, z: np.float64):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return 'point: {0}, {1}, {2}'.format(self.x, self.y, self.z)

    def __sub__(self, other):
        """
        Returns the difference between 2 points in a cartesian plane.
        It is used to create a vector out of 2 points in 3D space.
        """
        minuend = np.array([self.x, self.y, self.z])
        subtrahend = np.array([other.x, other.y, other.z])
        return minuend - subtrahend

    def __lt__(self, other):
        """Comparison override used to sort points in function of their x
        coordinate. This was done so because of the order the double integral
        is applied when calculating the volume casted by an ABC traingle 
        (defined by a set of 3 Cartesian Coordinates)
        """
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
        
