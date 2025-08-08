from pathlib import Path
import os, json

# ------------------------------- #
# ----------- consts ------------ #
# ------------------------------- #

DIR_PROJECT = f"{Path(__file__).resolve().parent.parent}/clips"
DIR_CACHE = f"{DIR_PROJECT}/cache"
DIR_OUTPUT = f"{DIR_PROJECT}/output"

os.makedirs(DIR_CACHE, exist_ok=True)
os.makedirs(DIR_OUTPUT, exist_ok=True)


# ------------------------------- #
# ------------ Utils ------------ #
# ------------------------------- #
from time import time, gmtime, strftime


def load_cache(file_path: str) -> str:
    if os.path.exists(file_path):
        print(f"[+] Loaded cache from '{file_path}'")
        with open(file_path, 'r') as f:
            return json.load(f)
    return ''

def save_cache(file_path: str, content: any, append=False) -> None:
    with open(file_path, 'a' if append else 'w') as f:
        json.dump(content, f)
    print(f"[+] Saved cache to '{file_path}'")


def log(content: any, newlines=1) -> None:
    print(content)
    with open(f"{DIR_PROJECT}/logs.txt", 'a') as f:
        f.write('\n' * newlines)
        f.write(str(content))
        # json.dump(content, f, indent=2)

def now() -> str:
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

class timer:
    _timers = {}

    @classmethod
    def start(cls, name: str):
        """Start a timer with the given name."""
        cls._timers[name] = time()

    @classmethod
    def end(cls, name: str) -> str:
        """End the timer with the given name and return the elapsed time as a string."""
        if name not in cls._timers:
            raise RuntimeError(f"Timer '{name}' has not been started.")
        
        start_time = cls._timers.pop(name)
        elapsed = time() - start_time
        return f"{elapsed:.2f}sec"

    @classmethod
    def get(cls, name: str) -> str:
        start_time = cls._timers[name]
        elapsed = time() - start_time
        return f"{elapsed:.2f}sec"


    
# ------------------------------- #
# ----------- Typing ------------ #
# ------------------------------- #
from typing import TypedDict, List, Tuple
from pydantic import BaseModel


class WordSegment(TypedDict):
    word: str
    start: float
    end: float
    score: float

class Segment(TypedDict):
    start: float
    end: float
    text: str
    words: List[WordSegment]

class Transcript(TypedDict):
    segments: List[Segment]
    word_segments: List[WordSegment]

ClipTimestamp = Tuple[float, float]
Segments = List[Segment]


# ---------- Run time ----------- #
class WordSegmentModel(BaseModel):
    word: str
    start: float
    end: float
    score: float

class SegmentModel(BaseModel):
    start: float
    end: float
    text: str
    words: List[WordSegmentModel]

class TranscriptModel(BaseModel):
    segments: List[SegmentModel]
    word_segments: List[WordSegmentModel]
    
