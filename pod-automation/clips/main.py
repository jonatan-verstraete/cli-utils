import os, json, subprocess, re
from pathlib import Path
import whisperx, ollama

from typing import TypedDict, List, Tuple

from helpers import load_cache, save_cache, timer, log, now
from helpers import Transcript, Segments, ClipTimestamp
from helpers import DIR_PROJECT, DIR_CACHE, DIR_OUTPUT

# LEARN
# - https://dev.to/saranshabd/python-w-strict-typechecker-3l7g
# - https://www.linkedin.com/pulse/demystifying-llm-quantization-suffixes-what-q4km-q80-q6k-paul-ilves-i0yvf


# -------- Configs -------- #

MODEL_NAME = "llama3"
# MODEL_NAME = "qwen2.5:7b-instruct-q4_K_M"

# ------- variable config ------- #
#  should be in flow or param
arg_current_guest_name="Mark Coleman".lower().replace(' ', '-') or "undefined"
arg_video_path=f'{DIR_PROJECT}/markColeman2.mp4'


use_cached_transcription=True # won't redo transcribe
used_cached_llm_output=False # won't redo prompts (only useful if you are testing clips)

# -------- Main functions -------- #
def transcribe_with_whisperx() -> Transcript:
    path_transcript= f"{DIR_CACHE}/{arg_current_guest_name}.json"

    if use_cached_transcription and os.path.exists(path_transcript):
        log(f"[+] Using cached 'transcript'")
        return load_cache(path_transcript)

    timer.start('T')
    log(f"[+] Starting transcribing video: '{arg_video_path}'...")
    # model = whisperx.load_model("large-v3", device="cpu", compute_type="int8") 
    model = whisperx.load_model("small.en", device="cpu", compute_type="int8") 
    
    
    audio = whisperx.load_audio(arg_video_path)
    result = model.transcribe(audio, batch_size=16, language="en")

    log("[+] Performing transcription word-level alignment...")
    model_a, metadata = whisperx.load_align_model(language_code='en', device="cpu") # result["language"]
    result = whisperx.align(result["segments"], model_a, metadata, audio, device="cpu")

    save_cache(path_transcript, result)
    log(f"[+] Transcript finished in {timer.end('T')}")
    return result


def prompt_llama3_for_clips(transcript_chuck: list) -> List[ClipTimestamp]:
    if used_cached_llm_output:
        log(f"[+] Using cached 'llm_output'")
        response = "[[0.0, 18.912], [289.051, 330.251]]"
        response = "[[41.548, 56.737], [155.051, 165.635], [289.051, 298.582]]"
    else:
        log(f"[+] Querying '{MODEL_NAME}'...")
        timer.start('Q')
        prompt = get_prompt(transcript_chuck)
        chat_response = ollama.chat(
                model=f"{MODEL_NAME}", # -uncensored
                messages=[
                    {'role': 'system','content': "You are a podcast clip extractor. Your job is to select highlights from a transcript of a user defined length. Return only a JSON array of [start, end] timestamps. No markdown. No explanations."},
                    {"role": "user", "content": prompt}
                ], 
                options={"format": "json", "temperature": 0.3, "top_p": 0.8, "top_k": 20}
        )
        
        response = chat_response.message.content
        log(f"[+] Query of '{len(prompt)}' tokens' took: {timer.end('Q')}")
    
    try:
        start = response.find("[")
        end = response.rfind("]") + 1
        parsed = json.loads(response[start:end])
        if not used_cached_llm_output:
            log(f"[+] Successfully parsed '{parsed}' out of: {response}")
        return parsed
    except Exception as e:
        log(f"[ERR] Failed to parse LLM output:  '{response}' with error: {e}")
        return []


# -------- Main -------- #

def main():
    assert os.path.exists(arg_video_path), f"File not found: {arg_video_path}"
    log('', 2)
    log(f"Start: {now()}")
    log(f"[+] Start conversion for '{Path(arg_video_path).name}'")
    timer.start('A')
    # first we transcribe the video and chuck it in parts to limit llm context
    transcript = transcribe_with_whisperx()
    segments = transcript['segments']
    chunks = chunk_by_time(segments)

    all_clips = []
    
 
    # for each chuck we prompt to LLM to select clips
    for idx, chunk in enumerate(chunks):
        log(f"[+] Processing: [Chunk {idx+1}/{len(chunks)}]")
        llm_clips = prompt_llama3_for_clips(chunk)
        for clip in llm_clips:
            clips = get_clips_by_timestamps(segments, clip)
            if len(clips) > 0:
                all_clips.append(clips)

    if not all_clips:
        log("[ERR] No valid clips found.")
        return

    log(f"[+] Cutting {len(all_clips)} clips...")
    clip_prefix= f"clip-{MODEL_NAME}"
    cip_suffix = re.sub('[^0-9]','', now())
    for i, clips in enumerate(all_clips):
        try:
            path_clip= f"{DIR_OUTPUT}/{clip_prefix}-{str(i)}-{cip_suffix}.mp4"
            start_time = clips[0]['start']
            end_time = clips[-1]['end']
            cut_clip(arg_video_path, path_clip, start_time, end_time)
        except Exception as e:
            log(f"[ERR] Failed to cut clip [{str(i)}/{str(len(all_clips))}]: {json.dumps(e)}")            

    with open(os.path.join(DIR_OUTPUT, "metadata.json"), 'w') as f:
        json.dump(all_clips, f, indent=2)

    log(f"[v] Done! Saved clips to: {DIR_OUTPUT}. Total time: {timer.end('A')}")




# -------- Helpers -------- #

def chunk_by_time(segments:Segments, minutes:int=10, overlap_seconds:int=60):
    """
    function is used to chuck the transcribed words into sections (10min by default) with some overlap.
    This is used to feed as chucked contexts to the LLM.
    """
    chunk_duration = minutes * 60    
    chunks = []
    current_chunk = []
    current_start = 0
    for seg in segments:
        if seg['end'] <= current_start + chunk_duration:
            current_chunk.append(seg)
        else:
            chunks.append(current_chunk)
            current_start = current_chunk[-1]['end'] - overlap_seconds
            current_chunk = [seg]
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def get_clips_by_timestamps(segments: Segments, timestamp:ClipTimestamp) -> Segments:
    """
    The llm with respond with an end and start time [[start, end]]. Here we find all the sections in between those times.
    """
    start, end = timestamp
    selected = []
    for segment in segments:
        if segment['end'] < start:
            continue
        if segment['start'] > end:
            break
        # note: adding this would make it strict, but this is not needed in case we got some slightly hallucinated values
        # if segment['start'] == start or segment['end'] == end:
        selected.append(segment)
    return selected

def cut_clip(input_path: str, output_path: str, start: float, end: float):
    duration = end - start
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", input_path,
        "-t", str(duration),
        "-c", "copy",
        output_path
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        # print(f"[+] Clip '{Path(output_path).name}' saved.")
    except Exception as e:
        log(f"Error - Failed to cut video: {e.stderr}")


def get_prompt(transcript_chuck:list) -> str:
    simplifiedTranscript = "\n".join([f"({i['start']}-{i['end']}): {i['text']}" for i in transcript_chuck])
#     prompt = f"""
# You are given a podcast transcript. Find 1-3 highlights, each between 5-20 seconds long.

# Use only the sentence boundaries provided.

# Return a JSON array of [start, end] timestamps from the "start" of the first sentence to the "end" of the last.

# Example:
# [[0.123, 18.912], [50.112, 70.554]]

# Transcript:
# ```json
# {json.dumps(simplifiedTranscript)}
# ```
# """

    prompt = f"""
You are given a podcast transcript with timestamps in the following format:
([start_time]-[end_time]): 'Spoken sentence.'

Your task is to identify 0 to 4 interesting highlights from the transcript. Each highlight should be:
- Approximately 5 to 20 seconds long (based on timestamps).
- Selected based on textual interest or significance

Return your answer as a 2D JSON array, where each sub-array contains the start time of the first sentence and the end time of the last sentence in the highlight.

Expected output format:
[number, number][]

Input transcript:
```json
{simplifiedTranscript}
```

Your task: extract 0-4 interesting highlights from the transcript (5-15s each) and return only a JSON array of [start_time, end_time] pairs.

Example output for 3 highlight:
[[10.123, 25.912], [50.112, 70.554], [80.31, 86.209]]
or 0 highlights:
[]
"""

    return prompt



if __name__ == "__main__":
    main()
    # if len(sys.argv) != 2:
    #     print("Usage: pod-clips path/to/video.mp4")
    #     sys.exit(1)

    # video_file = sys.argv[1]
    # main(video_file)





