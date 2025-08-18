import json, ollama

from utils import log, timer, load_cache, save_cache, slugify
from utils import Clip, AllClips
from utils import DIR_CACHE

from fn_parsers import fuzzy_parse_fullTexts



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



def query_fulltext(chuck: Clip, model_name: str, options: dict, use_cache=False, retry_count = 0):
    raw_text = " ".join([seg['text'].lower() for seg in chuck])
    prompt = f"""
    Your task is to identify impactful excerpts from the following text. 

    - Extract short, self-contained excerpts of exactly 30 words that are emotionally engaging or convey a key insight. 
    - These excerpts should be clear, attention-grabbing, and meaningful on their own.
    - The excerpts should feel impactful, exciting, thought-provoking, or funny.

    Return ONLY the excerpts in valid JSON format, like this:
    ["excerpt 1", "excerpt 2", "excerpt 3"]

    If no suitable excerpts exist, return [].

    Text:
    ```{raw_text}```
    """ 

    # 3 — Query LLM
    timer.start("LLM")
    content:str = ""
    path_cache_current_prompt = f"{DIR_CACHE}/cached_output_{slugify(model_name, '')}_{slugify(raw_text[:20], '')}.txt"
    if use_cache:
        content = load_cache(path_cache_current_prompt)
        if not content:
            log('[ERR]: query. Failed to load cached, resume with prompt.')
            
    if not content:
        chat_response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert at identifying impactful excerpts from text."},
                {"role": "user", "content": prompt}
            ],
            options=options
        )
        content = chat_response.message.content
        save_cache(path_cache_current_prompt, content)
        
    log(f"[+] query_fulltext. Took {timer.end('LLM')} ({len(prompt)} chars)")
    
    def retry():
        log(f"[+] Retry query: {retry_count}")
        query_fulltext(chuck, model_name, options, False, retry_count - 1)
    
    return fuzzy_parse_fullTexts(content, chuck, retry if retry_count is not 0 and use_cache is True else None)

    
    
    
    

