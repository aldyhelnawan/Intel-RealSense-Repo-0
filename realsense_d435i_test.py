"""
Credits to Intel RealSense Developer Team for providing the tutorial & guides
.. Code Author: Aldy Helnawan <aldyhelnawan003@gmail.com>
..                            <aldyhelnawan.18071@mhs.its.ac.id>
..                            <github: aldyhelnawan>
"""

"""
=================================================
== RUN THE CAMERA CODE ON THIS PYTHON FILE ===
=================================================
"""

""" Create an option to choose which source user want to use """
choose = input("Do you want to play the .bag file?   yes[y]   no[n]  ")
if choose == 'y':
    save_file_bag = input("Do you want to save the .bag file?  yes[y]  no[n] ")
    if save_file_bag == 'y':
        from realsense_d435i_bag_save import IntelRealSenseCamera, out_rgb, out_depth, out_infrared, out_rgb_depth_infrared
    elif save_file_bag !='y':
        from realsense_d435i_bag_playback import IntelRealSenseCamera
        print("Loading the .bag playback file... ")
if choose != 'y':
    from realsense_d435i_camera import IntelRealSenseCamera

""" Import the rest of the library """
from realsense_d435i_config import left, right, top, bottom, dim
import cv2
import numpy as np

rs = IntelRealSenseCamera()


while True:
    ret, color_rgb, depth_color_image, infrared_3d = rs.get_frame_stream()

    """ Crop the Depth and Infrared Pipeline to Align Them With RGB pipeline """
    crop_depth = depth_color_image[top:bottom, left:right]
    infrared_crop = infrared_3d[top:bottom, left:right]

    """ Resize Visual Resolution After Cropped to Match with RGB Resolution """
    resized_depth = cv2.resize(crop_depth, dim, interpolation=cv2.INTER_AREA)
    resized_infrared = cv2.resize(infrared_crop, dim, interpolation=cv2.INTER_AREA)

    """ Display the camera """
    cv2.namedWindow("Color, Depth, and Infrared Frame", cv2.WINDOW_KEEPRATIO)
    rgb_depth_infrared = np.hstack((color_rgb, resized_depth, resized_infrared))
    cv2.imshow("Color, Depth, and Infrared Frame", rgb_depth_infrared)

    # Write the Video to Save It
    out_rgb.write(color_rgb)
    out_depth.write(resized_depth)
    out_infrared.write(resized_infrared)
    out_rgb_depth_infrared.write(rgb_depth_infrared)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break

rs.release()
cv2.destroyAllWindows()
