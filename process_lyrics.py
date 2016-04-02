from nltk.corpus import stopwords
from collections import defaultdict

import os

DATA_DIR = "data"

def is_identifying(line):
    return line.startswith("[") and line.endswith("]\r")

def scrub_line(line):
    ret = line.rstrip("\n")
    print ret

def scrub_lyrics(lyrics):
    lyrics.remove("\n")
    return [scrub_line(line) for line in lyrics]

def vectorize_lyrics(lyrics):
    scrubbed_lyrics = scrub_lyrics(lyrics)
    return scrubbed_lyrics

dirs_list = next(os.walk(DATA_DIR))[1]
joined_dirs_list = [os.path.join(DATA_DIR, d) for d in dirs_list]

for subdir in joined_dirs_list:
    for root, dirs, files in os.walk(subdir):
        for file_item in files:
            file_path = os.path.join(subdir, file_item)

            with open(file_path) as f:
                lyrics = [line for line in f]

            vectorize_lyrics(lyrics)
