## This is the Intel RealSense Camera "Package" that modified to make sure many of the component configurable ans usable
## This program is not created for the IMU Sensor that included in the Camera.
## The FOV of this camera is Aligned to the RGB sensor FOV
## The purpose of the alignment is to make sure the famres that captured by the camera have the same res and vector

## Created by Aldy Helnawan
## Github: aldyhelnawan

## Credits to Intel RealSense Team for the example they provide

# Import the Library
import pyrealsense2 as rs
import cv2
import numpy as np

# Use the enable_device for enable or disable for the program capable to read the recorded device from file
# to be used by the pipeline through the playback

########################################################################################################################
## The bag file that use to playback ##
file = 'name_of_the_file.bag'
########################################################################################################################

########################################################################################################################
## Command for the enable the playback ##
# To enable the playback capability, use enable_device = 1
# To Disable the playback capability, use enable_device = 0
enable_device = 0
########################################################################################################################

########################################################################################################################
## Camera Configuration ##
# Camera Configuration (Recommended: Use the same config as the bag file or the time you record the bag file)
hres = 1280
vres = 720
fps = 30

# IR_1 is the left Infrared, IR_2 is for the Right Infrared
# If ir_x = 0, then it's off. If ir_x = 1, it's on
ir_1 = 1
ir_2 = 0
########################################################################################################################

class IntelRealSenseCamera:
# Initialize the camera
    def __init__(self):
        print("Loading Intel RealSense Camera")
        self.pipeline = rs.pipeline()

        config = rs.config()

        # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
        if enable_device == 1:
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

        # Align the camera Stereo Camera (Depth and Infrared Sensor) to RGB Sensor, because RGB and Stereo Sensors have
        # a different FOV.
        # So we need to align the FOV to make sure that all the frame that process is the same
        align_rgb_depth = rs.stream.color
        self.align_depth = rs.align(align_rgb_depth)

        align_rgb_infrared = rs.stream.color
        self.align_infrared = rs.align(align_rgb_infrared)

# Get the Camera to Stream
    def get_frame_stream(self):
        # Wait for a coherent pair of frames: color, depth, and infrared
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align_depth.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        # depth_frame = frames.get_depth_frame()
        aligned_infrared = self.align_infrared.process(frames)
        infrared_frame = aligned_infrared.get_infrared_frame(1)
        # if ir_2 == 1:
        #     infrared_frame_2 = aligned_frames.get_infrared_frame(2)

        if not color_frame or not depth_frame or not infrared_frame:
            # If there is no frame, probably camera not connected, return False
            print("Error!. No Camera Detected!. Make Sure That The Intel Realsense Camera Is Correctly Connected")
            return False, None, None, None, None

        # Apply filter to fill the Holes in the depth image
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 5)
        filtered_depth = spatial.process(depth_frame)
        filtered_infrared = spatial.process(infrared_frame)
        # if ir_2 == 1:
        #     filtered_infrared_2 = spatial.process(infrared_frame_2)

        # Fill the Holes in the Stereo Sensor (Depth Sensor and Infrared Sensor)
        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)
        filled_infrared = hole_filling.process(filtered_infrared)
        # if ir_2 == 1:
        #     filled_infrared_2 = hole_filling.process(filtered_infrared_2)

        # Create colormap to show the visual depth of the Objects
        colorizer = rs.colorizer()
        depth_color_frame = colorizer.colorize(filled_depth)

        # Convert depth_frame to numpy array to render image in opencv
        color_image = np.asanyarray(color_frame.get_data())
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        infrared_image = np.asanyarray(filled_infrared.get_data())
        # if ir_2 == 1:
        #     infrared_image_2 = np.asanyarray(filled_infrared_2.get_data())

        # Special for color_image, convert bgr (opencv)  to rgb (opencv)
        # And convert the Infrared Sensor to a 3D Matrix as the numpy can't process the 2D Matrix
        color_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        infrared_3d = cv2.cvtColor(infrared_image, cv2.COLOR_GRAY2RGB)

        return True, color_rgb, depth_color_image, infrared_3d

    def release(self):
        self.pipeline.release()
