# Mario Plumber
This repo contains tools to help in our day to day work.

# Tools

## clips
    
### generate_clips.py 

Given a folder with videos and gentle information, a text, and a destination folder,this script will crop the videos seconds containing the text in gentle info, and save them to the destination folder.

```
./generate_clips.py --help
usage: generate_clips.py [-h] --videos_folder VIDEOS_FOLDER --text TEXT [--seconds_before SECONDS_BEFORE] [--seconds_after SECONDS_AFTER] [--destination_folder DESTINATION_FOLDER]

Crop videos seconds containing the text in gentle info, and save them to the destination folder.

optional arguments:
  -h, --help            show this help message and exit
  --videos_folder VIDEOS_FOLDER
                        Folder with .mp4 videos and gentle information. It look for into subfolder also.
  --text TEXT           Text to search for in the video.
  --seconds_before SECONDS_BEFORE
                        Number of seconds to crop before first word expression.
  --seconds_after SECONDS_AFTER
                        Number of seconds to crop after first word expression.
  --destination_folder DESTINATION_FOLDER
                        Destination folder.
```


### Example:
```
generate_clips.py --videos_folder /home/user/videos --text "text to search for" --seconds_before 3 --seconds_after 5 --destination_folder /home/user/crop_videos
``` 


## copycsv

### copycsv.py

Copy csv files that have a matching video file to the destination folder.

```
usage: copycsv.py [-h] --csv_folder CSV_FOLDER --videos_folder VIDEOS_FOLDER --destination_folder DESTINATION_FOLDER

Copy csv files that have a matching video file to the destination folder.

optional arguments:
  -h, --help            show this help message and exit
  --csv_folder CSV_FOLDER
                        Folder with .csv files.
  --videos_folder VIDEOS_FOLDER
                        Folder with .mp4 videos.
  --destination_folder DESTINATION_FOLDER
                        Destination folder.
```

### copyfromcsvfile.py

Copy videos that have a matching filename in the csv file to the destination folder.


```
./copyfromcsvfile.py --help
usage: copyfromcsvfile.py [-h] --input_csv INPUT_CSV --videos_folder VIDEOS_FOLDER --destination_folder DESTINATION_FOLDER

Copy videos that have a matching filename in the csv file to the destination folder.

optional arguments:
  -h, --help            show this help message and exit
  --input_csv INPUT_CSV
                        Input csv file.
  --videos_folder VIDEOS_FOLDER
                        Folder with .mp4 videos.
  --destination_folder DESTINATION_FOLDER
                        Destination folder.

```
