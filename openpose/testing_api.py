#!/usr/bin/env python

# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse


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

      
bodyPoints = { 'Nose': 0, 'Neck': 1, 'RShoulder': 2, 'RElbow': 3, 'RWrist': 4, 'LShoulder': 5, 
          'LElbow': 6, 'LWrist': 7, 'MidHip': 8, 'RHip': 9, 'RKnee': 10, 'RAnkle': 11, 
          'LHip': 12, 'LKnee': 13, 'LAnkle': 14, 'REye': 15, 'LEye': 16, 'REar': 17, 'LEar': 18, 
          'LBigToe': 19, 'LSmallToe': 20, 'LHeel': 21, 'RBigToe': 22, 'RSmallToe': 23, 'RHeel': 24, 
          'Background': 25}


poseModel = op.PoseModel.BODY_25

datum = op.Datum()
imageToProcess = cv2.imread(args[0].image_path)
datum.cvInputData = imageToProcess
openposeWrapper.emplaceAndPop(op.VectorDatum([datum]))


if datum.poseKeypoints.size == 0:
    print("No pose found")
else :
    # Result for BODY_25 (25 body parts consisting of COCO + foot)
    if datum.poseKeypoints.shape[0] == 1:
        print("One pose found")
        if (datum.poseKeypoints[0][bodyPoints['Nose']] != [0,0,0]).all():
            print("Nose found")
        if (datum.poseKeypoints[0][bodyPoints['RWrist']] != [0,0,0]).all():
            print("RWrist found")
        if (datum.poseKeypoints[0][bodyPoints['LWrist']] != [0,0,0]).all():
            print("LWrist found")
        if (datum.poseKeypoints[0][bodyPoints['RHeel']] != [0,0,0]).all():
            print("RHeel found")





#print("Body keypoints: \n" + str(datum.poseKeypoints))


