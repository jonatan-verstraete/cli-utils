# LEARN
# - https://dev.to/saranshabd/python-w-strict-typechecker-3l7g
# - https://www.linkedin.com/pulse/demystifying-llm-quantization-suffixes-what-q4km-q80-q6k-paul-ilves-i0yvf



from pathlib import Path
import os, re
from utils import log, now
from utils import DIR_PROJECT, DIR_CACHE, DIR_OUTPUT

from fn_chuck import chunk_by_time
from fn_query import query_fulltext 
from fn_transcribe import transcribe_with_whisperx
from fn_post_processing import fuzzy_map_text_to_timestamps_simple, post_clean_obvious_clips, post_query_filter_relevant_clip



# -------- Configs -------- #

# MODEL_NAME = "llama3" # no-long-context, mehmeh-quality
# MODEL_NAME = "qwen2.5:7b-instruct-q4_K_M" # meh-quality-clips
MODEL_NAME = "yi:9b-chat-v1.5-q6_K" # +long context, meh_ok-quality, 
# MODEL_NAME = "spooknik/hermes-2-pro-mistral-7b:q8" # ..


print(re.sub('[^\w','', MODEL_NAME))
exit()

# TRY: MythoMax-L2
# TRY?: OpenChat 3.6

# -uncensored

# ------- variable config ------- #
#  should be in flow or param
arg_video_path=f'{DIR_PROJECT}/pod mark Coleman.mp4'
arg_video_path=f'{DIR_PROJECT}/pod car dude.mp4'

guest_name=Path(arg_video_path).name.split('.mp4')[0] or "Unknown Guest"


use_cached_transcription=False # won't redo transcribe
used_cached_llm_output=False # won't redo prompts (only useful if you are testing clips)


def main():
    assert os.path.exists(arg_video_path), f"File not found: {arg_video_path}"
    log('', 2)
    log(f"Start: {now()}")
    log(f"[+] Start processing for '{guest_name}'")    
    transcription = transcribe_with_whisperx(arg_video_path, guest_name, use_cached_transcription)
    word_segments = transcription['word_segments']

    chunks = chunk_by_time(word_segments, minutes=10)

    all_clips = []
    for chunk in chunks:
        # Step 1 — Query full text
        raw_text = " ".join([w['text'] for w in chunk])
        highlights = query_fulltext(raw_text)  # returns list of strings

        # Step 2 — Map back to timestamps
        mapped = []
        for h in highlights:
            res = fuzzy_map_text_to_timestamps_simple(h, word_segments)
            if res:
                mapped.append(res)

        # Step 3 — Basic cleaning
        mapped = post_clean_obvious_clips(mapped)
        all_clips.extend(mapped)

    # Step 4 — Optional ranking
    # all_clips = post_rank_top(all_clips, 10)

    # Step 5 — Optional LLM-based relevance filtering
    all_clips = post_query_filter_relevant_clip(all_clips)

    # Step 6 — Final clean
    all_clips = post_clean_obvious_clips(all_clips)

    # Step 7 — Save to file (no cutting yet)
    out_path = Path(DIR_OUTPUT) / f"output_{MODEL_NAME.replace(':','_')}_{guest_name}.txt"
    with open(out_path, "w") as f:
        for start, end, text in all_clips:
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
    log(f"[v] Done! Saved output to {out_path}")
    


if __name__ == "__main__":
    main()
