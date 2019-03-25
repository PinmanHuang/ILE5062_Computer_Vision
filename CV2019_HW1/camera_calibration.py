import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import camera_calibration_show_extrinsics as show
from PIL import Image

DEBUG = False
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
        u, v = imgpoints[i,0]

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

#################################################################################################################################################################
#                       Compute Symmetric Positive Matrix                                                                                                       #
#   N = images numbers (needing at least 3 images to compute b matrix)                                                                                          #
#   Vb = 0                                                                                                                                                      #
#   h = | h11 h12 h13 h21 h22 h23 h31 h32 h33 |                                                                                                                 #
#       | h11 h12 h13 |                                                                                                                                         #
#   H = | h21 h22 h23 | = | h1 h2 h3 |                                                                                                                          #
#       | h31 h32 h33 |                                                                                                                                         #
#       | b11 b12 b13 |                                                                                                                                         #
#   B = | b12 b22 b23 |                                                                                                                                         #
#       | b13 b23 b33 |                                                                                                                                         #
#   b = | b11 b12 b13 b22 b23 b33 |                                                                                                                             #
#   => h1.T B h2 = 0, h1.T B h1 = h2.T B h2                                                                                                                     #
#                                                                                                                                                  | b11 |      #
#                                                                                                                                                  | b12 |      #
#   |    h11h12              h12h21+h11h22          h12h31+h11h32                      h21h22              h22h31+h21h32             h31h32     |  | b13 |      #
#   | h11h11-h12h12 (h11h21+h11h21)-(h12h22+h12h22) (h11h31+h11h31)-(h12h32+h12h32) h21h21-h22h22 (h21h31+h21h31)-(h22h32+h22h32) h31h31-h32h32 |  | b22 | = 0  #
#                                                                                                                                                  | b23 |      #
#                                                                                                                                                  | b33 |      #
#                                                               V(2N*6)                                                                             b(6*1) = 0  #
#################################################################################################################################################################

def compute_symmetric_positive_matrix(h):
    print('Compute b from Vb = 0...')
    # N = len(h)
    N = 3
    V = np.zeros((2*N, 6))  # initialize V matrix, each image will contribute two rows

    # create P matrix
    for i in range(N):
        H = h[i].reshape(3, 3)
        row_1 = np.array([
            H[0,0]*H[0,1],
            H[0,1]*H[1,0]+H[0,0]*H[1,1],
            H[0,1]*H[2,0]+H[0,0]*H[2,1],
            H[1,0]*H[1,1],
            H[1,1]*H[2,0]+H[1,0]*H[2,1],
            H[2,0]*H[2,1]
        ])
        row_2 = np.array([
            H[0,0]*H[0,0]-H[0,1]*H[0,1],
            2*H[0,0]*H[1,0]-2*H[0,1]*H[1,1],
            2*H[0,0]*H[2,0]-2*H[0,1]*H[2,1],
            H[1,0]*H[1,0]-H[1,1]*H[1,1],
            2*H[1,0]*H[2,0]-2*H[1,1]*H[2,1],
            H[2,0]*H[2,0]-H[2,1]*H[2,1]
        ])
        V[2*i] = row_1
        V[2*i+1] = row_2

    # print("V: {0}\n{1}".format(V.shape, V))
    u, s, vh = np.linalg.svd(V, full_matrices=False)
    # print("u: {0}\n{1}".format(u.shape, u))
    # print("s: {0}\n{1}".format(s.shape, s))
    # print("vh: {0}\n{1}".format(vh.shape, vh))
    b = vh[np.argmin(s)]
    print("b: {0}\n{1}".format(b.shape, b))
    return b

#############################################################################################
#                                   Intrinsic Matrix                                        #
#   B=inv(K.T) inv(K)                                                                       #
#   K is an upper triangular matrix and its inverse is also an upper triangular matrix,     #
#   so B is a lower triangular matrix multiply to upper triangular matrix,                  #
#   then we could use Cholesky Decomposition to get the inv(K),                             #
#   and do the inverse to find out the K.                                                   #
#############################################################################################
def intrinsic_matrix(b, img_size):
    print('Intrinsic Matrix...')
    B = np.array([
        [b[0], b[1], b[2]],
        [b[1], b[3], b[4]],
        [b[2], b[4], b[5]]
    ])
    # print("B: {0}\n{1}".format(B.shape, B))
    K = np.linalg.inv((np.linalg.cholesky(B)).transpose())
    # K = np.array([
    #     [K[0,0], 0, img_size[0]/2],
    #     [K[1,0], K[1,1], img_size[1]/2],
    #     [K[2,0], K[2,1], 1]
    # ])
    # vc = (b[1]*b[2] - b[0]*b[4])/(b[0]*b[3] - b[1]**2)
    # l = b[5] - (b[2]**2 + vc*(b[1]*b[3] - b[0]*b[4]))/b[0]
    # alpha = np.sqrt((l/b[0]))
    # beta = np.sqrt(((l*b[0])/(b[0]*b[3] - b[1]**2)))
    # gamma = -1*((b[1])*(alpha**2) *(beta/l))
    # uc = (gamma*vc/beta) - (b[2]*(alpha**2)/l)
    # K = np.array([
    #     [alpha, gamma, uc],
    #     [0, beta, vc],
    #     [0, 0, 1.0],
    # ])
    print("K: {0}\n{1}".format(K.shape, K))
    return K

def extrinsic_matrix(K, h):
    print('Extrinsic Matrix...')
    K_inv = np.linalg.inv(K)
    N = len(h)
    extrinsics = np.zeros((N, 6))
    for i in range(N):
        H = h[i].reshape(3, 3)
        h1 = H[:, 0]
        h2 = H[:, 1]
        h3 = H[:, 2]

        lam = 1/np.linalg.norm(np.matmul(K_inv, h1))
        r1T = lam*np.matmul(K_inv, h1)
        r2T = lam*np.matmul(K_inv, h2)
        r3T = np.cross(r1T, r2T)
        tT = lam*np.matmul(K_inv, h3)

        R = np.array([[r1T[0], r2T[0], r3T[0]], [r1T[1], r2T[1], r3T[1]], [r1T[2], r2T[2], r3T[2]]])
        r, j = cv2.Rodrigues(R)
        t = np.array([[tT[0]], [tT[1]], [tT[2]]])
        row = np.array([r[0,0], r[1,0], r[2,0], t[0,0], t[1,0], t[2,0]])
        # print("r: {0}\n{1}".format(r.shape, r))
        # print("t: {0}\n{1}".format(t.shape, t))
        print("row: {0}\n{1}".format(row.shape, row))
        extrinsics[i] = row

    print("extrinsics: {0}\n{1}".format(extrinsics.shape, extrinsics))
    return extrinsics

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
"""
# You need to comment these functions and write your calibration function from scratch.
# Notice that rvecs is rotation vector, not the rotation matrix, and tvecs is translation vector.
# In practice, you'll derive extrinsics matrixes directly. The shape must be [pts_num,3,4], and use them to plot.
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)
Vr = np.array(rvecs)
Tr = np.array(tvecs)
extrinsics = np.concatenate((Vr, Tr), axis=1).reshape(-1,6)
"""

#######################################################################################################
h = np.zeros((img_num, 9))    # homography 1D matrix of all images (img_num*9)
for i in range(len(imgpoints)):
    h[i] = compute_view_homography(imgpoints[i], objpoints[i])
print("h: {0}\n{1}".format(h.shape, h))
b = compute_symmetric_positive_matrix(h)
K = intrinsic_matrix(b, img_size)
extrinsics = extrinsic_matrix(K, h)
mtx = K
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
plt.show()

#animation for rotating plot
"""
for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.pause(.001)
"""

