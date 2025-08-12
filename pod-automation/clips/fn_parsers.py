import json
from utils import log
from utils import Clip, List, PostQueryResults

def parse_fullTexts(response: str, clip:Clip):
    """
    Converts an llm output (str) to a list of Words (aka. Word)
    """
    try:
        highlights = json.loads(response)
        
        if not isinstance(highlights, list):
            raise ValueError("Output not a JSON list")
        
        highlights = [h.strip() for h in highlights if isinstance(h, str) and h.strip()]
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


