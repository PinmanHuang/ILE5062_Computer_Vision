import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import camera_calibration_show_extrinsics as show
from PIL import Image

DEBUG = True
img_num = 0
d_img_len = 3

#####################################################################################
#                           Compute View Homography                                 #
#   N: the number of corner points                                                  #
#   | x |   | h11 h12 h13 |   | U |                                                 #
#   | y | = | h21 h22 h23 | . | V |                                                 #
#   | z |   | h31 h32 h33 |   | 1 |                                                 #
#   u = x/z , v = y/z                                                               #
#   => u = (h11U+h12V+h13)/(h31U+h32V+h33), v = (h21U+h22V+h23)/(h31U+h32V+h33)     #
#   => (h11U+h12V+h13)-u(h31U+h32V+h33) = 0, (h21U+h22V+h23)-v(h31U+h32V+h33) = 0   #
#                                            | h11 |                                #
#                                            | h12 |                                #
#                                            | h13 |                                #
#   | U   V   1   0   0   0   -uU -uV -u |   | h21 |                                #
#   | 0   0   0   U   V   1   -vU -vV -v | . | h22 | = 0                            #
#                                            | h23 |                                #
#                                            | h31 |                                #
#                                            | h32 |                                #
#                                            | h33 |                                #
#                     P(2N*9)                 h(9*1) = 0                            #
#####################################################################################
def compute_view_homography(imgpoints, objpoints):
    print('Homography for View...')
    N = len(imgpoints)
    # N = 8   # N needs bigger than 8, because imgpoints are in order, if we choose less than 8 points, it will be a line
    P = np.zeros((2*N, 9))    # initialize P matrix, each corner will contribute two rows

    # create P matrix
    for i in range(N):
        U, V, W = objpoints[i]
        u, v = imgpoints[i][0]

        row_1 = np.array([U, V, 1, 0, 0, 0, -u*U, -u*V, -u])
        row_2 = np.array([0, 0, 0, U, V, 1, -v*U, -v*V, -v])
        P[2*i] = row_1
        P[2*i+1] = row_2

        # print("P_model {0} \tp_row {1}".format(2*i, P[2*i]))
        # print("P_model {0} \tp_row {1}".format(2*i+1, P[2*i+1]))
    
    # print("P: {0}\n{1}".format(P.shape, P))
    u, s, vh = np.linalg.svd(P, full_matrices=False)
    # print("u: {0}\n{1}".format(u.shape, u))
    # print("s: {0}\n{1}".format(s.shape, s))
    # print("vh: {0}\n{1}".format(vh.shape, vh))
    h = vh[np.argmin(s)]
    print("h: {0}\n{1}".format(h.shape, h))
    return h

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# (8,6) is for the given testing images.
# If you use the another data (e.g. pictures you take by your smartphone), 
# you need to set the corresponding numbers.
corner_x = 7
corner_y = 7
objp = np.zeros((corner_x*corner_y,3), np.float32)
objp[:,:2] = np.mgrid[0:corner_x, 0:corner_y].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

# Make a list of calibration images
images = glob.glob('data/*.jpg')
sorted(glob.glob('*.png'))

# Step through the list and search for chessboard corners
print('Start finding chessboard corners...')
for idx, fname in enumerate(images):
    if DEBUG and img_num == d_img_len:
        break
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # plt.imshow(gray, cmap='gray')
    # plt.show()

    #Find the chessboard corners
    print('find the chessboard corners of',fname)
    ret, corners = cv2.findChessboardCorners(gray, (corner_x,corner_y), None)   # search from top-left

    # If found, add object points, image points
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (corner_x,corner_y), corners, ret)
        
        # plt.imshow(img, cmap='gray')
        # plt.show()
    img_num += 1

#######################################################################################################
#                                Homework 1 Camera Calibration                                        #
#               You need to implement camera calibration(02-camera p.76-80) here.                     #
#   DO NOT use the function directly, you need to write your own calibration function from scratch.   #
#                                          H I N T                                                    #
#                        1.Use the points in each images to find Hi                                   #
#                        2.Use Hi to find out the intrinsic matrix K                                  #
#                        3.Find out the extrensics matrix of each images.                             #
#######################################################################################################
print('Camera calibration...')
img_size = (img.shape[1], img.shape[0])
""""""
# You need to comment these functions and write your calibration function from scratch.
# Notice that rvecs is rotation vector, not the rotation matrix, and tvecs is translation vector.
# In practice, you'll derive extrinsics matrixes directly. The shape must be [pts_num,3,4], and use them to plot.
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)
Vr = np.array(rvecs)
Tr = np.array(tvecs)
extrinsics = np.concatenate((Vr, Tr), axis=1).reshape(-1,6)
""""""

#######################################################################################################
h = np.zeros((img_num, 9))    # homography 1D matrix of all images (img_num*9)
for i in range(len(imgpoints)):
    h[i] = compute_view_homography(imgpoints[i], objpoints[i])
# print("h: {0}\n{1}".format(h.shape, h))
#######################################################################################################

# show the camera extrinsics
print('Show the camera extrinsics')
# plot setting
# You can modify it for better visualization
fig = plt.figure(figsize=(10, 10))
ax = fig.gca(projection='3d')
# camera setting
camera_matrix = mtx
cam_width = 0.064/0.1
cam_height = 0.032/0.1
scale_focal = 1600
# chess board setting
board_width = 8
board_height = 6
square_size = 1
# display
# True -> fix board, moving cameras
# False -> fix camera, moving boards
min_values, max_values = show.draw_camera_boards(ax, camera_matrix, cam_width, cam_height,
                                                scale_focal, extrinsics, board_width,
                                                board_height, square_size, True)

X_min = min_values[0]
X_max = max_values[0]
Y_min = min_values[1]
Y_max = max_values[1]
Z_min = min_values[2]
Z_max = max_values[2]
max_range = np.array([X_max-X_min, Y_max-Y_min, Z_max-Z_min]).max() / 2.0

mid_x = (X_max+X_min) * 0.5
mid_y = (Y_max+Y_min) * 0.5
mid_z = (Z_max+Z_min) * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, 0)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_zlabel('-y')
ax.set_title('Extrinsic Parameters Visualization')
# plt.show()

#animation for rotating plot
"""
for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.pause(.001)
"""

