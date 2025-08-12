# LEARN
# - https://dev.to/saranshabd/python-w-strict-typechecker-3l7g
# - https://www.linkedin.com/pulse/demystifying-llm-quantization-suffixes-what-q4km-q80-q6k-paul-ilves-i0yvf



from pathlib import Path
import os, re
from utils import log, now
from utils import DIR_PROJECT, LLM_OPTIONS
from utils import List, PostQueryResults

from fn_chuck import chunk_by_time
from fn_query import query_fulltext 
from fn_save_clips import cut_and_save_clips, output_text
from fn_transcribe import transcribe_with_whisperx
from fn_post_processing import post_clean_obvious_clips, post_query_filter_relevant_clip


# -------- Configs -------- #

# MODEL_NAME = "llama3" # no-long-context, mehmeh-quality
# MODEL_NAME = "qwen2.5:7b-instruct-q4_K_M" # meh-quality-clips
MODEL_NAME = "yi:9b-chat-v1.5-q6_K" # +long context, meh_ok-quality, 
# MODEL_NAME = "spooknik/hermes-2-pro-mistral-7b:q8" # ..




# TRY: MythoMax-L2
# TRY?: OpenChat 3.6

# -uncensored

# ------- variable config ------- #
#  should be in flow or param
arg_video_path=f'{DIR_PROJECT}/pod mark Coleman.mp4'
arg_video_path=f'{DIR_PROJECT}/pod car dude.mp4'

guest_name=Path(arg_video_path).name.split('.mp4')[0] or "Unknown Guest"


use_cached_transcription=True # won't redo transcribe
# used_cached_llm_output=False # won't redo prompts (only useful if you are testing clips)


def main():
    assert os.path.exists(arg_video_path), f"File not found: {arg_video_path}"
    log('', 2)
    log(f"{now()}: Start processing for '{guest_name}'")
    # Step 1 — transcribe video
    transcription = transcribe_with_whisperx(arg_video_path, guest_name, use_cached_transcription)
    # word_segments = transcription['word_segments']
    segments = transcription['segments']
    
    
    # Step 2 — Query the chunks
    all_results: PostQueryResults = []
    chunks = chunk_by_time(segments, minutes=10)
    chunks = [chunks[5]]
    for i, chunk in enumerate(chunks):
        log(f"[+] Processing chuck: {i}/{len(chunks)}")
        results = query_fulltext(chunk, MODEL_NAME, LLM_OPTIONS['best_b'], True)
        if len(results):
            # merge new clips into main clips array
            all_results.extend(results)
            
        
    # print(' ') 
    # print(' ')
    # print(all_clips)
    # print(' ')
    # print(' ')


    # Step 3 — Post process output (middlewares)
    post_results = post_clean_obvious_clips(all_results)
    # post_results = post_rank_top(all_results, 10)
    # post_results = post_query_filter_relevant_clip(post_results)

    # Step 4 — Output results
    # cut_and_save_clips(all_clips, arg_video_path, f"{re.sub('\W','', MODEL_NAME)}_{guest_name}")
    output_text(post_results, re.sub('\W','', MODEL_NAME))
  
    


if __name__ == "__main__":
    main()
