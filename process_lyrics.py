from nltk.corpus import stopwords
from collections import defaultdict

import os

DATA_DIR = "data"
OUPUT_DATA_DIR = "processed_data"

def is_identifying(line):
    """
    Determines whether the line passed into this method contains potentially
    identifying information which may pollute clustering with artist information
    encoded in a song.

    Parameters
    ----------
    line : str
        A line of a lyric. Identifying information generally is enclosed within
        square brackets.
    """
    return line.startswith("[") and line.endswith("]\r")

def scrub_line(line):
    ret = line.rstrip("\n")
    return ret

def scrub_lyrics(lyrics):
    lyrics.remove("\n")
    return [scrub_line(line) for line in lyrics if not is_identifying(line)]

def vectorize_lyrics(lyrics):
    scrubbed_lyrics = scrub_lyrics(lyrics)
    return scrubbed_lyrics

dirs_list = next(os.walk(DATA_DIR))[1]
joined_dirs_list = [os.path.join(DATA_DIR, d) for d in dirs_list]

def write_lyrics_to_file(lyrics, artist):

for subdir in joined_dirs_list:
    for root, dirs, files in os.walk(subdir):
        for file_item in files:
            file_path = os.path.join(subdir, file_item)

            with open(file_path) as f:
                lyrics = [line for line in f]

            vectorized_lyrics = vectorize_lyrics(lyrics)

