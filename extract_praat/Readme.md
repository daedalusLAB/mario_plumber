# Extract PRAAT features

## Description

This tool get as input a folder with mp4 videos and return a folder with wavs of the videos and a csv where each line contains 3 columns with: name of the wav, array of intensity per frame, array of pitch per frame

## Usage

You have to install parselmouth as a requirement to use this tool. 
```
pip install praat-parselmouth
```

After that usage is simple:
```
python extract_praat.py --help

usage: extract_praat.py [-h] --videos_folder VIDEOS_FOLDER [--destination_folder DESTINATION_FOLDER]

Get videos and extract PRAAT features

optional arguments:
  -h, --help            show this help message and exit
  --videos_folder VIDEOS_FOLDER
                        Folder with .mp4 videos and gentle information. It look for into subfolder also.
  --destination_folder DESTINATION_FOLDER
                        Destination folder.
```

