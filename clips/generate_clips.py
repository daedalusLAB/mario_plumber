#!/usr/bin/env python3

# generate_clips.py 
#    Given a folder with videos and gentle information, a text, and a destination folder,
#    this script will crop the videos seconds containing the text in gentle info, and save them to the destination folder.
#
#    Example:
#    generate_clips.py --videos_folder /home/user/videos --text text --seconds_before number_of_seconds --seconds_after number_of_seconds --destination_folder /home/user/crop_videos

import os
import sys
import argparse
import pandas as pd
import gzip
import warnings

warnings.filterwarnings('ignore')



parser = argparse.ArgumentParser(description='Crop videos seconds containing the text in gentle info, and save them to the destination folder.')
parser.add_argument('--videos_folder', type=str, help='Folder with .mp4 videos and gentle information. It look for into subfolder also.', required=True)
parser.add_argument('--text', type=str, help='Text to search for in the video.', required=True)
parser.add_argument('--seconds_before', type=int, help='Number of seconds to crop before first word expression.', default=3)
parser.add_argument('--seconds_after', type=int, help='Number of seconds to crop after first word expression.', default=5)
parser.add_argument('--destination_folder', type=str, help='Destination folder.', default="videos_output")

args = parser.parse_args()

    
# Check that folder exists
if not os.path.exists(args.videos_folder):
    print("The 'videos folder' does not exist.")
    sys.exit(1)

# if destination folder exists, exit.
if os.path.exists(args.destination_folder): 
    print("The 'destination folder' already exists. Please, remove it or use a different name.")
    sys.exit(1)


if not os.path.exists(args.destination_folder):
    print("Creating destination folder.")
    os.makedirs(args.destination_folder)


# get cut times of a video containing n word searching text and return list with exact second 
# where the first word of text is found.
# Imagine this gentle output:
# [1st match "whole debate"]
#  string  Time
# whole   2125.059
# debate  2125.088
# was     2126.030
#
## [2nd match "whole debate"]
# string  Time
# whole   2133.004
# debate  2133.032
# ,       2133.077
# 
# [3]
# string  Time
# whole   2150.060
# debate  2150.089
# rises   2151.030

# example: get_cut_times("2016-01-18_1500_US_CNN_Newsroom.v4.vrt.gz", "whole") - return: [398.039, 1800.052, 2125.059, 2133.004, 2150.06, 2483.044, 2675.048]
# example: get_cut_times("2016-01-18_1500_US_CNN_Newsroom.v4.vrt.gz", "whole debate") - return: [2125.059, 2133.004, 2150.06]
# example: get_cut_times("2016-01-18_1500_US_CNN_Newsroom.v4.vrt.gz", "whole debate rises") - return: [2150.06]
def get_cut_times(video, search_text):
    cutting_times = {}
    try:
        # read file and delete lines starting with "<"
        f = gzip.open(video,"rt")
        lines = f.readlines()
        lines = [line for line in lines if not line.startswith('<')]
        f.close()
        # create a list from lines using "\t" as separator
        lines = [line.split("\t") for line in lines]
        gentle = pd.DataFrame(lines)
        # Selection on important columns
        selection1 = gentle.iloc[:, [0, 51, 52 ]]
        # rename columns to "string", "second" and "milisecond"
        selection1.columns = ["string", "second", "milisecond"]
        words = search_text.split(" ")
        # get rows with conditions. consecutive words must be in consecutive rows
        for i in range(len(words)):
            if i == 0:
                cond = selection1["string"].eq(words[i])
            else:
                cond = cond & selection1["string"].shift(-1*i).eq(words[i])
        cutting_times = selection1[cond]
        # Create new column in cutting_times called "cutTime" with the value of second + milisecond * 0.001.
        cutting_times["second"]     = cutting_times["second"].apply(lambda x: float(x))
        cutting_times["milisecond"] = cutting_times["milisecond"].apply(lambda x: float(x) * 0.0001)
        cutting_times["cutTime"] = cutting_times["second"] + cutting_times["milisecond"]
    except:
        print("Error: " + video)
        cutting_times["cutTime"] = []
    return list(cutting_times["cutTime"])

    
# get a list of all .vrt.gz files in the videos folder and subfolders and return a list of strings with the names of the files.
def get_all_vrts(videos_folder):
    vrts = []
    for root, dirs, files in os.walk(videos_folder):
        for file in files:
            if file.endswith("v4.vrt.gz"):
                vrts.append(os.path.join(root, file))
    return vrts


# loop over vrts and get cut times for each one passing text argument
# and generate a dictionary with the video name as key and the list of cut times as value.
def get_all_cut_times(vrts, text):
    # create dictionary with video name as key and list of cut times as value
    cut_times = {}
    for vrt in vrts:
        cut_times[vrt] = get_cut_times(vrt, text)
    return cut_times

# loop over cut_times and crop the video using the cut times and save it to the destination folder.
# Use ffmpeg to crop the video.
def crop_videos(cut_times, destination_folder, seconds_before, seconds_after, text):
    for vrt in cut_times:
        # sub spaces in text from underscores
        text = text.replace(" ", "_")
        # get the name of the video. Remove v4.vrt.gz from the name and add .mp4 extension
        video_name = vrt.replace("v4.vrt.gz", "mp4")
        # get the list of cut times
        cut_times_list = cut_times[vrt]
        # loop over the list of cut times and crop the video
        for i in range(len(cut_times_list)):
            # get the cut time
            cut_time = cut_times_list[i]
            # get the start time of the clip
            start_time = cut_time - args.seconds_before
            # extract file name from video name
            dest_video_name = video_name.split("/")[-1]
            # check if video_name file exists.
            if os.path.exists(video_name):
                print("Cropping video: " + video_name)
                # create the command to crop the video and generate a new .mp4 video 
                command = "ffmpeg -ss " + str(start_time) + " -t " + str(seconds_before + seconds_after)  + " -i " + video_name  + " -c copy " + os.path.join(destination_folder, dest_video_name.replace(".mp4", "_" + str(i) + "_" + text + ".mp4"))
                # execute the command without console output
                # print(command)
                os.system(command + " > /dev/null 2>&1")
            else:
                print("*** ERROR: The video file ' " + video_name + "' does not exist. ***")
                
            



print("Starting. I could take a while.")
print("Generating list of all .v4.vrt.gz files in the videos folder.")
vrts = get_all_vrts(args.videos_folder)
print("Found " + str(len(vrts)) + " .v4.vrt.gz files.")
print("Looking for text in the videos.")
cut_times = get_all_cut_times(vrts, args.text)

# Print number of keys of cut_times keys where the value is not empty:
videos_WITH_text = {k: v for k, v in cut_times.items() if v}
print("Found " + str(len(videos_WITH_text)) + " videos with the text '" + args.text + "'.")
print("Cropping videos.")
crop_videos(cut_times, args.destination_folder, args.seconds_before, args.seconds_after, args.text)
print("Done.")
sys.exit(0)



