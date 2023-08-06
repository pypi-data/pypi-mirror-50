# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
from pymp.utils.transforms import (Cyl2Rect, AffineRx, AffineRy, AffineRz, AffineTx, AffineTy, AffineTz)

class Cylinder(object):
    def __init__(self, radius, height, resolution):
        self._radius = float(radius)
        self._height = float(height)
        self._resolution = float(resolution)
        self.__transform_hist = []
        self.__set_base_coordinates()
        
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, value):
        self._radius = float(value)
        self.__set_base_coordinates()
        
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        self._height = float(value)
        self.__set_base_coordinates()
        
    @property
    def resolution(self):
        return self._resolution
    @resolution.setter
    def resolution(self, value):
        self._resolution = float(value)
        self.__set_base_coordinates()
        
    @property        
    def circumference(self):
        return 2 * np.pi * self.radius
    
    @property
    def arc_lengths(self):
        return np.arange(0, self.circumference, self.resolution)
    
    @property
    def thetas(self):
        return (self.arc_lengths / self.radius) #+ (2*np.pi) 
    
    @property
    def z(self):
        return np.arange(0, self.height, self.resolution)     
    
    @property
    def homogeneous_coordinates(self):
        return self.__coordinates.T[-1::-1,::]

    @property
    def cartesian_coordinates(self):
        return self.__coordinates[0:3, ::].T[-1::-1,::]

    @property
    def numpy_coordinates(self):
        return self.__coordinates[2::-1, ::].T[-1::-1,::]
    
    def __construct_cyl_coordinates(self):
        z = (self.z[::, None] + np.zeros_like(self.thetas)).flatten()
        t = (self.thetas + np.zeros_like(self.z[::, None])).flatten()
        r = (self.radius + np.zeros_like(z[::, None])).flatten()
        
        return np.vstack([r.ravel(), t.ravel(), z.ravel()])
    
    def __set_base_coordinates(self):
        cyl_coords = self.__construct_cyl_coordinates()
        
        self.__base_coordinates = Cyl2Rect(cyl_coords)
        self.__base_coordinates = np.vstack([self.__base_coordinates, np.ones_like(self.__base_coordinates[0])])
        
        self.__compute_final_coordinates()
        
    def __compute_final_coordinates(self):        
        if self.__transform_hist:
            T = None
            for t in self.__transform_hist:
                if T is None:
                    T = t
                else:
                    T = t * T
            self.__coordinates = T * self.__base_coordinates
        else:
            self.__coordinates = self.__base_coordinates.copy('A')
            
    def reset_coordinates(self):
        self.__transform_hist = []
        self.__compute_final_coordinates()
            
    def rotate_x(self, value, unit='deg'):
        self.__transform_hist.append(AffineRx(value, unit))
        self.__compute_final_coordinates()
        
    def rotate_y(self, value, unit='deg'):
        self.__transform_hist.append(AffineRy(value, unit))
        self.__compute_final_coordinates()
    
    def rotate_z(self, value, unit='deg'):
        self.__transform_hist.append(AffineRz(value, unit))
        self.__compute_final_coordinates()
        
    def translate_x(self, value):
        self.__transform_hist.append(AffineTx(value))
        self.__compute_final_coordinates()
        
    def translate_y(self, value):
        self.__transform_hist.append(AffineTy(value))
        self.__compute_final_coordinates()
        
    def translate_z(self, value):
        self.__transform_hist.append(AffineTz(value))
        self.__compute_final_coordinates()
        
    def show3d(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter3D(*self.__coordinates[0:3,::], s=200, c='r', marker='.')
        
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')

        plt.show()

if __name__ == '__main__':
    # Example usage to extract dose from a DICOM RT Plan and Dose file set
    # In this case we are using an NDRefFrame from the frames library to construct and tract the coordinates of the
    # dose grid and extract the dose values. The NDRefFrame uses trilinear interpolation to determine the dose value at
    # each point on the cylinder's surface

    import numpy as np
    import pydicom                              # Python DICOM Library
    from pymp.frames import NDRefFrame  # numpy.ndarray subclass that constructs and tracks coordinate frames

    # Create a cylinder model the size of the ArcCheck at 1mm resolution
    #
    # Cylinder(radius, height, resolution)
    cylinder  = Cylinder(105, 220, 1)
    cylinder.rotate_z(-90)
    cylinder.translate_z(-110)

    # Open the DICOM RT Plan file and grab the isocenter coordinate
    plan = pydicom.read_file('plan.dcm')
    isocenter = np.array(plan.BeamSequence[0].ControlPointSequence[0].IsocenterPosition, dtype=np.float)
    print(isocenter)

    # Open the DICOM RT Dose file
    dose = pydicom.read_file('dose.dcm')

    # Extract and scale the dose values by the DoseGridScaling value
    #
    # dose.DoseGridScaling - Scaling factor that when multiplied by the dose grid data found in Pixel Data (7FE0,0010)
    # Attribute of the Image Pixel Module, yields grid doses in the dose units as specified by Dose Units (3004,0002).
    dose_grid = NDRefFrame(dose.pixel_array * float(dose.DoseGridScaling))

    # Convert to cGy if the DoseUnits are in Gy
    dose_grid *= 100 if dose.DoseUnits == 'GY' else 1

    # Grab the upper left corner position for the dose grid to set the coordinate mappers
    #
    # dose.ImagePositionPatient - Found in (0020,0032) specifies the x, y, and z coordinates of the upper left hand
    # corner of the image; it is the center of the first voxel transmitted.
    position = np.array(dose.ImagePositionPatient, dtype=np.float)

    # Grab the pixel spacing for the dose grid planes
    #
    # dose.PixelSpacing - Physical distance in the patient between the center of each pixel, specified by a numeric
    # pair - adjacent row spacing (delimiter) adjacent column spacing in mm.
    spacing = np.array(dose.PixelSpacing, dtype=np.float)

    # Grad the 'Z' position of the first dose plane (upper right corner) and the dose plane spacing
    #
    # dose.GridFrameOffsetVector - Grid Frame Offset Vector (3004,000C) shall be provided if a dose distribution is
    # encoded as a multi-frame image. Values of the Grid Frame Offset Vector (3004,000C) shall vary monotonically and
    # are to be interpreted as follows:
    #
    #   a)  If Grid Frame Offset Vector (3004,000C) is present and its first element is zero, this Attribute contains an
    #       array of n elements indicating the plane location of the data in the right-handed image coordinate system,
    #       relative to the position of the first dose plane transmitted, i.e., the point at which Image Position
    #       (patient) (0020,0032) is defined, with positive offsets in the direction of the cross product of the row and
    #       column directions.
    #
    #   b)  If Grid Frame Offset Vector (3004,000C) is present, its first element is equal to the third element of
    #       Image Position (patient) (0020,0032), and Image Orientation (patient) (0020,0037) has the value
    #       (1,0,0,0,1,0), then Grid Frame Offset Vector contains an array of n elements indicating the plane location
    #       (patient z coordinate) of the data in the Patient-Based Coordinate System.
    #
    # Option (a) can represent a rectangular-parallelepiped dose grid with any orientation with respect to the patient,
    # while option (b) can only represent a rectangular-parallelepiped dose grid whose planes are in the transverse
    # patient dimension and whose x- and y-axes are parallel to the patient x- and y-axes.
    #
    # For this case we really only care about the spacing of the "Z" planes since the NDRefFrame will handle the
    # construction of the coordinate frames from the position and spacing using its LinearMappers. We don't really care
    # if the coordinates in the file are relative (option a) or absolute (option b)
    gfov = np.array(dose.GridFrameOffsetVector, dtype=np.float)

    z_spacing = gfov[1:] - gfov[0:-1]
    if not np.all(z_spacing == z_spacing[0]):
        print(z_spacing)
        raise ValueError("Grid Frame Offset Vector spacing is not uniform")

    # Check image orientation just to be safe
    orientation = np.array(dose.ImageOrientationPatient, dtype=np.int)
    if not np.all(orientation == np.array([1, 0, 0, 0, 1, 0], dtype=np.int)):
        print(orientation, np.array([1, 0, 0, 0, 1, 0], dtype=np.int))
        raise ValueError('Image orientation is not a standard orientation')

    spacing = np.hstack((spacing, np.array([z_spacing[0]])))

    # Set the position, spacing, and origin of the dose_grid NDRefFrame so that the dose grid coordinates are centered
    # around the isocenter. This makes the coordinate of isocenter (0, 0, 0)
    #
    # The coordinates from the DICOM RT files are in (X, Y, Z) format and the NDRefFrame coordinates are in numpy
    # orientation (Z, Y, X) so the DICOM coordinates have to be reversed hence the [-1::-1] indexing.
    dose_grid.position = position[-1::-1]
    dose_grid.spacing = spacing[-1::-1]
    dose_grid.origin = isocenter[-1::-1]