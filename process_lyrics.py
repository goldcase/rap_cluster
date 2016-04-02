from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from django.utils.encoding import smart_str, smart_text

import os, re, logging, string, pprint, cPickle

DATA_DIR        = "data"
OUTPUT_DATA_DIR = "processed_data"
STOPWORDS       = stopwords.words("english")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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
    # Remove parentheses and other special characters.
    punctuation = string.punctuation
    for punct in punctuation:
        line = line.replace(punct, "")

    words = line.split(" ")
    ret   = [word for word in words if word not in STOPWORDS]
    ret   = " ".join(ret)
    ret   = ret.strip(" \t\r\n")

    return ret

def scrub_lyrics(lyrics):
    # Remove identifying information and lowercase all words.
    ret = lyrics
    ret = [re.sub("[\[]([\s\S]+?)[\]]", "", line) for line in lyrics]
    ret = [scrub_line(line.lower()) for line in ret]

    # Remove blank lines.
    try:
        ret.remove("\n")
        ret.remove("\r\n")
    except:
        pass

    # Remove empty lines.
    ret = [line for line in ret if line != '']

    return ret

def make_freq_dict(lyrics):
    ret = {}
    flat_lyrics = [word for line in lyrics for word in word_tokenize(line)]

    for word in flat_lyrics:
        if word in ret:
            ret[word] += 1
        else:
            ret[word] = 1

    return ret


def vectorize_lyrics(lyrics):
    scrubbed_lyrics  = scrub_lyrics(lyrics)
    word_frequencies = make_freq_dict(scrubbed_lyrics)

    return word_frequencies

def write_lyrics_to_file(lyrics_dict, song_name, artist):
    assert type(lyrics_dict) is dict

    # Check if the output data path exists and if not, create it.
    if not os.path.isdir(OUTPUT_DATA_DIR):
        os.mkdir(OUTPUT_DATA_DIR)

    artist_path = os.path.join(OUTPUT_DATA_DIR, artist)
    if not os.path.isdir(artist_path):
        os.mkdir(artist_path)

    lyric_path = os.path.join(artist_path, song_name)
    with open(lyric_path, "w") as target:
        str_lyrics = cPickle.dumps(lyrics_dict)
        target.write(str_lyrics)

def decode(line):
    # Get line as unicode.
    return smart_text(line)

# Get all directories in data and begin walking every subdirectory.
dirs_list        = next(os.walk(DATA_DIR))[1]
joined_dirs_list = [os.path.join(DATA_DIR, d) for d in dirs_list]

for subdir in joined_dirs_list:
    # Walk files in every subdirectory.
    for root, dirs, files in os.walk(subdir):
        for file_item in files:
            file_path = os.path.join(subdir, file_item)

            # Read file and vectorize lyrics.
            with open(file_path) as f:
                lyrics = [decode(line) for line in f]

                vectorized_lyrics = vectorize_lyrics(lyrics)
                logging.debug(pprint.pformat(vectorized_lyrics))

                _, artist = os.path.split(subdir)
                write_lyrics_to_file(vectorized_lyrics,
                                     os.path.basename(f.name),
                                     artist)

