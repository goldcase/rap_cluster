from nltk.corpus import stopwords
from collections import defaultdict

import os, re

DATA_DIR = "data"
OUTPUT_DATA_DIR = "processed_data"

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
    return line.startswith("[") and line.endswith("]")

def scrub_line(line):
    ret = line.strip(" \t\r\n")
    return ret

def scrub_lyrics(lyrics):
    ret = [line for line in lyrics]
    ret = [re.sub("[\[]([\s\S]+?)[\]]", "", line) for line in lyrics]
    ret = [scrub_line(line.lower()) for line in ret]
    try:
        lyrics.remove("\n")
        lyrics.remove("\r\n")
    except:
        pass

    ret = [line for line in ret if line != '']
    return ret

def vectorize_lyrics(lyrics):
    scrubbed_lyrics = scrub_lyrics(lyrics)
    return scrubbed_lyrics

def write_lyrics_to_file(lyrics, song_name, artist):
    if not os.path.isdir(OUTPUT_DATA_DIR):
        os.mkdir(OUTPUT_DATA_DIR)

    artist_path = os.path.join(OUTPUT_DATA_DIR, artist)

    if not os.path.isdir(artist_path):
        os.mkdir(artist_path)

    lyric_path = os.path.join(artist_path, song_name)

    with open(lyric_path, "w") as target:
        str_lyrics = "\n".join(lyrics)
        target.write(str_lyrics)

dirs_list = next(os.walk(DATA_DIR))[1]
joined_dirs_list = [os.path.join(DATA_DIR, d) for d in dirs_list]

for subdir in joined_dirs_list:
    for root, dirs, files in os.walk(subdir):
        for file_item in files:
            file_path = os.path.join(subdir, file_item)

            with open(file_path) as f:
                lyrics = [line for line in f]

                vectorized_lyrics = vectorize_lyrics(lyrics)
                _, artist = os.path.split(subdir)
                write_lyrics_to_file(vectorized_lyrics,
                                     os.path.basename(f.name),
                                     artist)

