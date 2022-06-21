"""
Credits to Intel RealSense Developer Team
.. Code Author: Aldy Helnawan <aldyhelnawan003@gmail.com>
..                            <aldyhelnawan.18071@mhs.its.ac.id>
..                            <github: aldyhelnawan>
"""

""" Camera Resolution Configuration """
print("What is the resolution of the camera? ")
""" 
..For usign optional resolution, we need to take the source from 1280x720p as the backbone.
..The reason is to make the FOV of each module the same, or it would distrub the masking or segmenting process.
..The logic is when the source already in 720p, we need to resize them to custom resolution, 
...so the FOV will remain the same.
..On Cityscapes dataset, the image resolution is 2048x1024 pixel, to make it smaller we could use 1024x512p
..resolution. So the ratio remain the same as the image provided (2:1).
..You can also use these options to use another resolution for your own project. 
..But the FOV remain the same (~99% similarity)
"""
""" Camera Resolution 720p """
hres = 1280
vres = 720
""" Camera Video Crop 720p Configuration to Align Stereo Module With RGB Module """
left = int(204.84)
top = int(94.33)
right = int(hres - 186.13)
bottom = int(vres - 126.41)
""" 
We need to resize the resolution from 720p to 512p (or other resolution from the input options)
"""
""" Camera Resolution Dataset Cityscapes Configuration """
hres_custom = int(input("Input the width (horizontal) resolution: "))
vres_custom = int(input("Input the height (vertical) resolution: "))
dim_custom = (hres_custom, vres_custom)

""" Camera Video Resize Resolution Configuration to Align Stereo Module With RGB Module """
width = hres
height = vres
dim = (width, height)

""" FPS Size """
fps = 30

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