"""
Credits to Intel RealSense Developer Team
.. Code Author: Aldy Helnawan <aldyhelnawan003@gmail.com>
..                            <aldyhelnawan.18071@mhs.its.ac.id>
..                            <github: aldyhelnawan>
"""

""" Camera Resolution Configuration """
input_res = input("What is the configuration of the camera? 640x480[480p] 1280x720[720p] ")
if input_res == '480p':
    """ Camera Resolution 480p """
    hres = 640
    vres = 480
    """ Camera Video Crop 480p Configuration to Align Stereo Module With RGB Module """
    left = int(103.95)
    top = int(60.81)
    right = int(hres - 91.3)
    bottom = int(vres - 83.51)
elif input_res == '720p':
    """ Camera Resolution 720p """
    hres = 1280
    vres = 720
    """ Camera Video Crop 720p Configuration to Align Stereo Module With RGB Module """
    left = int(204.84)
    top = int(94.33)
    right = int(hres - 186.13)
    bottom = int(vres - 126.41)

""" Camera Video Resize Resolution Configuration to Align Stereo Module With RGB Module """
width = hres
height = vres
dim = (width, height)

""" FPS Size """
fps = 30

""" Camera Resolution Dataset Cityscapes Configuration """
hres_crop = 1024
vres_crop = 512

""" Infrared Sensor Pipeline Configuration """
# IR_1 is the left Infrared, IR_2 is for the Right Infrared
# If ir_x = 0, then it's off. If ir_x = 1, it's on
ir_1 = 1
ir_2 = 0

""" Depth Hole Filler Configuration """
fill_stereo_camera = input("Fill the depth hole? yes[y]  no[n] ")
# The higher the number, the smoother the depth filtered
hole_fill_config = 1

""" Depth Colorizer Configuration """
# Possible values for color_scheme:
# 0 - Jet; 1 - Classic; 2 - WhiteToBlack; 3 - BlackToWhite; 4 - Bio; 5 - Cold; 6 - Warm; 7 - Quantized; 8 - Pattern
color_mode = 2