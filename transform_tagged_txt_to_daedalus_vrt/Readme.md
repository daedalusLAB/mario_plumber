# Transform vrt to new daedalus format
Given a 'Red Hen' tagged file, this script will transform it into a new daedalus format. The new format is a tab separated file with the following columns:

1. text: text of the word
2. pos: part of speech of the word
3. lemma: lemma of the word
4. lemma_pos: lemma + pos
5. lower: lower case of the word
6. prefix: prefix of the word
7. suffix: suffix of the word
8. is_digit: is the word a digit
9. like_num: is the word a number
10. dep: dependency of the word
11. shape: shape of the word
12. tag: tag of the word
13. sentiment: sentiment of the word
14. is_alpha: is the word alphanumeric
15. is_stop: is the word a stop word
16. head: head of the word
17. head_pos: part of speech of the head of the word
18. children: children of the word
19. start_sec: start time of the word in seconds
20. start_msec: start time of the word in milliseconds
21. end_sec: end time of the word in seconds
22. end_msec: end time of the word in milliseconds


We also make a contextual spellchecker of the file if you like

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_trf
python -m spacy download es_dep_news_trf
```

## Usage
```
./transform_tagged_txt_to_daedalus_vrt.py --help
usage: transform_tagged_txt_to_daedalus_vrt.py [-h] --input INPUT [--language LANGUAGE] [--spellcheck SPELLCHECK]

options:
  -h, --help            show this help message and exit
  --input INPUT         Input file or directory containing tagged files
  --language LANGUAGE   Language of the input file
  --spellcheck SPELLCHECK
                        True if you want to spellcheck the transcription
```






