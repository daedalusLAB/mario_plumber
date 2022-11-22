#!/usr/bin/env python3

import sys
import argparse
import spacy
import contextualSpellCheck

import re
import os

def load_spacy_model(language, spellcheck):
  if language == 'es':
    # load spanish transformer spacy model
    nlp = spacy.load('es_dep_news_trf')
    if (spellcheck):
      print('Loading contextual spell check model for spanish...')
      nlp.add_pipe(
        "contextual spellchecker",
        config={
          "model_name": "dccuchile/bert-base-spanish-wwm-cased",
          "max_edit_dist": 2,
        },
      )
  else:
    # load english transformer spacy model
    nlp = spacy.load('en_core_web_trf')
    if (spellcheck):
      print('Loading contextual spell check model for english...')
      nlp.add_pipe("contextual spellchecker")
  return nlp

def clean_html(raw_html):
  CLEANR = re.compile('<.*?>') 
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext


def parse_vrt_file_to_transcription(vrt_file):
  # read vrt file lines 
  transcription = ''
  with open(vrt_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
      # take first word of each line
      word = line.split(' ')[0]
      if word == '#' or word == ' ' or word == '\n':
        continue
      else:
        transcription += word + ' '

  transcription = clean_html(transcription)
  # remove all \n from transcription
  transcription = transcription.replace('\n', '')
  # remove multiple spaces
  transcription = re.sub(' +', ' ', transcription)
  # before punctuation no space 
  transcription = re.sub(' ([.,!?()])', r'\1', transcription)

  return transcription

# Parse data from file name expecting a filename as this: 2016-01-01_0000_US_MSNBC_Hardball_with_Chris_Matthews.mp4
def parse_file(file):
  # file without extension and path
  filename = file.split('/')[-1].split('.')[0]
  # sub - for _ in filename
  filename = filename.replace('-', '_')  
  filename_with_ext = file.split('/')[-1]
  # filename with extension: 2016-01-01_0000_US_MSNBC_Hardball_with_Chris_Matthews.mp4
  # date and time: 2016-01-01_0000
  date_time = filename_with_ext.split('_')[0] + '_' + filename_with_ext.split('_')[1]
  # channel: MSNBC
  channel = filename_with_ext.split('_')[3]
  # title: Hardball_with_Chris_Matthews from 2016-01-01_0000_US_MSNBC_Hardball_with_Chris_Matthews.mp4
  title = '_'.join(filename_with_ext.split('_')[4:]).split('.')[0]  
  # year: 2016
  year = date_time.split('-')[0]
  # month: 01
  month = date_time.split('-')[1]
  # day: 01
  day = date_time.split('-')[2].split('_')[0]
  # time: 0000
  time = date_time.split('-')[2].split('_')[1]
  return filename, filename_with_ext, date_time, channel, title, year, month, day, time
    
def create_vrt_file(file, language, spellcheck):
  print("Generating transcription from VRT file...")
  transcription = parse_vrt_file_to_transcription(file)
  print("Correcting spelling and Generating spacy doc...")
  doc = nlp(transcription)

  # file = 2021-01-01_1700_US_KMEX_Noticiero_Univisión_Edición_Digital_tagged.txt 
  # get file2 = 2021-01-01_1700_US_KMEX_Noticiero_Univisión_Edición_Digital.mp4
  file2 = file.split('_tagged')[0] + '.mp4'
  # unicode to ascii file2
  file2 = file2.encode('ascii', 'ignore').decode('ascii') 


  print('Writing to vrt file...')
  vrt_file = open(file2 + '.daedalus_vrt', 'w')
  filename, filename_with_ext, date_time, channel, title, year, month, day, time = parse_file(file2)
  vrt_file.write('<text id="' + filename  +  '" '  + 'file="' + filename_with_ext + '" '  + ' language="' + args.language + '" ' +
      'collection="Daedalus Test" ' + 'date="' + date_time + '" ' + 'channel="' + channel + '" ' + 'title="' + title + '" ' + 'year="' + year + '" ' + 'month="' + month + '" ' + 'day="' + day + '" ' + 'time="' + time + '" ' + '>\n')  
  vrt_file.write('<story>\n')
  vrt_file.write('<turn>\n')
  last_start = 0
  last_end = 0
  last_token = ''
  sentence_id = 0
  for sent in doc.sents:
      sentence_id += 1
      vrt_file.write('<s id="' + str(sentence_id) + '" ' + 'file="' + filename + '" ' +     
      'reltime="0" ' + " >\n")
      for token in sent:
        vrt_file.write(token.text + " \t " + token.pos_  +  " \t " + token.lemma_  +  " \t " + token.lemma_ + "_" + token.pos_  + " \t " + token.lower_ + " \t " + 
          token.prefix_ + " \t " + token.suffix_  +  " \t " + str(token.is_digit) + " \t " + str(token.like_num) + " \t " + 
          token.dep_ + " \t " + token.shape_ + " \t " + token.tag_ + " \t "  +  str(token.sentiment) + " \t " +
          str(token.is_alpha) + " \t " +  str(token.is_stop) + " \t " +  token.head.text + " \t " +  
          token.head.pos_ + " \t " +  str([child for child in token.children]) + " \t " + 
          "0" + " \t " + "0" + " \t " + "0" + " \t " + "0" + "\n")
      vrt_file.write("</s>\n")
  vrt_file.write('</turn>\n')
  vrt_file.write('</story>\n')
  vrt_file.write("</text>\n")
  vrt_file.close()



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", help="Input file or directory containing tagged files", required=True)
  parser.add_argument("--language", help="Language of the input file", default='es')
  parser.add_argument("--spellcheck", help="True if you want to spellcheck the transcription", default=False)
  args = parser.parse_args()
  
  print("Loading spacy model...")
  nlp = load_spacy_model(args.language, args.spellcheck)

  # remove / from end of input path
  if args.input[-1] == '/':
    args.input = args.input[:-1]

  # if input is a folder loop over all older and subfolders
  if os.path.isdir(args.input):
    for root, dirs, files in os.walk(args.input):
      for file in files:
        if file.endswith('_tagged.txt'):
          print("Processing file: " + file)
          create_vrt_file(os.path.join(root, file), args.language, args.spellcheck)
  else:
    print("Processing file: " + args.input)
    create_vrt_file(args.input, args.language, args.spellcheck)

  

