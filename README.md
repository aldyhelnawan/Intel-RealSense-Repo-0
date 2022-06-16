## Intel_RealSense_D4xx_Camera_Python
#### [UPDATE] | June 16th, 2022.

This is the improvement of the previous program that with pyrealsense2 python library.

Tested it with Intel RealSense D435i Stereo Camera on Windows 10 with Pycharm on Anaconda Virtual Environment.

This update has a major changes, include in this list:
  1. User interaction with the code. So, no need to configure so much to use it.
  2. Adding a config file (realsense_d435i_config.py) for configuring the camera for other mode in .
  3. All interaction already centralized to one python file (realsense_d435i_test.py).
  4. Update of the stereo module (Depth & Infrared) FOV to be aligned with the RGB FOV.
  5. Configurable to switch between 1280x720[720p] with 620x480[480p] resolutions.

The file that included in this repository:
  1. realsense_d435i_test.py
  2. realsense_d435i_config.py
  3. realsense_d435i_camera.py
  4. realsense_d435i_bag_save.py
  5. realsense_d435i_bag_playback.py

Note:
For the .bag file, it is recommended that the camera configuration is matched with the .bag file configuration which it's created.
And to change the camera configuration such as resolutions and fps, you need to do it on the realsense_d435i_config.py python file.



Credits to [Intel RealSense Team](https://github.com/IntelRealSense/librealsense)
