#!/usr/bin/env python

# copycsv.py <csv folder> <video folder> <destination folder> 
#    Given a folder with cvs, a folder with videos, and a destination folder,
#    this script will copy the csv files that have a matching video file to the destination folder.
#
#    Example:
#    copycsv.py --csv_folder /home/user/csv --videos_folder /home/user/videos --destination_folder /home/user/csv_videos

import os
import sys
import argparse
import shutil

parser = argparse.ArgumentParser(description='Copy csv files that have a matching video file to the destination folder.')
parser.add_argument('--csv_folder', type=str, help='Folder with .csv files.', required=True)
parser.add_argument('--videos_folder', type=str, help='Folder with .mp4 videos.', required=True)
parser.add_argument('--destination_folder', type=str, help='Destination folder.', required=True)

args = parser.parse_args()

    
if not os.path.exists(args.csv_folder):
    print("The csv folder does not exist.")
    sys.exit(1)

if not os.path.exists(args.videos_folder):
    print("The videos folder does not exist.")
    sys.exit(1)

if not os.path.exists(args.destination_folder):
    print("The destination folder does not exist.")
    print("Creating destination folder.")
    os.makedirs(args.destination_folder)

    

for csv_file in os.listdir(args.csv_folder):
    csv_file_path = os.path.join(args.csv_folder, csv_file)
    csv_file_name, csv_file_extension = os.path.splitext(csv_file)
    if csv_file_extension == ".csv":
        video_file_name = csv_file_name + ".mp4"
        video_file_path = os.path.join(args.videos_folder, video_file_name)
        if os.path.exists(video_file_path):
            print("Found matching video file: " + video_file_name)
            shutil.copy(csv_file_path, args.destination_folder)
        else:
            print("No matching video file: " + video_file_name)
