# 1. Image processing
1. Load file \
   Using **pywavefront** package read cloud points to scan\_obj

1. Scale image\
   Scale unit length to 1 mm(coordinate 1000x)

1. Remove Background \
   Find plane using RANSAC(open3D segment_plane)\
   plane function: ax + by + cz + d = 0 

1. Remove noise points \
   (open3D remove_statistical_outlier)

1.  Project points to plane \
    project 3D points to the ground plane(plane function in step 3)

1. Change axis with PCA, 3D points to 2D points

1. Get alpha shape \
   Alpha shapes are often used to generalize bounding polygons containing sets of points.
   For different type of bone, the position are different
   1. Radius and tibia: need bigger end positioned on the left
   1. Both femur and humerus need put "head" to right-bottom corner
  
# 2. Some util functions
1. Divide a bone to several regions, we use a rectangle to intersect with the original alpha shape
    get_left_region(alpha_shape)\
    get_center_region(alpha_shape)\
    get_right_region(alpha_shape)
1. Least squares polynomial fit.\
    Fit a polynomial p(x) = p[0] * x**deg + ... + p[deg] of degree deg to points\
    def fit_line(points_array, show_figure):
 
      
# 2. Measurements
## 2.1 Femur
### FML (Femur Maximum Length)
Difference between maximum x-coordinate and minimum x-coordinate of the whole bone

## FEB(Femur Epidondylar Breadth)
Difference between maximum y-coordinate and minimum y-coordinate of the left region(get_center_region in utils)

### FBML(Femur Bicondylar Length) **--Different algorithm**
1. find two POI in the left region
    1. left most point is defined as P1
    1. second left most point,  apart from P1 across the gap, is defined as P2
    1. line1 is defined by P1 and P2
1. iterate points in head region, namely P3, find the largest distance between P3 and line1

## FMLD (Femur Mediolateral Diameter)
1. fit upper and bottom lines in center region(use get_center_region in utils) with 2-degree
1. find the minimum distance between these two lines 

## FHD (Femur Head Diameter)



# Radius
## RML (Radius Maximum Length)
## RMLD(Radius Mediolateral Diameter)

# Humerus
## HHD (Humerus Head Diameter)
## HEB(Humerus Epicondylar Breadth)
## HML (Humerus Maximum Length)

# Tibia
## TML (Tibia Maximum Length)
## TPN(Tibia Plateau Mediolateral Breadth)