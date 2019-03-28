# Camera Calibration
Practice how to implement camera calibration.

## Introduction

### 1. Coordinate System
We could divide coordinate into four kinds, World, Camera, Fil, and Pixel coordinates.

World Coordinates   |   Camera Coordinates  |   Film Coordinates    |   Pixel Coordinates
:------------------:|:---------------------:|:---------------------:| :------------------:
U                   |           X           |           x           |           u
V                   |           Y           |           y           |           v
W                   |           Z           |                       |                       

Between Camera Coordinates and Film Coordinates, there is a relationship that:

 ![equation_A](https://latex.codecogs.com/svg.latex?x%20%3D%20%5Cboldsymbol%7Bf%7D%5Cfrac%7BX%7D%7BZ%7D%20%2C%20y%20%3D%20%5Cboldsymbol%7Bf%7D%5Cfrac%7BY%7D%7BZ%7D%20%5Cleftrightarrow%20%5Cbegin%7Bbmatrix%7D%20x%27%5C%5C%20y%27%5C%5C%20z%27%20%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bf%7D%26%200%20%26%200%20%26%200%5C%5C%200%26%20%5Cboldsymbol%7Bf%7D%26%200%20%26%200%5C%5C%200%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D)

Between World Coordinates and Camera Coordinates, there is a relationship that:

![equation_B](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20r_%7B11%7D%20%26%20r_%7B12%7D%20%26%20r_%7B13%7D%20%26%200%5C%5C%20r_%7B21%7D%20%26%20r_%7B22%7D%20%26%20r_%7B23%7D%20%26%200%5C%5C%20r_%7B31%7D%20%26%20r_%7B32%7D%20%26%20r_%7B33%7D%20%26%200%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%201%20%26%200%20%26%200%20%26%20-c_%7Bx%7D%5C%5C%200%20%26%201%20%26%200%20%26%20-c_%7By%7D%5C%5C%200%20%26%200%20%26%201%20%26%20-c_%7Bz%7D%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20U%5C%5C%20V%5C%5C%20W%5C%5C%201%20%5Cend%7Bbmatrix%7D)

![equation_B1](https://latex.codecogs.com/svg.latex?%5Cleft%20%28R_%7Bx%7D%28%5Calpha%20%29%3D%5Cbegin%7Bbmatrix%7D%201%20%26%200%20%26%200%5C%5C%200%20%26%20%5Ccos%28%5Calpha%29%20%26%20-%5Csin%28%5Calpha%29%5C%5C%200%20%26%20%5Csin%28%5Calpha%29%20%26%20%5Ccos%28%5Calpha%29%20%5Cend%7Bbmatrix%7D%2C%20R_%7By%7D%28%5Cbeta%29%3D%5Cbegin%7Bbmatrix%7D%20%5Ccos%28%5Cbeta%29%20%26%200%20%26%20%5Csin%28%5Cbeta%29%5C%5C%200%20%26%201%20%26%200%5C%5C%20-%5Csin%28%5Cbeta%29%20%26%200%20%26%20%5Ccos%28%5Cbeta%29%20%5Cend%7Bbmatrix%7D%2C%20R_%7Bz%7D%28%5Cgamma%29%3D%5Cbegin%7Bbmatrix%7D%20%5Ccos%28%5Cgamma%29%20%26%20-%5Csin%28%5Cgamma%29%20%26%200%5C%5C%20%5Csin%28%5Cgamma%29%20%26%20%5Ccos%28%5Cgamma%29%20%26%200%5C%5C%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cright%20%29)

![equation_B2](https://latex.codecogs.com/svg.latex?%5CRightarrow%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20r_%7B11%7D%20%26%20r_%7B12%7D%20%26%20r_%7B13%7D%20%26%20t_%7Bx%7D%5C%5C%20r_%7B21%7D%20%26%20r_%7B22%7D%20%26%20r_%7B23%7D%20%26%20t_%7By%7D%5C%5C%20r_%7B31%7D%20%26%20r_%7B32%7D%20%26%20r_%7B33%7D%20%26%20t_%7Bz%7D%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20U%5C%5C%20V%5C%5C%20W%5C%5C%201%20%5Cend%7Bbmatrix%7D)

Between Film Coordinates and Pixel Coordinates, there is a relationship that:

![equation_C](https://latex.codecogs.com/svg.latex?u%3D%5Cboldsymbol%7Bf%7D%5Cfrac%7BX%7D%7BZ%7D&plus;o_%7Bx%7D%2C%20v%3D%5Cboldsymbol%7Bf%7D%5Cfrac%7BY%7D%7BZ%7D&plus;o_%7By%7D%5Crightarrow%20u%3D%5Cfrac%7B1%7D%7Bs_%7Bx%7D%7D%5Cboldsymbol%7Bf%7D%5Cfrac%7BX%7D%7BZ%7D&plus;o_%7Bx%7D%2C%20v%3D%5Cfrac%7B1%7D%7Bs_%7By%7D%7D%5Cboldsymbol%7Bf%7D%5Cfrac%7BY%7D%7BZ%7D&plus;o_%7By%7D)

![equation_C1](https://latex.codecogs.com/svg.latex?%5CRightarrow%20%5Cbegin%7Bbmatrix%7D%20x%27%5C%5C%20y%27%5C%5C%20z%27%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7Bx%7D%7D%20%26%200%20%26%20o_%7Bx%7D%20%26%200%5C%5C%200%20%26%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7By%7D%7D%20%26%20o_%7By%7D%20%26%200%5C%5C%200%20%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D%5Crightarrow%20u%3D%5Cfrac%7Bx%27%7D%7Bz%27%7D%2C%20v%3D%5Cfrac%7By%27%7D%7Bz%27%7D)

some skew effect would happen

![equation_C2](https://latex.codecogs.com/svg.latex?%5CRightarrow%20%5Cbegin%7Bbmatrix%7D%20x%27%5C%5C%20y%27%5C%5C%20z%27%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7Bx%7D%7D%20%26%20s_%7Bk%7D%20%26%20o_%7Bx%7D%20%26%200%5C%5C%200%20%26%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7By%7D%7D%20%26%20o_%7By%7D%20%26%200%5C%5C%200%20%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D)

![equation_C3](https://latex.codecogs.com/svg.latex?%5CRightarrow%20%5Cbegin%7Bbmatrix%7D%20u%27%5C%5C%20v%27%5C%5C%20w%27%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20a_%7B11%7D%20%26%20a_%7B12%7D%20%26%20a_%7B13%7D%5C%5C%20a_%7B21%7D%20%26%20a_%7B22%7D%20%26%20a_%7B23%7D%5C%5C%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bf%7D%20%26%200%20%26%200%20%26%200%5C%5C%200%20%26%20%5Cboldsymbol%7Bf%7D%20%26%200%20%26%200%5C%5C%200%20%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D%5Crightarrow%20u%3DM_%7Bint%7DP_%7Bc%7D%3DM_%7Baff%7DM_%7Bproj%7DP_%7Bc%7D)

### Summary

World Coordinates   |  |   Camera Coordinates  |  |   Film Coordinates    |  |   Pixel Coordinates
:------------------:|--|:---------------------:|--|:---------------------:|--|:------------------:
U                   |  |           X           |  |           x           |  |           u
V                   | ![equation_D](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM_%7Bext%7D%7D%7B%5CRightarrow%7D) |           Y           | ![equation](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM_%7Bproj%7D%7D%7B%5CRightarrow%7D) |           y           | ![equation](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM_%7Baff%7D%7D%7B%5CRightarrow%7D) |           v
W                   |  |           Z           |  |                       |  |   

![equation](https://latex.codecogs.com/svg.latex?%5Cleft%20%28%20M_%7Bext%7D%3D%20%5Cbegin%7Bbmatrix%7D%20r_%7B11%7D%20%26%20r_%7B12%7D%20%26%20r_%7B13%7D%20%26%20t_%7Bx%7D%5C%5C%20r_%7B21%7D%20%26%20r_%7B22%7D%20%26%20r_%7B23%7D%20%26%20t_%7By%7D%5C%5C%20r_%7B31%7D%20%26%20r_%7B32%7D%20%26%20r_%7B33%7D%20%26%20t_%7Bz%7D%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%2C%20M_%7Bproj%7D%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cboldsymbol%7Bf%7D%20%26%200%20%26%200%20%26%200%5C%5C%200%20%26%20%5Cboldsymbol%7Bf%7D%20%26%200%20%26%200%5C%5C%200%20%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D%2C%20M_%7Baff%7D%20%5Cbegin%7Bbmatrix%7D%20a_%7B11%7D%20%26%20a_%7B12%7D%20%26%20a_%7B13%7D%5C%5C%20a_%7B21%7D%20%26%20a_%7B22%7D%20%26%20a_%7B23%7D%5C%5C%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cright%20%29)

World Coordinates   |  |   Camera Coordinates  |   Film Coordinates    |   Pixel Coordinates
:------------------:|--|:---------------------:|:---------------------:|:------------------:
U                   |  |          X            |                       |          u
V                   | ![equation_D](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM_%7Bext%7D%7D%7B%5CRightarrow%7D) |          Y            | ![equation](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM_%7Bint%7D%7D%7B%5CRightarrow%7D) |          v
W                   |  |          Z            |                       |

World Coordinates   |   Camera Coordinates  |   Film Coordinates    |   Pixel Coordinates
:------------------:|:---------------------:|:---------------------:|:------------------:
U                   |                       |                       |          u
V                   |                       |     ![equation](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM%7D%7B%5CRightarrow%7D)                  |          v
W                   |                       |                       |

![equation](https://latex.codecogs.com/svg.latex?%5Cleft%20%28%20M%3D%20%5Cbegin%7Bbmatrix%7D%20m_%7B11%7D%20%26%20m_%7B12%7D%20%26%20m_%7B13%7D%20%26%20m_%7B14%7D%5C%5C%20m_%7B21%7D%20%26%20m_%7B22%7D%20%26%20m_%7B23%7D%20%26%20m_%7B24%7D%5C%5C%20m_%7B31%7D%20%26%20m_%7B32%7D%20%26%20m_%7B33%7D%20%26%20m_%7B34%7D%20%5Cend%7Bbmatrix%7D%20%5Cright%20%29)

From above relations of each coordinate, we could get:

![equation_E1](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20r_%7B11%7D%20%26%20r_%7B12%7D%20%26%20r_%7B13%7D%20%26%200%5C%5C%20r_%7B21%7D%20%26%20r_%7B22%7D%20%26%20r_%7B23%7D%20%26%200%5C%5C%20r_%7B31%7D%20%26%20r_%7B32%7D%20%26%20r_%7B33%7D%20%26%200%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%201%20%26%200%20%26%200%20%26%20-c_%7Bx%7D%5C%5C%200%20%26%201%20%26%200%20%26%20-c_%7By%7D%5C%5C%200%20%26%200%20%26%201%20%26%20-c_%7Bz%7D%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20U%5C%5C%20V%5C%5C%20W%5C%5C%201%20%5Cend%7Bbmatrix%7D)

![euqation_E2](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20x%27%5C%5C%20y%27%5C%5C%20z%27%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7Bx%7D%7D%20%26%20s_%7Bk%7D%20%26%20o_%7Bx%7D%20%26%200%5C%5C%200%20%26%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7By%7D%7D%20%26%20o_%7By%7D%20%26%200%5C%5C%200%20%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D)

![equation_E3](https://latex.codecogs.com/svg.latex?%5CRightarrow%20x%3DK%5Cbegin%7Bbmatrix%7D%20R%20%26%20r%20%5Cend%7Bbmatrix%7DX)

### 2. Camera Calibration

In the 3D coordinate and in the image coordinate, we could find a pair of points. We suppose it as P and p.

![equation_F1](https://latex.codecogs.com/svg.latex?P_%7Bi%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20X_%7Bi%7D%5C%5C%20Y_%7Bi%7D%5C%5C%20Z_%7Bi%7D%5C%5C%201%20%5Cend%7Bbmatrix%7D%2C%20p_%7Bi%7D%3D%5Cbegin%7Bbmatrix%7D%20u_%7Bi%7D%5C%5C%20v_%7Bi%7D%20%5Cend%7Bbmatrix%7D)

From the above summary, we know that:
![equation_F2](https://latex.codecogs.com/svg.latex?p_%7Bi%7D%3D%5Cbegin%7Bbmatrix%7D%20u_%7Bi%7D%5C%5C%20v_%7Bi%7D%20%5Cend%7Bbmatrix%7D%3DMP_%7Bi%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cfrac%7Bm_%7B1%7DP_%7Bi%7D%7D%7Bm_%7B3%7DP_%7Bi%7D%7D%5C%5C%20%5Cfrac%7Bm_%7B2%7DP_%7Bi%7D%7D%7Bm_%7B3%7DP_%7Bi%7D%7D%20%5Cend%7Bbmatrix%7D%20%5Crightarrow%20%5Cbegin%7Bmatrix%7D%20u_%7Bi%7D%5Cleft%20%28%20m_%7B3%7DP_%7Bi%7D%20%5Cright%20%29-m_%7B1%7DP_%7Bi%7D%3D0%5C%5C%20v_%7Bi%7D%5Cleft%20%28%20m_%7B3%7DP_%7Bi%7D%20%5Cright%20%29-m_%7B2%7DP_%7Bi%7D%3D0%20%5Cend%7Bmatrix%7D%20%5Crightarrow%20%5Cbegin%7Bmatrix%7D%20u_%7B1%7D%5Cleft%20%28%20m_%7B3%7DP_%7B1%7D%20%5Cright%20%29-m_%7B1%7DP_%7B1%7D%3D0%5C%5C%20v_%7B1%7D%5Cleft%20%28%20m_%7B3%7DP_%7B1%7D%20%5Cright%20%29-m_%7B2%7DP_%7B1%7D%3D0%5C%5C%20...%5C%5C%20u_%7Bn%7D%5Cleft%20%28%20m_%7B3%7DP_%7Bn%7D%20%5Cright%20%29-m_%7B1%7DP_%7Bn%7D%3D0%5C%5C%20v_%7Bn%7D%5Cleft%20%28%20m_%7B3%7DP_%7Bn%7D%20%5Cright%20%29-m_%7B2%7DP_%7Bn%7D%3D0%20%5Cend%7Bmatrix%7D)

So we could know each correspondence gives 2 equations, while M has 11 DoF, so we need at least 6 correspondences, however, we often use more as measurement are often noisy.

![equation_F3](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20P_%7B1%7D%5E%7BT%7D%20%26%200%5E%7BT%7D%20%26%20-u_%7B1%7DP_%7B1%7D%5E%7BT%7D%5C%5C%200%5E%7BT%7D%20%26%20P_%7B1%7D%5E%7BT%7D%20%26%20-v_%7B1%7DP_%7B1%7D%5E%7BT%7D%5C%5C%20...%20%26%20...%20%26%20...%5C%5C%20P_%7Bn%7D%5E%7BT%7D%20%26%200%5E%7BT%7D%20%26%20-u_%7Bn%7DP_%7Bn%7D%5E%7BT%7D%5C%5C%200%5E%7BT%7D%20%26%20P_%7Bn%7D%5E%7BT%7D%20%26%20-v_%7Bn%7DP_%7Bn%7D%5E%7BT%7D%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20m_%7B1%7D%5E%7BT%7D%5C%5C%20m_%7B2%7D%5E%7BT%7D%5C%5C%20m_%7B3%7D%5E%7BT%7D%20%5Cend%7Bbmatrix%7D%3DPm%3D0)

we could use SVD to solve m: 

![equation_F4](https://latex.codecogs.com/svg.latex?P%3DUDV%5E%7BT%7D%5Crightarrow%20M%3DK%5Cbegin%7Bbmatrix%7D%20R%20%26%20t%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20KR%20%26%20KRT%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20C%20%26%20CT%20%5Cend%7Bbmatrix%7D)

where K is upper triangular matrix, R is orthogonol matrix, we could use RQ decomposition to get K(intrinsic) and R(rotation), and then get T(translation) by multiplying C's inverse to CT.

## Implementation Proedure

Because 3D calibration rig is hard to make, so we use a 2D pattern(e.g. a chessboard) to implement.
> Hint. set the World Corrdinate system to the corner of chessboard, and all points on the chessboard line in one plane.

### 1. Find the Homography matrix

Using the world coordinate and pattern coordinate to find the H:

![equation_G1](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20x%27%5C%5C%20y%27%5C%5C%20z%27%20%5Cend%7Bbmatrix%7D%3D%5Crho%20H%20%5Cbegin%7Bbmatrix%7D%20U%5C%5C%20V%5C%5C%201%20%5Cend%7Bbmatrix%7D%2C%20%5Cbegin%7Bmatrix%7D%20u%3D%5Cfrac%7Bx%27%7D%7Bz%27%7D%5C%5C%20v%3D%5Cfrac%7By%27%7D%7Bz%27%7D%20%5Cend%7Bmatrix%7D)

Because chessboard is a 2D pattern, we cound think all points in the pattern don't have z-axis value. Then, H matrix is a 3x3 matrix:

![H](https://latex.codecogs.com/svg.latex?H%3D%5Cbegin%7Bbmatrix%7D%20h_%7B11%7D%20%26%20h_%7B12%7D%20%26%20h_%7B13%7D%5C%5C%20h_%7B21%7D%20%26%20h_%7B22%7D%20%26%20h_%7B23%7D%5C%5C%20h_%7B31%7D%20%26%20h_%7B32%7D%20%26%20h_%7B33%7D%20%5Cend%7Bbmatrix%7D)
, ![equation_G2](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20u%5C%5C%20v%5C%5C%201%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20h_%7B11%7D%20%26%20h_%7B12%7D%20%26%20h_%7B13%7D%5C%5C%20h_%7B21%7D%20%26%20h_%7B22%7D%20%26%20h_%7B23%7D%5C%5C%20h_%7B31%7D%20%26%20h_%7B32%7D%20%26%20h_%7B33%7D%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20U%5C%5C%20V%5C%5C%201%20%5Cend%7Bbmatrix%7D)

![equation_G3](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bmatrix%7D%20%5Cleft%20%28%20h_%7B11%7DU&plus;h_%7B12%7DV&plus;h_%7B13%7D%20%5Cright%20%29-u%5Cleft%20%28%20h_%7B31%7D&plus;h_%7B32%7D&plus;h_%7B33%7D%20%5Cright%20%29%3D0%5C%5C%20%5Cleft%20%28%20h_%7B21%7DU&plus;h_%7B22%7DV&plus;h_%7B23%7D%20%5Cright%20%29-u%5Cleft%20%28%20h_%7B31%7D&plus;h_%7B32%7D&plus;h_%7B33%7D%20%5Cright%20%29%3D0%20%5Cend%7Bmatrix%7D)

we could rewrite it into matrix:

![equation_G4](https://latex.codecogs.com/svg.latex?%5Cinline%20%5Cbegin%7Bbmatrix%7D%20U_%7B0%7D%20%26%20V_%7B0%7D%20%26%201%20%26%200%20%26%200%20%26%200%20%26%20-u_%7B0%7DU_%7B0%7D%20%26%20-u_%7B0%7DV_%7B0%7D%20%26%20-u_%7B0%7D%5C%5C%200%20%26%200%20%26%200%20%26%20U_%7B0%7D%20%26%20V_%7B0%7D%20%26%201%20%26%20-v_%7B0%7DU_%7B0%7D%20%26%20-v_%7B0%7DV_%7B0%7D%20%26%20-v_%7B0%7D%5C%5C%20...%20%26%20...%20%26%20...%20%26%20...%20%26%20...%20%26%20...%20%26%20...%20%26%20...%20%26%20...%5C%5C%20U_%7Bn-1%7D%20%26%20V_%7Bn-1%7D%20%26%201%20%26%200%20%26%200%20%26%200%20%26%20-u_%7Bn-1%7DU_%7Bn-1%7D%20%26%20-u_%7Bn-1%7DV_%7Bn-1%7D%20%26%20-u_%7Bn-1%7D%5C%5C%200%20%26%200%20%26%200%20%26%20U_%7Bn-1%7D%20%26%20V_%7Bn-1%7D%20%26%201%20%26%20-v_%7Bn-1%7DU_%7Bn-1%7D%20%26%20-v_%7Bn-1%7DV_%7Bn-1%7D%20%26%20-v_%7Bn-1%7D%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20h_%7B11%7D%5C%5C%20h_%7B12%7D%5C%5C%20h_%7B13%7D%5C%5C%20h_%7B21%7D%5C%5C%20h_%7B22%7D%5C%5C%20h_%7B23%7D%5C%5C%20h_%7B31%7D%5C%5C%20h_%7B32%7D%5C%5C%20h_%7B33%7D%20%5Cend%7Bbmatrix%7D)

* In the implementation, we should use the points in the pattern and its correapondence in the world coordinate to produce the matrix P.
* Using SVD to solve Ph=0 equation to figure out the h, which is 9x1 matrix. In SVD solution, the last column of V's transpose matrix is the answer.
* Reconstructing the h into H, which is 3x3 matrix.
* Because P(h) equal to zero, P(-h) will equal to zero too, we always set the last element positive.

### 2. Find the symmetric positive definite matrix

Using the homography matrix to find out the b:

![equation_G5](https://latex.codecogs.com/svg.latex?%5Cinline%20%5Cbegin%7Bmatrix%7D%20h_%7B1%7D%5E%7BT%7DBh_%7B2%7D%3D0%5C%5C%20h_%7B1%7D%5E%7BT%7DBh_%7B1%7D%3Dh_%7B2%7D%5E%7BT%7DBh_%7B2%7D%20%5Cend%7Bmatrix%7D)

From these two equations, we could get:

![equation_G6](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20h_%7B11%7Dh_%7B12%7D%20%26%20h_%7B12%7Dh_%7B21%7D&plus;h_%7B11%7Dh_%7B22%7D%20%26%20h_%7B12%7Dh_%7B31%7D&plus;h_%7B11%7Dh_%7B32%7D%20%26%20h_%7B21%7Dh_%7B22%7D%20%26%20h_%7B22%7Dh_%7B31%7D&plus;h_%7B21%7Dh_%7B32%7D%20%26%20h_%7B31%7Dh_%7B32%7D%5C%5C%20h_%7B11%7D%5E%7B2%7D-h_%7B12%7D%5E%7B2%7D%20%26%202h_%7B11%7Dh_%7B21%7D-2h_%7B12%7Dh_%7B22%7D%20%26%202h_%7B11%7Dh_%7B31%7D-2h_%7B12%7Dh_%7B32%7D%20%26%20h_%7B21%7D%5E%7B2%7D-h_%7B22%7D%5E%7B2%7D%20%26%202h_%7B21%7Dh_%7B31%7D-2h_%7B22%7Dh_%7B32%7D%20%26%20h_%7B31%7D%5E%7B2%7D-h_%7B32%7D%5E%7B2%7D%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20b_%7B11%7D%5C%5C%20b_%7B12%7D%5C%5C%20b_%7B13%7D%5C%5C%20b_%7B22%7D%5C%5C%20b_%7B23%7D%5C%5C%20b_%7B33%7D%20%5Cend%7Bbmatrix%7D)

* Using previous homography matrix to combine the V matrix, which is 2x6 matrix.
* Using SVD to solve Vb=0 equation to figure out the b.
* Recontructing the b into B, which is 3x3 symmetric positive definite matrix.
* Because V(b) equal to zero, V(-b) will equal to zero too, we always set the last element positive.

### 3. Get the intrinsic matrix

![equation_H1](https://latex.codecogs.com/svg.latex?B%3D%5Cleft%20%28%20K%5E%7BT%7D%20%5Cright%20%29%5E%7B-1%7DK%5E%7B-1%7D)

* Using Cholesky Decomposition to solve out K.
* K is an upper triangular matrix and its inverse is also an upper triangular matrix, so B is a lower triangular matrix multiply to upper triangular matrix, then we could use Cholesky Decomposition to get the inv(K), and do the inverse to find out the K.

### 4. Get the extrinsic matrix

![equation_I1](https://latex.codecogs.com/svg.latex?H%3D%5Cbegin%7Bbmatrix%7D%20h_%7B1%7D%20%26%20h_%7B2%7D%20%26%20h_%7B3%7D%20%5Cend%7Bbmatrix%7D%20%5Crightarrow%20%5Cbegin%7Bmatrix%7D%20%5Clambda%20%3D%5Cfrac%7B1%7D%7B%5Cleft%20%5C%7C%20K%5E%7B-1%7Dh_%7B1%7D%20%5Cright%20%5C%7C%7D%5C%5C%20r_%7B1%7D%3D%5Clambda%20K%5E%7B-1%7Dh_%7B1%7D%5C%5C%20r_%7B2%7D%3D%5Clambda%20K%5E%7B-1%7Dh_%7B2%7D%5C%5C%20r_%7B3%7D%3Dr_%7B1%7D%5Ctimes%20r_%7B2%7D%5C%5C%20t%3D%5Clambda%20K%5E%7B-1%7Dh_%7B3%7D%20%5Cend%7Bmatrix%7D)

* Using the equations above to get the translation and rotation matrix, then the rotation matrix need to use the Rodrigues function to get its rotation vector.
* The images of chessboard will not always in same orientation, so we should remember its original homography matrix and use its rotated image to calculate the right intrinsic matrix.

## Experimental Result

The intrinsic matrix of using opencv library and implementing myself.

![equation_J1](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bmatrix%7D%20K%5Cleft%20%28%20opencv%20%5Cright%20%29%3D%20%5Cbegin%7Bbmatrix%7D%203.17677524%5Ctimes%2010%5E%7B3%7D%20%26%200%20%26%201.64148716%5Ctimes%2010%5E%7B3%7D%5C%5C%200%20%26%203.19706975%5Ctimes%2010%5E%7B3%7D%20%26%201.43116675%5Ctimes%2010%5E%7B3%7D%5C%5C%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%5C%5C%20%5C%5C%20K%5Cleft%20%28%20ours%20%5Cright%20%29%3D%20%5Cbegin%7Bbmatrix%7D%202.98653567%5Ctimes%2010%5E%7B3%7D%20%26%20-1.69915365%20%26%201.46421577%5Ctimes%2010%5E%7B3%7D%5C%5C%200%20%26%202.99318403%5Ctimes%2010%5E%7B3%7D%20%26%201.95176612%5Ctimes%2010%5E%7B3%7D%5C%5C%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cend%7Bmatrix%7D)

We could see the results of these two intrinsic matrixs are very similar.

And the extrinsic results are:

OpenCV                      |       Ours 
:--------------------------:|:----------------------------:
![OpenCV](./img/sample.png) |![Ours](./img/implement.png)
