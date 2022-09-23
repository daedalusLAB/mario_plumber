# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import pyopenpose as op

try:
    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../models/"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(args[0].image_path)
    datum.cvInputData = imageToProcess
#    opWrapper.emplaceAndPop([datum])
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))


    # Display Image
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    cv2.imwrite("result_body.jpg", datum.cvOutputData)
    #cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", datum.cvOutputData)
    #cv2.waitKey(0)
except Exception as e:
    print(e)
    print("RAULLLL")
    sys.exit(-1)
