#####################################################
##               Read bag from file                ##
#####################################################

## Created by: Aldy Helnawan
## Github: aldyhelnawan

## This program is original example created by Intel RealSense devs (The read bag from file example),
## and modified as purpose to use the other feature of the Intel RealSense Depth (Stereo) Camera.
## The purpose of this program is to read the .bag file to show the result as a graphical view using OpenCV

# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2

# Initializt the .bag file (or the .bag path file)
file = '20220110_141836.bag'

# Camera Configuration (Recommended: Use the same config as the bag file or the time you record the bag file)
hres = 1280
vres = 720
fps = 30

# IR_1 is the left Infrared, IR_2 is for the Right Infrared
# If ir_x = 0, then it's off. If ir_x = 1, it's on
ir_1 = 1
ir_2 = 0

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, file)

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.color, hres, vres, rs.format.rgb8, fps)
    config.enable_stream(rs.stream.depth, hres, vres, rs.format.z16, fps)
    if ir_1 == 1:
        config.enable_stream(rs.stream.infrared, 1, hres, vres, rs.format.y8, fps)
    if ir_2 == 1:
        config.enable_stream(rs.stream.infrared, 2, hres, vres, rs.format.y8, fps)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image incv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
    # cv2.namedWindow("Color and Depth Stream", cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow("Color and Infrared Stream", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Color, Depth, and Infrared Stream", cv2.WINDOW_KEEPRATIO)
    # cv2.namedWindow("Color Stream", cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow("Infrared Stream", cv2.WINDOW_AUTOSIZE)

    # Create colorizer object
    colorizer = rs.colorizer()

    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get frame
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        infrared_frame = frames.get_infrared_frame(ir_1)
        if ir_2 == 1:
            infrared_frame_2 = frames.get_inrared_frame(2)

        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(depth_frame)

        # Convert depth_frame to numpy array to render image in opencv
        color_image = np.asanyarray(color_frame.get_data())
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        infrared_image = np.asanyarray(infrared_frame.get_data())

        # Special for color_image, convert bgr (opencv)  to rgb (opencv)
        color_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        infrared_3d = cv2.cvtColor(infrared_image, cv2.COLOR_GRAY2RGB)

        # Render image in opencv window
        images_depth_infrared = np.hstack((color_rgb, depth_color_image, infrared_3d))
        # images_depth = np.hstack((color_rgb, depth_color_image))
        # images_infrared = np.hstack((color_rgb, infrared_3d))

        cv2.imshow("Color, Depth, and Infrared Stream", images_depth_infrared)
        # cv2.imshow("Color and Depth Stream", images_depth)
        # cv2.imshow("Color and Infrared Stream", images_infrared)
        # cv2.imshow("Color Stream", color_rgb)
        # cv2.imshow("Depth Stream", depth_color_image)
        # cv2.imshow("Infrared Stream", infrared_image)

        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            pipeline.stop()
            break

finally:
    pass
