 # Download Videos 

 Simple script to download videos given a .csv file like this [csv](https://raw.githubusercontent.com/daedalusLAB/mario_plumber/main/download_videos/wherever_it_will_be.csv?token=GHSAT0AAAAAABSEAMXQSP4RVK6NWYLTY6SSYRLGGEQ)

 ```
usage: download_videos.py [-h] --csv CSV --destination DESTINATION

Download videos from a .csv file.

optional arguments:
  -h, --help                show this help message and exit
  --csv CSV                 The .csv file.
  --destination DESTINATION The destination folder.
 
 ```

 ```
Example:
download_videos.py --csv /home/user/videos.csv --destination /home/user/videos
 ```
