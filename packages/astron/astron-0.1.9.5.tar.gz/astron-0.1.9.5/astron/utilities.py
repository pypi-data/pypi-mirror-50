import numpy as np
import math
import os, sys
import pygame

def getModpath():
    
    np_path = pygame.__file__
    if os.path.isfile(np_path[:-19] + r'\astron\__init__.py'):
        return np_path[:-19] + r'\astron'
    else:
        modpath = os.path.abspath(os.path.split(sys.argv[0])[0])        
        return modpath

class Velocity:
    
    def __init__(self, x_vel, y_vel):
        
        self.x = x_vel
        self.y = y_vel
        self.vec = [self.x, self.y]
        self.rot_matrix = getRotMatrix(self.getTheta())
        self.mag = (self.x ** 2 + self.y ** 2) ** 0.5
        self.theta = self.getTheta()
    
    def getTheta(self):
        
        angle = angleBetween([1,0], self.vec)
        if self.y < 0:
            angle += np.pi
        
        return angle
    
    def __repr__(self):
        return str((self.x, self.y))

class Force:
    
    def __init__(self, x_vector, y_vector, mag):
        
        hyp = (x_vector ** 2 + y_vector ** 2) ** 0.5
        if hyp != 0.0:
            ratio = mag / hyp
        else:
            ratio = 0.0
            mag = 0.0
            
        self.x = x_vector * ratio
        self.y = y_vector * ratio
        self.mag = mag  
    
    def __repr__(self):  
         
        return str((self.x, self.y))      

class Momentum:
    
    def __init__(self, x_vel, y_vel, mass = 1):
        
        self.x = mass * x_vel
        self.y = mass * y_vel
    
    @classmethod
    def fromImpulse(cls, force = Force, duration = float):
        
        x = force.x * duration
        y = force.y * duration
        
        return cls(x, y)

    def __add__(self, new):
        
        self.x += new.x
        self.y += new.y
        
        return self 

    def __repr__(self):
        
        return str((self.x, self.y))
    
class Orbit:
    
    def __init__(self, a, b, center_x, center_y, progress = 0.0, CW = True, angular_step = 3.14/900):
        self.a = a
        self.b = b
        self.center_x = center_x
        self.center_y = center_y
        self.progress = progress
        self.cw = CW
        self.angular_step = angular_step % 2*np.pi 
        
    def x(self, progress):
        return self.a * np.cos(progress) + self.center_x
    
    def y(self, progress):
        return self.b * np.sin(progress) + self.center_y
    
    def nextPos(self, factor = 1.0):
        if self.cw:
            self.progress += self.angular_step * factor
        else:
            self.progress -= self.angular_step * factor
            
        return self.x(self.progress), self.y(self.progress)

    def resetPos(self):
        self.progress = 0
        return self.x(self.progress), self.y(self.progress)
 
def unit_vector(vector):
    
    """ Returns the unit vector of the vector.  """
    if np.linalg.norm(vector) > 0:
        return vector / np.linalg.norm(vector)
    else:
        return np.array([0.0, 0.0])
        
def getRotMatrix(theta):
    
    return [
        [math.cos(theta), -math.sin(theta)],
        [math.sin(theta), math.cos(theta)]
    ]

def angleBetween(v1, v2):
    """ Returns the angle in degrees between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))