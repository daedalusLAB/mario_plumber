#!/usr/bin/env python3

# download_videos.py --csv <csv.file> --destination <destination folder> 
#    Given a .cvs file, download all files with wget (column 7) to the destination folder.
#
#    Example:
#    download_videos.py --csv /home/user/videos.csv --destination /home/user/videos

import os
import argparse


parser = argparse.ArgumentParser(description='Download videos from a .csv file.')
parser.add_argument('--csv', type=str, help='The .csv file.', required=True)
parser.add_argument('--destination', type=str, help='The destination folder.', required=True)

args = parser.parse_args()

# Create destination folder if doesn't exist
if not os.path.exists(args.destination):
    print("The destination folder does not exist.")
    print("Creating destination folder.")
    os.makedirs(args.destination)

# Read csv file and skip first line and empty lines.
# Download all videos in column 5.
with open(args.csv, 'r') as csv_file:
    # skip 2 first lines
    csv_file.readline()
    csv_file.readline()
    for line in csv_file:
        if line.startswith(','):
            continue
        if line.strip() == '':
            continue
        line_split = line.split(',')
        wgetline = line_split[7]
        url = wgetline.split(' ')[3]
        # delete quotes of url
        url = url.replace('"', '')
        filename = wgetline.split(' ')[2]
        print("Downloading: " + url + " to " + filename)
        #('wget -O ' + os.path.join(args.destination, filename) + " \"" +  url  + "\"")
        os.system('wget -O ' + os.path.join(args.destination, filename) + " \"" +  url  + "\"")

