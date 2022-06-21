"""
Credits to Intel RealSense Developer Team for providing the tutorial & guides
.. Code Author: Aldy Helnawan <aldyhelnawan003@gmail.com>
..                            <aldyhelnawan.18071@mhs.its.ac.id>
..                            <github: aldyhelnawan>
"""
""" [UPDATE]: 
.Added a configurable resolution option for a custom resolution (recommended up to 1280x720).
.Remove the 480p and 720p resolution option.
"""

"""
=================================================
==== RUN THE CAMERA CODE ON THIS PYTHON FILE ====
=================================================
"""

""" Create an option to choose which source user want to use """
choose = input("Do you want to play the .bag file?   yes[y]   no[n]  ")
if choose == 'y':
    save_file_bag = input("Do you want to save the .bag file?  yes[y]  no[n] ")
    if save_file_bag == 'y':
        from realsense_d435i_bag_save import IntelRealSenseCamera, out_rgb, out_depth, out_infrared, out_rgb_depth_infrared
        from realsense_d435i_config import left, right, top, bottom, dim, dim_custom
    elif save_file_bag =='n':
        from realsense_d435i_bag_playback import IntelRealSenseCamera
        from realsense_d435i_config import left, right, top, bottom, dim, dim_custom
        print("Loading the .bag playback file... ")
elif choose == 'n':
    from realsense_d435i_camera import IntelRealSenseCamera
    from realsense_d435i_config import left, right, top, bottom, dim, dim_custom

""" Import the rest of the library """
import cv2
import numpy as np

rs = IntelRealSenseCamera()

while (choose == 'y') and (save_file_bag == 'n'):
    ret, color_rgb, depth_color_image, infrared_3d = rs.get_frame_stream()

    """ Crop the Depth and Infrared Pipeline to Align Them With RGB pipeline """
    crop_depth = depth_color_image[top:bottom, left:right]
    infrared_crop = infrared_3d[top:bottom, left:right]

    """ Resize Visual Resolution After Cropped to Match with RGB Resolution """
    resized_depth = cv2.resize(crop_depth, dim, interpolation=cv2.INTER_AREA)
    resized_infrared = cv2.resize(infrared_crop, dim, interpolation=cv2.INTER_AREA)

    """ Resize to the Custom Resolution After the Resolution Converted to 720p """
    rgb_custom = cv2.resize(color_rgb, dim_custom, interpolation = cv2.INTER_AREA)
    depth_custom = cv2.resize(resized_depth, dim_custom, interpolation = cv2.INTER_AREA)
    infrared_custom = cv2.resize(resized_infrared, dim_custom, interpolation = cv2.INTER_AREA)

    """ Display the camera """
    cv2.namedWindow("Color, Depth, and Infrared Frame", cv2.WINDOW_KEEPRATIO)
    rgb_depth_infrared_custom = np.hstack((rgb_custom, depth_custom, infrared_custom))
    cv2.imshow("Color, Depth, and Infrared Frame", rgb_depth_infrared_custom)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break

while (choose == 'y') and (save_file_bag == 'y'):
    ret, color_rgb, depth_color_image, infrared_3d = rs.get_frame_stream()

    """ Crop the Depth and Infrared Pipeline to Align Them With RGB pipeline """
    crop_depth = depth_color_image[top:bottom, left:right]
    infrared_crop = infrared_3d[top:bottom, left:right]

    """ Resize Visual Resolution After Cropped to Match with RGB Resolution """
    resized_depth = cv2.resize(crop_depth, dim, interpolation=cv2.INTER_AREA)
    resized_infrared = cv2.resize(infrared_crop, dim, interpolation=cv2.INTER_AREA)

    """ Resize to the Custom Resolution After the Resolution Converted to 720p """
    rgb_custom = cv2.resize(color_rgb, dim_custom, interpolation = cv2.INTER_AREA)
    depth_custom = cv2.resize(resized_depth, dim_custom, interpolation = cv2.INTER_AREA)
    infrared_custom = cv2.resize(resized_infrared, dim_custom, interpolation = cv2.INTER_AREA)

    """ Display the camera """
    cv2.namedWindow("Color, Depth, and Infrared Frame", cv2.WINDOW_KEEPRATIO)
    rgb_depth_infrared_custom = np.hstack((rgb_custom, depth_custom, infrared_custom))
    cv2.imshow("Color, Depth, and Infrared Frame", rgb_depth_infrared_custom)

    # Write the Video to Save It
    out_rgb.write(rgb_custom)
    out_depth.write(depth_custom)
    out_infrared.write(infrared_custom)
    out_rgb_depth_infrared.write(rgb_depth_infrared_custom)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break

while choose == 'n':
    ret, color_rgb, depth_color_image, infrared_3d = rs.get_frame_stream()

    """ Crop the Depth and Infrared Pipeline to Align Them With RGB pipeline """
    crop_depth = depth_color_image[top:bottom, left:right]
    infrared_crop = infrared_3d[top:bottom, left:right]

    """ Resize Visual Resolution After Cropped to Match with RGB Resolution """
    resized_depth = cv2.resize(crop_depth, dim, interpolation=cv2.INTER_AREA)
    resized_infrared = cv2.resize(infrared_crop, dim, interpolation=cv2.INTER_AREA)

    """ Resize to the Custom Resolution After the Resolution Converted to 720p """
    rgb_custom = cv2.resize(color_rgb, dim_custom, interpolation = cv2.INTER_AREA)
    depth_custom = cv2.resize(resized_depth, dim_custom, interpolation = cv2.INTER_AREA)
    infrared_custom = cv2.resize(resized_infrared, dim_custom, interpolation = cv2.INTER_AREA)

    """ Display the camera """
    cv2.namedWindow("Color, Depth, and Infrared Frame", cv2.WINDOW_KEEPRATIO)
    rgb_depth_infrared_custom = np.hstack((rgb_custom, depth_custom, infrared_custom))
    cv2.imshow("Color, Depth, and Infrared Frame", rgb_depth_infrared_custom)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break

rs.release()
cv2.destroyAllWindows()
