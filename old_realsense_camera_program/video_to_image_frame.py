## THis program is created to convert video format (.avi) to image by frame
## The fps set depends on the images per second to cut.
## Before run this program, you need to create a folder named videos, then drop the video file to the folder.
## The resolution that created by this program in default depends on the video resolution
## The output (images) were crated on the save file
## github: aldyhelnawan

# How to run the video to image separator:
# Use this command:
# python video_to_image_frame.py

import os
import numpy as np
import cv2
from glob import glob

def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name {path}")

def save_frame(video_path, save_dir, gap=10):
    name = video_path.split("/")[-1].split(".")[0]
    save_path = os.path.join(save_dir, name)
    create_dir(save_path)

    cap = cv2.VideoCapture(video_path)
    idx = 0

    while True:
        ret, frame = cap.read()

        if ret == False:
            cap.release()
            break

        if idx == 0:
            cv2.imwrite(f"{save_path}/{idx}.png", frame)
        else:
            if idx % gap == 0:
                cv2.imwrite(f"{save_path}/{idx}.png", frame)

        idx += 1

if __name__ == "__main__":
    video_paths = glob("videos/*")
    save_dir = "save"

    for path in video_paths:
        save_frame(path, save_dir, gap=10)
