import cv2
import sys
sys.path.append("/home/raul/miscosas/openpose/build/python")
from openpose import pyopenpose as op

bodyPoints = { 'Nose': 0, 'Neck': 1, 'RShoulder': 2, 'RElbow': 3, 'RWrist': 4, 'LShoulder': 5, 
          'LElbow': 6, 'LWrist': 7, 'MidHip': 8, 'RHip': 9, 'RKnee': 10, 'RAnkle': 11, 
          'LHip': 12, 'LKnee': 13, 'LAnkle': 14, 'REye': 15, 'LEye': 16, 'REar': 17, 'LEar': 18, 
          'LBigToe': 19, 'LSmallToe': 20, 'LHeel': 21, 'RBigToe': 22, 'RSmallToe': 23, 'RHeel': 24, 
          'Background': 25}

def person_with_hands_in_image(image_path, openposeWrapper):
  """
  Returns True if there is a person with visible head and hands in the image .
  """
  datum = op.Datum()
  imageToProcess = cv2.imread(image_path)
  datum.cvInputData = imageToProcess
  openposeWrapper.emplaceAndPop(op.VectorDatum([datum]))

  if datum.poseKeypoints.size == 0:
    return False
  else:
    if datum.poseKeypoints.shape[0] > 0:
      for i in range(datum.poseKeypoints.shape[0]):
        print(datum.poseKeypoints[i][bodyPoints['Nose']] )
        print(datum.poseKeypoints[i][bodyPoints['RWrist']] )
        print(datum.poseKeypoints[i][bodyPoints['LWrist']] )
        return ( (datum.poseKeypoints[i][bodyPoints['Nose']] != [0,0,0]).all() and \
          (datum.poseKeypoints[i][bodyPoints['RWrist']] != [0,0,0]).all() and \
          (datum.poseKeypoints[i][bodyPoints['LWrist']] != [0,0,0]).all()
        )
  return False
      