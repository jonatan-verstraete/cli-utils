import os
import sys
import json
# import shutil
# import tempfile
import subprocess
from datetime import datetime
from pathlib import Path

import whisperx
# import numpy as np
# from moviepy.video.io.VideoFileClip import VideoFileClip

import ollama
from time import time

from clips.helpers import load_cache, save_cache

# -------- Configs -------- #
CHUNK_CHAR_LEN = 1500  # max chunk len for LLM prompt
OVERLAP = 150          # char overlap between chunks
MAX_CLIPS_PER_CHUNK = 2
MODEL_NAME = "llama3"
TRANSCRIPT_CACHE_DIR = "./cache"


cache_path = os.path.join(TRANSCRIPT_CACHE_DIR, Path('/Users/VJONA/code/cli-utils/pod-automation/clips/test.mp4').stem + ".json")
data = load_cache(cache_path)
segments = data['segments']
for i in segments:
    del i['words']
    
save_cache(os.path.join(TRANSCRIPT_CACHE_DIR, 'test.segments.json'), segments)
# print(segments[0])
    