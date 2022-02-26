import cv2
import numpy as np
from intel_realsense_camera import *

videoplayback = input('Wanna Play the Video Playback from the .bag file? ')
if videoplayback == 'yes':
    from videplayback_bag import *

# Load the RealSense camera
rs = IntelRealSenseCamera()

while True:
    # Get the Intel RealSense Camera Frame into real time
    ret, color_rgb, depth_color_image, infrared_3d = rs.get_frame_stream()

    cv2.namedWindow("Color, Depth, and Infrared Stream", cv2.WINDOW_KEEPRATIO)

    # Render image in opencv window
    images_depth_infrared = np.hstack((color_rgb, depth_color_image, infrared_3d))
    # images_depth = np.hstack((color_rgb, depth_color_image))
    # images_infrared = np.hstack((color_rgb, infrared_3d))

    cv2.imshow("Color, Depth, and Infrared Stream", images_depth_infrared)

    key = cv2.waitKey(1)
    if key == 27:
        break

rs.release()
cv2.destroyAllWindows()