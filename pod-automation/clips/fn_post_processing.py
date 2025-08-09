"""

Post-processing scripts

"""
import ollama

from utils import log
from utils import Clip

def fuzzy_map_text_to_timestamps_simple(highlight_text: str, word_segments: Clip, search_window: int = 8):
    """
    Map highlight text back to timestamps by finding the first and last few words
    in the transcript and mapping to their start/end times.

    highlight_text: string from LLM
    search_window: number of words to use from start and end for matching
    """
    words = highlight_text.strip().split()
    if len(words) < 4:
        log(f"[err]: Highlight too short to map — '{highlight_text[:50]}...'")
        return None

    start_snippet = " ".join(words[:search_window]).lower()
    end_snippet = " ".join(words[-search_window:]).lower()

    transcript_words = [w['text'].lower() for w in word_segments]


    start_idx = None
    end_idx = None    
    for i in range(len(transcript_words) - search_window + 1):
        words_slice = " ".join(transcript_words[i:i+search_window])
        if start_idx is None:
            if words_slice == start_snippet:
                start_idx = i
                continue
        else:
            if words_slice == end_snippet:
                end_idx = i
                break

    if start_idx is None or end_idx is None or end_idx <= start_idx:
        log(f"[err]: Could not parse output for highlight — '{highlight_text[:50]}...'")
        return None

    start_time = word_segments[start_idx]['start']
    end_time = word_segments[end_idx]['end']

    return (start_time, end_time, highlight_text)



def post_clean_obvious_clips(clips:Clip, min_length_sec=5, max_length_sec=60, min_words=8):
    """
    Filter clips based on obvious bad criteria.
    Input: list of slips
    Output: filtered list of slips
    """
    cleaned:Clip = []
    for clip in clips:
        duration = clip['end'] - clip['start']
        if duration < min_length_sec or duration > max_length_sec:
            continue
        if len(clip['text'].split()) < min_words:
            continue
        cleaned.append(clip)
    log(f"[+] post_clean_obvious_clips: {len(cleaned)}/{len(clips)} kept")
    return cleaned



def post_query_filter_relevant_clip(clips, model="llama3"):
    """
    Use a lightweight LLM to decide if a clip is relevant and worth keeping.
    Optionally trim start/end text inside the clip.
    Input: list of slips
    Output: filtered list of slips
    """
    if not clips:
        return []

    filtered = []
    for start, end, text in clips:
        prompt = f"""
Decide if the following podcast clip is interesting enough to keep.
Criteria:
- Emotionally engaging OR intellectually valuable
- Makes sense without outside context
If yes, return "YES".
If no, return "NO".

Clip:
\"\"\"{text}\"\"\"
"""
        resp = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        decision = resp.message.content.strip().upper()
        if decision == "YES":
            filtered.append((start, end, text))
    log(f"[+] post_query_filter_relevant_clip: kept {len(filtered)}/{len(clips)}")
    return filtered
