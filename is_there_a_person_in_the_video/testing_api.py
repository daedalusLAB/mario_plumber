#!/usr/bin/env python

# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import common


# Import openpose libraries
sys.path.append("/home/raul/miscosas/openpose/build/python")
from openpose import pyopenpose as op

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", 
    default="/home/raul/miscosas/openpose/examples/media/COCO_val2014_000000000459.jpg", 
    help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/home/raul/miscosas/openpose/models/"


# Starting OpenPose
openposeWrapper = op.WrapperPython()
openposeWrapper.configure(params)
openposeWrapper.start()

if common.person_with_hands_in_image(args[0].image_path, openposeWrapper):
    print("Person with hands in image")
else:
    print("No person with hands in image")
