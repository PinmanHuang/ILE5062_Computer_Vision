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

World Coordinates   |  |   Camera Coordinates  |  |   Film Coordinates    |  |   Pixel Coordinates
:------------------:|--|:---------------------:|--|:---------------------:|--|:------------------:
U                   |  |          X            |  |                       |  |          u
V                   | ![equation_D](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM_%7Bext%7D%7D%7B%5CRightarrow%7D) |          Y            |  | ![equation](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM_%7Bint%7D%7D%7B%5CRightarrow%7D) |  |          v
W                   |  |          Z            |  |                       |  |

World Coordinates   |  |   Camera Coordinates  |  |   Film Coordinates    |  |   Pixel Coordinates
:------------------:|--|:---------------------:|--|:---------------------:|--|:------------------:
U                   |  |                       |  |                       |  |          u
V                   |  |                       |  |     ![equation](https://latex.codecogs.com/svg.latex?%5CLARGE%20%5Coverset%7BM%7D%7B%5CRightarrow%7D)                  |  |          v
W                   |  |                       |  |                       |  |

![equation](https://latex.codecogs.com/svg.latex?%5Cleft%20%28%20M%3D%20%5Cbegin%7Bbmatrix%7D%20m_%7B11%7D%20%26%20m_%7B12%7D%20%26%20m_%7B13%7D%20%26%20m_%7B14%7D%5C%5C%20m_%7B21%7D%20%26%20m_%7B22%7D%20%26%20m_%7B23%7D%20%26%20m_%7B24%7D%5C%5C%20m_%7B31%7D%20%26%20m_%7B32%7D%20%26%20m_%7B33%7D%20%26%20m_%7B34%7D%20%5Cend%7Bbmatrix%7D%20%5Cright%20%29)

From above relations of each coordinate, we could get:

![equation_E1](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20r_%7B11%7D%20%26%20r_%7B12%7D%20%26%20r_%7B13%7D%20%26%200%5C%5C%20r_%7B21%7D%20%26%20r_%7B22%7D%20%26%20r_%7B23%7D%20%26%200%5C%5C%20r_%7B31%7D%20%26%20r_%7B32%7D%20%26%20r_%7B33%7D%20%26%200%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%201%20%26%200%20%26%200%20%26%20-c_%7Bx%7D%5C%5C%200%20%26%201%20%26%200%20%26%20-c_%7By%7D%5C%5C%200%20%26%200%20%26%201%20%26%20-c_%7Bz%7D%5C%5C%200%20%26%200%20%26%200%20%26%201%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20U%5C%5C%20V%5C%5C%20W%5C%5C%201%20%5Cend%7Bbmatrix%7D)

![euqation_E2](https://latex.codecogs.com/svg.latex?%5Cbegin%7Bbmatrix%7D%20x%27%5C%5C%20y%27%5C%5C%20z%27%20%5Cend%7Bbmatrix%7D%3D%20%5Cbegin%7Bbmatrix%7D%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7Bx%7D%7D%20%26%20s_%7Bk%7D%20%26%20o_%7Bx%7D%20%26%200%5C%5C%200%20%26%20%5Cfrac%7B%5Cboldsymbol%7Bf%7D%7D%7Bs_%7By%7D%7D%20%26%20o_%7By%7D%20%26%200%5C%5C%200%20%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D)

![equation_E3](https://latex.codecogs.com/svg.latex?%5CRightarrow%20x%3DK%5Cbegin%7Bbmatrix%7D%20R%20%26%20r%20%5Cend%7Bbmatrix%7DX)