import json, ollama

from utils import log, timer, load_cache, save_cache, slugify
from utils import Clip, AllClips
from utils import DIR_CACHE

from fn_parsers import parse_fullTexts



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



def query_fulltext(chuck: Clip, model_name: str, options: dict, use_cache=False):
    """
    Query an LLM with raw text from a chunk of transcript (Clip) to get highlight clips.
    Output: Clip (subset of original chunk) or [] if none.

    Steps:
    1. Convert chunk to raw text (no timestamps)
    2. Prompt LLM to find 0-N clips
    3. Parse output: for each highlight, find start and end in chunk word_segments
    4. Return list of Clip for each highlight
    """

    raw_text = " ".join([seg['text'].lower() for seg in chuck])
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
    content:str = ""
    path_cache_current_prompt = f"{DIR_CACHE}/cached_output_{slugify(model_name, '')}_{slugify(raw_text[:20], '')}.txt"
    if use_cache:
        cached = load_cache(path_cache_current_prompt)
        if cached and isinstance(cached, list):
            content = cached
        else:
            log('ERR]: query. Failed to load cached, resume with prompt.')
            
    if not content:
        chat_response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a professional podcast highlight extractor."},
                {"role": "user", "content": prompt}
            ],
            options=options
        )
        content = chat_response.message.content
        save_cache(path_cache_current_prompt, content)
        
    log(f"[+] query_fulltext. Took {timer.end('LLM')} ({len(prompt)} chars)")
    
    return parse_fullTexts(content, chuck)

    