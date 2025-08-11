"""

Post-processing scripts

"""
import ollama
from utils import log
from utils import PostQueryResult, List, AllClips



def post_clean_obvious_clips(all_clips:List[PostQueryResult], min_length_sec=5, max_length_sec=60):
    """
    Filter clips based on obvious bad criteria.
    Input: list of slips
    Output: filtered list of slips
    """
    cleaned:List[PostQueryResult] = []
    for words in all_clips:        
        duration = words[0]['end'] - words[-1]['start']
        if duration < min_length_sec or duration > max_length_sec:
            continue
        cleaned.append(words)
    log(f"[+] POST. post_clean_obvious_clips: {len(cleaned)}/{len(all_clips)} clips left")
    return cleaned


# TODO: update me once more to become relevant ot this code base pls :)
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
If yes, reply "YES".
If no, reply "NO".

Clip:
\"\"\"{text}\"\"\"
"""
        resp = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        decision = resp.message.content.strip().upper()
        if "YES" in  decision and not "NO" in decision:
            filtered.append((start, end, text))
    log(f"[+] POST. post_query_filter_relevant_clip:  {len(filtered)}/{len(clips)} clips left")
    return filtered
