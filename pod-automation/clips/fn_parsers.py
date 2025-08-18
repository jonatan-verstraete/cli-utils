import json
from utils import log
from utils import Clip, List, PostQueryResults

def fuzzy_parse_fullTexts(response: str, clip: Clip, retry) -> PostQueryResults:
    """
    Parse an LLM response into highlights and map them back to transcript words.

    Steps:
    1. Try strict json.loads
    2. If that fails, attempt fuzzy extraction:
       - Find first '[' and last ']' in response
       - Extract substring and try json.loads again
    3. Ensure highlights is a list of strings
    4. Fuzzy map each highlight to transcript word indices
    """
    reconstructed_clips: PostQueryResults = []
    highlights: List[str] = []

    # --- Step 1: strict parse
    try:
        highlights = json.loads(response)
    except Exception as e:
        # --- Step 2: fallback parse
        try:
            response = response.replace('\n', '')
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end != -1 and end > start:
                snippet = response[start:end]
                highlights = json.loads(snippet)
            else:
                raise ValueError("No JSON-like brackets found in response")
        except Exception as inner_e:
            log(f"[err] fuzzy_parse_fullTexts: Failed to parse LLM output as JSON ({inner_e})")
            return []

    # --- Step 3: sanitize highlights
    if not isinstance(highlights, list):
        log(f"[err] fuzzy_parse_fullTexts: Parsed output is not a JSON list.")
        if retry:
            retry()
        return []
    highlights = [h for h in highlights if isinstance(h, str)]

    # --- Step 4: fuzzy map
    transcript_words = [word for seg in clip for word in seg["words"]]
    transcript_words_cleaned = [w['word'].lower() for w in transcript_words]

    search_window = 8
    for highlight_text in highlights:
        if len(highlight_text) < 10:
            log(f"[skip] fuzzy_parse_fullTexts: Highlight too short — '{highlight_text[:50]}...'")
            continue

        fuzzy_words = highlight_text.split()
        start_snippet = " ".join(fuzzy_words[:search_window]).lower()
        end_snippet = " ".join(fuzzy_words[-search_window:]).lower()

        start_idx, end_idx = None, None
        for i in range(len(transcript_words_cleaned) - search_window + 1):
            words_slice = " ".join(transcript_words_cleaned[i:i+search_window])
            if start_idx is None and words_slice == start_snippet:
                start_idx = i
                continue
            if start_idx is not None and words_slice == end_snippet:
                end_idx = i
                break

        if start_idx is None or end_idx is None or end_idx <= start_idx:
            log(f"[err] fuzzy_parse_fullTexts: Could not map highlight — '{highlight_text[:30]}...'")
            continue

        reconstructed_clips.append(transcript_words[start_idx:end_idx])

    log(f"[+] fuzzy_parse_fullTexts: Successfully mapped {len(reconstructed_clips)}/{len(highlights)} highlights.")
    return reconstructed_clips



def parse_fullTexts(response: str, clip:Clip):
    """
    Converts an llm output (str) to a list of Words (aka. Word)
    """
    reconstructed_clips: PostQueryResults = []
    highlights: List[str] = []
    try:
        highlights = json.loads(response)
        
        if not isinstance(highlights, list):
            raise ValueError("Output not a JSON list")
        
        highlights = [h for h in highlights if isinstance(h, str)]
        reconstructed_clips = fuzzy_map_text_to_words(highlights, clip)
        
    except Exception as e:
        print(e)
        log(f"[err]: Failed to parse llm JSON: {e}")

    log(f"[+] parse_fullTexts: Successfully parsed {len(reconstructed_clips)}/{len(highlights)} prompts.")
    return reconstructed_clips



def fuzzy_map_text_to_words(highlights: List[str], clip: Clip, search_window: int = 8) -> PostQueryResults:
    """
    Map highlight text back to timestamps by finding the first and last few words
    in the transcript and mapping to their start/end times.

    highlight_text: string from LLM
    search_window: number of words to use from start and end for matching
    """
    reconstructed_clips: PostQueryResults = []
    transcript_words = [word for seg in clip for word in seg["words"]]
    transcript_words_cleaned = [w['word'].lower() for w in transcript_words]
    
    for highlight_text in highlights:
        if len(highlight_text) < 10:
            log(f"[skip] fuzzy_map_text_to_words: Highlight too short to map — '{highlight_text[:50]}...'")
            continue

        fuzzy_words = highlight_text.split(' ')
        start_snippet = " ".join(fuzzy_words[:search_window]).lower()
        end_snippet = " ".join(fuzzy_words[-search_window:]).lower()
        
        start_idx = None
        end_idx = None
        for i in range(len(transcript_words_cleaned) - search_window + 1):
            words_slice = " ".join(transcript_words_cleaned[i:i+search_window])
            if start_idx is None:
                if words_slice == start_snippet:
                    start_idx = i
                    continue
            else:
                if words_slice == end_snippet:
                    end_idx = i
                    break

        if start_idx is None or end_idx is None or end_idx <= start_idx:
            log(f"[err] fuzzy_map_text_to_words: Could not parse/find highlight: '{start_snippet[:10]}' ... '{end_snippet[:-10]}'")
            continue
        
        reconstructed_clips.append(transcript_words[start_idx:end_idx])
    return reconstructed_clips

