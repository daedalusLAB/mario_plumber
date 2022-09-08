import os
import sys
import argparse
import warnings
import pandas as pd
import parselmouth
from feature_extraction_utils import *

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Extract PRAAT features from videos')
parser.add_argument('--videos_folder', type=str, help='Folder with .mp4 videos and gentle information. It look for into subfolder also.', required=True)
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

def get_all_mp4s(videos_folder):
    mp4s = []
    for root, dirs, files in os.walk(videos_folder):
        for file in files:
            if file.endswith(".mp4"):
                mp4s.append(os.path.join(root, file))
    return mp4s


def generate_wavs(videos, destination_folder):
  for mp4 in videos:
    dest_video_name = mp4.split("/")[-1]
    command = "ffmpeg -i " + mp4  + " -q:a 0 -map a " +  os.path.join(destination_folder, dest_video_name.replace(".mp4", ".wav"))
    os.system(command + " > /dev/null 2>&1")


def extract_content(path):
  fps = 1/29.97 # fps needed for extraction
  sound = parselmouth.Sound(path) # Load the file
  df = pd.DataFrame() # create empty df

  # Initializing empty dictionaries which would be used to store praat features of the audio
  attributes = {}
  intensity_second_wise = []
  pitch_second_wise = []

  # Implementation taking from the official repository, here intensity of the audio file is getting extracted
  intensity_attributes1 = get_intensity_attributes(sound,time_step=fps,return_values=True)
  # Function to extract the pitch based attributes 
  pitch_attributes1 = get_pitch_attributes(sound,time_step=fps,return_values=True)

  # Implementation taken from official repository, can check for documentation in feature_extraction_utils file in the cloned repository
  intensity_attributes = intensity_attributes1[0]
  pitch_attributes = pitch_attributes1[0]

  intensity_attributes2 = intensity_attributes1[1]
  pitch_attributes2 = pitch_attributes1[1]

  attributes.update(intensity_attributes)
  attributes.update(pitch_attributes)

  intensity_second_wise.append(intensity_attributes2)
  pitch_second_wise.append(pitch_attributes2)

  return intensity_second_wise, pitch_second_wise


def get_all_wavs(wavs_folder):
  wavs = []
  for root, dirs, files in os.walk(wavs_folder):
      for file in files:
          if file.endswith(".wav"):
              wavs.append(os.path.join(root, file))
  return wavs


def generate_praat_csv(was, destination_folder):
  name = []
  intensity = []
  pitch = []
  for wav in wavs:
    wav_name = wav.split("/")[-1]
    intensity_second_wise, pitch_second_wise = extract_content(wav)
    print(wav_name)
    print(intensity_second_wise)
    print(pitch_second_wise)
    name.append(wav_name)
    intensity.append(intensity_second_wise)
    pitch.append(pitch_second_wise)

  df = pd.DataFrame()
  df['Name'] = name
  df['Intensity'] = intensity
  df['Pitch'] = pitch
  df.to_csv(destination_folder + "/praat_output.csv")
    


print("Starting. I could take a while.")
mp4s = get_all_mp4s(args.videos_folder)
generate_wavs(mp4s, args.destination_folder)
wavs = get_all_wavs(args.destination_folder)
generate_praat_csv(wavs, args.destination_folder)











