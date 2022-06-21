"""
Credits to Intel RealSense Developer Team for providing the tutorial & guides
.. Code Author: Aldy Helnawan <aldyhelnawan003@gmail.com>
..                            <aldyhelnawan.18071@mhs.its.ac.id>
..                            <github: aldyhelnawan>
"""

import pyrealsense2 as rs
import numpy as np
import cv2
from realsense_d435i_config import hres, vres, fps, ir_1, ir_2, fill_stereo_camera, \
    color_mode, hole_fill_config, hres_custom, vres_custom

""" Insert the RealSense .bag File """
file = input("Please insert the .bag file name here: ")

""" Saved Video Resolution Configuration """
# (Recommended to Use the same config as the bag file or the time you record the bag file)
# Or if you wana change it to a lower resolution / settings, there's no problem with it.
svhres = hres_custom
svvres = vres_custom
svfps = fps
svhtres = int(svhres*3)

""" Configuration of Save Video """
# The default use 20 FPS, so we can put 30 FPS as a "normal" speed reference
# If we put 60 FPS, the video will speedup 1.5x up to 2.0x since the origin fps is 30
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_rgb = cv2.VideoWriter('video_rgb.avi', fourcc, svfps, (svhres,svvres))
out_depth = cv2.VideoWriter('video_depth.avi', fourcc, svfps, (svhres,svvres))
out_infrared = cv2.VideoWriter('video_infrared.avi', fourcc, svfps, (svhres,svvres))
out_rgb_depth_infrared = cv2.VideoWriter('video_rgb_depth_infrared.avi', fourcc, svfps, (svhtres,svvres))

########################################################################################################################
class IntelRealSenseCamera:
# Initialize the camera
    def __init__(self):
        print("Loading Intel RealSense Camera")
        self.pipeline = rs.pipeline()

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
        self.pipeline.start(config)

        align_rgb_depth = rs.stream.color
        self.align_depth = align_rgb_depth
        align_rgb_infrared = rs.stream.color
        self.align_infrared = align_rgb_infrared

# Get the Camera to Stream
    def get_frame_stream(self):
        # Wait for a coherent pair of frames: color, depth, and infrared
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if (ir_1 == 1) & (ir_2 == 0):
            infrared_frame = frames.get_infrared_frame(1)
        if (ir_2 == 1) & (ir_1 == 0):
            infrared_frame = frames.get_infrared_frame(2)

        if not color_frame or not depth_frame or not infrared_frame:
            # If there is no frame, probably camera not connected, return False
            print("Error!. No Camera Detected!. Make Sure That The Intel Realsense Camera Is Correctly Connected")
            return False, None, None, None, None

        # Set the number inside () to define the visualized depth color:
        colorizer = rs.colorizer(color_mode)

        # Setup the depth hole filler
        if fill_stereo_camera == "y":
            # Apply filter to fill the Holes in the depth image
            spatial = rs.spatial_filter()
            spatial.set_option(rs.option.holes_fill, hole_fill_config)
            filtered_depth = spatial.process(depth_frame)
            filtered_infrared = spatial.process(infrared_frame)

            # Fill the Holes in the Stereo Sensor (Depth Sensor and Infrared Sensor)
            hole_filling = rs.hole_filling_filter()
            filled_depth = hole_filling.process(filtered_depth)
            filled_infrared = hole_filling.process(filtered_infrared)

            # Create colormap to show the visual depth of the Objects
            depth_color_frame = colorizer.colorize(filled_depth)
            filled_infrared = filled_infrared

        if fill_stereo_camera == "n":
            depth_color_frame = colorizer.colorize(depth_frame)
            filled_infrared = infrared_frame

        # Convert depth_frame to numpy array to render image in opencv
        color_image = np.asanyarray(color_frame.get_data())
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        infrared_image = np.asanyarray(filled_infrared.get_data())

        # Special for color_image, convert bgr (opencv)  to rgb (opencv)
        # And convert the Infrared Sensor to a 3D Matrix as the numpy can't process the 2 Channel Matrix
        color_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        infrared_3d = cv2.cvtColor(infrared_image, cv2.COLOR_GRAY2RGB)

        return True, color_rgb, depth_color_image, infrared_3d

    def release(self):
        self.pipeline.stop()