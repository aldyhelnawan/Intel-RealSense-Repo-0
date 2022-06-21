## Intel_RealSense_D4xx_Camera_Python
#### [UPDATE] | June 21st, 2022.

This is the update of the previous code.

Tested with Intel RealSense D435i Stereo Camera on Windows 10 and Ubuntu 20.04 with Pycharm on Anaconda Virtual Environment.

List of updates, some major changes, deletion, and modification.
  1. Removed the 480p, 720p resolution option.
  2. Removed some sections that doesn't functional.
  3. Added the optional resolution input (recomended up to 1280x720 pixels for better image quality).
  4. Added optional resolution for .bag playback selection (and .bag video save in .avi format).

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
