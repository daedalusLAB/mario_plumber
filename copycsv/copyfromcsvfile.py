#!/usr/bin/env python

# copyfromcsvfile.py --input_csv csv_file.csv --videos_folder /home/user/videos --destination_folder /home/user/selected_videos
# Given a csv file with a filename per row, this script copy all the videos in videos_folder to destination_folder
# if the filename of the video is in the csv file.

# Example:
# copyfromcsvfile.py --input_csv csv_file.csv --videos_folder /home/user/videos --destination_folder /home/user/selected_videos


import os
import sys
import argparse
import shutil

parser = argparse.ArgumentParser(description='Copy videos that have a matching filename in the csv file to the destination folder.')
parser.add_argument('--input_csv', type=str, help='Input csv file.', required=True)
parser.add_argument('--videos_folder', type=str, help='Folder with .mp4 videos.', required=True)
parser.add_argument('--destination_folder', type=str, help='Destination folder.', required=True)

args = parser.parse_args()

if not os.path.exists(args.input_csv):
    print("The csv file does not exist.")
    sys.exit(1)

if not os.path.exists(args.videos_folder):
    print("The videos folder does not exist.")
    sys.exit(1) 

if not os.path.exists(args.destination_folder):
    print("The destination folder does not exist.")
    print("Creating destination folder.")
    os.makedirs(args.destination_folder)  

# open the csv file and read all the lines in a loop
with open(args.input_csv, 'r') as csv_file:
    for line in csv_file:
      # Remove " and ' from the line
      line = line.replace('"', '')
      line = line.replace("'", '')
      # if line + .mp4 exists in videos_folder, copy it to destination_folder
      video_file_name = line.strip() + ".mp4"
      video_file_path = os.path.join(args.videos_folder, video_file_name)
      if os.path.exists(video_file_path):
        print("Found matching video file: " + video_file_name)
        shutil.copy(video_file_path, args.destination_folder)
      else:
        print("No matching video file: " + video_file_name)

    

