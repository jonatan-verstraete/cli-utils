import json 

from utils import log, timer
from utils import Clip
from fn_post_processing import fuzzy_map_text_to_timestamps_simple

def get_prompt(transcript_chuck: Clip, type: str) -> str:
    match type:
        case 'sentence':
            return prompt_sentences(transcript_chuck)
        case 'full_text':
            return query_fulltext(transcript_chuck)
        case _:
            print('Not a valid type of prompt requested')
            exit()




def prompt_sentences(transcript_chuck:Clip) -> str:
    simplifiedTranscript = "\n".join([f"({i['start']}-{i['end']}): {i['text']}" for i in transcript_chuck])
    return  f"""
You are an expert video editor for viral podcast clips.

You are given a chunk of podcast transcript with precise timestamps. Your task is to identify 0 to 4 emotionally or intellectually impactful highlights. Each highlight should:
- Be between 10 and 25 seconds long
- Contain meaningful insight, emotional depth, humor, tension, or dramatic storytelling
- Start and end on complete thoughts (don't cut mid-sentence)
- Be **self-contained**: the clip should make sense on its own without needing additional context

Avoid selecting punchlines or conclusions without the setup — each highlight must include enough context to be understood independently.

**Input format (timestamped transcript):**
([start_time]-[end_time]): Spoken text

**Expected output:**
A JSON array of [start_time, end_time] pairs — only include the highlights.
- Times must match those in the transcript
- Return ONLY the array, with no extra comments

If **no suitable highlights** are found in the transcript, confidently return an empty array: []
Do not force a result if nothing meaningful fits the criteria.

**Example output with 2 highlights:**
[[123.1, 140.3], [325.2, 347.9]]

**Example output with 0 highlights:**
[]

Transcript:
```json
{simplifiedTranscript}
```
"""






from pathlib import Path

def query_fulltext(
    chunk: Clip,
    model_name: str,
    options: dict
) -> Clip:
    """
    Query an LLM with raw text from a chunk of transcript (Clip) to get highlight clips.
    Output: Clip (subset of original chunk) or [] if none.

    Steps:
    1. Convert chunk to raw text (no timestamps)
    2. Prompt LLM to find 0–N clips
    3. Parse output: for each highlight, find start and end in chunk word_segments
    4. Return list of Clip for each highlight
    """
    log(f"[+] query_fulltext: processing chunk of {len(chunk)} segments")

    # 1 — Convert to raw text
    raw_text = " ".join([seg['text'] for seg in chunk])

    # 2 — Build prompt
    prompt = f"""
You are an expert podcast highlight selector.

You will be given a continuous block of podcast transcript text (no timestamps). 
Identify 0 to 4 emotionally or intellectually impactful highlights that:
- Are between 10 and 25 seconds long
- Make sense when viewed alone (self-contained, with enough setup and payoff)
- Contain meaningful insight, humor, tension, or emotional impact

Return ONLY the highlighted text excerpts, as a JSON array of strings.
If no highlights are found, return [].

Transcript:
\"\"\"{raw_text}\"\"\"
"""

    # 3 — Query LLM
    timer.start("LLM")
    chat_response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a podcast highlight extractor."},
            {"role": "user", "content": prompt}
        ],
        options=options
    )
    log(f"[+] query_fulltext: LLM call took {timer.end('LLM')}")

    # 4 — Parse JSON output → list[str]
    try:
        highlights = json.loads(chat_response.message.content.strip())
        if not isinstance(highlights, list):
            raise ValueError("Output not a JSON list")
        highlights = [h.strip() for h in highlights if isinstance(h, str) and h.strip()]
    except Exception as e:
        log(f"[err]: Failed to parse highlights JSON: {e}")
        return []

    if not highlights:
        log("[+] query_fulltext: No highlights returned")
        return []

    # 5 — For each highlight, map to Clip
    mapped_segments: Clip = []
    for htext in highlights:
        res = fuzzy_map_text_to_timestamps_simple(htext, get_word_segments_from_chunk(chunk))
        if res:
            start_time, end_time, _ = res
            clip_segments = get_segments_by_time_range(chunk, start_time, end_time)
            if clip_segments:
                mapped_segments.extend(clip_segments)
            else:
                log(f"[err]: Could not map highlight to segments — '{htext[:50]}...'")

    log(f"[+] query_fulltext: returning {len(mapped_segments)} mapped segments")
    return mapped_segments


def get_word_segments_from_chunk(chunk: Clip) -> List[WordSegment]:
    """Flatten all word entries from a chunk of Clip."""
    words = []
    for seg in chunk:
        words.extend(seg.get('words', []))
    return words


def get_segments_by_time_range(chunk: Clip, start: float, end: float) -> Clip:
    """Return all Clip in the given time range."""
    return [seg for seg in chunk if seg['end'] >= start and seg['start'] <= end]