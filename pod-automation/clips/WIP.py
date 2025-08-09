# LEARN
# - https://dev.to/saranshabd/python-w-strict-typechecker-3l7g
# - https://www.linkedin.com/pulse/demystifying-llm-quantization-suffixes-what-q4km-q80-q6k-paul-ilves-i0yvf



import os, json, subprocess, re
from pathlib import Path
import whisperx, ollama

from typing import List

from utils import load_cache, save_cache, timer, log, now
from utils import Transcript, Clip, ClipTimestamp
from utils import DIR_PROJECT, DIR_CACHE, DIR_OUTPUT



# -------- Configs -------- #

# MODEL_NAME = "llama3" # no-long-context, mehmeh-quality
# MODEL_NAME = "qwen2.5:7b-instruct-q4_K_M" # meh-quality-clips
MODEL_NAME = "yi:9b-chat-v1.5-q6_K" # +long context, meh_ok-quality, 
MODEL_NAME = "spooknik/hermes-2-pro-mistral-7b:q8" # ..

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

# -------- Main functions -------- #
def transcribe_with_whisperx() -> Transcript:
    path_transcript= f"{DIR_CACHE}/{guest_name}.json"

    if use_cached_transcription and os.path.exists(path_transcript):
        log(f"[+] Using cached 'transcript'")
        return load_cache(path_transcript)

    timer.start('T')
    log(f"[+] Starting transcribing video: '{arg_video_path}'...")
    model = whisperx.load_model("small.en", device="cpu", compute_type="int8")
    audio = whisperx.load_audio(arg_video_path)
    transcription = model.transcribe(audio, batch_size=16, language="en")

    log(f"[+] Performing transcription word-level alignment (transcribe took {timer.get('T')})...")
    model_a, metadata = whisperx.load_align_model(language_code='en', device="cpu")
    transcription = whisperx.align(transcription["segments"], model_a, metadata, audio, device="cpu")
    
    save_cache(path_transcript, transcription)
    total_duration = transcription['segments'][-1]['end'] - transcription["segments"][0]["start"]
    log(f"[+] Transcript finished in {timer.end('T')}. Total video duration: {total_duration}")
    return transcription


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
                model=f"{MODEL_NAME}", 
                messages=[
                    # {'role': 'system','content': "You are a professional podcast clip editor. Your job is to extract 0-4 emotionally or intellectually powerful highlights from a transcript. Return only a JSON array of [start, end] timestamp pairs. No markdown, no explanation, no text outside the array."},
                    # {'role': 'system','content': "You are a professional podcast clip editor. Your job is to extract 0-4 emotionally or intellectually powerful highlights from a transcript. Think carefully and consider what sections are meaningful, emotional, or stand out. But return ONLY the final output: a JSON array of [start_time, end_time] pairs."},
                     {
                        'role': 'system',
                        'content': (
                            "You are a professional podcast clip editor. Your job is to extract 0-4 emotionally or intellectually powerful highlights from a transcript. "
                            "Each highlight should be 10-25 seconds long and make sense on its own. "
                            "Return only a JSON array of [start_time, end_time] pairs. No markdown, no explanations."
                        )
                    },
                    {"role": "user", "content": prompt}
                ], 
                options={"format": "json", 
                         # creativity
                        "temperature": 0.5, 
                        # Allows the model to sample from a wider probability mass — helps with varied but still relevant results.
                        "top_p": 0.9, 
                        # 	Reasonable — you could also try omitting it (defaults tend to work well), or go up to 40 to let it explore slightly more options.
                        # "top_k": 20
                        "top_k": 40,
                        # "repeat_penalty": 1.3,
                        # "repeat_last_n": 64,
                        # "num_predict": 256,
                }
        )
        response = chat_response.message.content
        log(f"[+] Query of {len(prompt)} characters, took: {timer.end('Q')}")
    
    try:
        start = response.find("[")
        end = response.rfind("]") + 1
        # make sure to have [[int, int]]
        parsed = [[int(sec[0]), int(sec[1])] for sec in json.loads(response[start:end])]
        # if not used_cached_llm_output:
        #     log(f"[+] Successfully parsed '{parsed}' out of: {response}")
        return parsed
    except Exception as e:
        short_response = (response.replace('\n', '').replace('  ', ''))[:100]
        log(f"[ERR] Failed to parse LLM output:  '{short_response}...' with error: {e}")
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
        log(f"[+] Processing Chunk: {idx+1}/{len(chunks)}...")
        llm_clips = prompt_llama3_for_clips(chunk)
        for clip in llm_clips:
            clips = get_clips_by_timestamps(segments, clip)
            if len(clips) > 0:
                all_clips.append(clips)

    if not all_clips:
        log("[ERR] No valid clips found.")
        return

    log(f"[+] Cutting {len(all_clips)} clips...")
    clip_prefix= f"{guest_name}_{re.sub('[^0-9]','', now()) }"
    cip_suffix = f"{MODEL_NAME}"
    for i, clips in enumerate(all_clips):
        try:
            path_clip= f"{DIR_OUTPUT}/{clip_prefix}_clip-{str(i)}_{cip_suffix}.mp4"
            start_time = clips[0]['start']
            end_time = clips[-1]['end']
            cut_clip(arg_video_path, path_clip, start_time, end_time)
        except Exception as e:
            log(f"[ERR] Failed to cut clip [{str(i)}/{str(len(all_clips))}]: {json.dumps(e)}")            


    with open(os.path.join(DIR_OUTPUT, "metadata.json"), 'w') as f:
        metadata_json = {
            'texts': [ " ".join([i['text'] for i in section]) for section in all_clips],
            'clips': all_clips,
        }
        json.dump(metadata_json, f, indent=2)

    log(f"[v] Done! Saved clips to: {DIR_OUTPUT}. Total time: {timer.end('A')}")




# -------- Helpers -------- #

def chunk_by_time(segments:Clip, minutes:int=10, overlap_seconds:int=60):
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


def get_clips_by_timestamps(segments: Clip, timestamp:ClipTimestamp) -> Clip:
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



from difflib import SequenceMatcher



def fuzzy_map_text_to_timestamps(highlight_texts: list, word_segments: Clip, min_match_ratio: float = 0.7):
    """
    Map LLM-selected raw text excerpts back to start/end timestamps
    using fuzzy string matching against the word-level transcript.
    Returns list of (start, end, matched_text).
    """
    results = []
    transcript_text = " ".join([w['text'] for w in word_segments])
    for htext in highlight_texts:
        # Find best matching substring
        matcher = SequenceMatcher(None, transcript_text.lower(), htext.lower())
        match = matcher.find_longest_match(0, len(transcript_text), 0, len(htext))
        if match.size > 0 and (match.size / len(htext)) >= min_match_ratio:
            # Find which words this span covers
            matched_string = transcript_text[match.a: match.a + match.size]
            start_idx = len(transcript_text[:match.a].split())
            end_idx = start_idx + len(matched_string.split())
            start_time = word_segments[start_idx]['start']
            end_time = word_segments[min(end_idx, len(word_segments)-1)]['end']
            results.append((start_time, end_time, matched_string))
    return results

def postprocess_rank_and_filter(clips, min_length_sec=10, max_length_sec=25, min_words=8):
    """
    Simple scoring/filtering pass over mapped clips.
    You can replace this with an EQ/sentiment model later.
    """
    scored = []
    for start, end, text in clips:
        duration = end - start
        if duration < min_length_sec or duration > max_length_sec:
            continue
        if len(text.split()) < min_words:
            continue
        score = 0
        # Example: boost if emotional keywords present
        for kw in ["amazing", "crazy", "important", "love", "hate", "best", "worst"]:
            if kw in text.lower():
                score += 1
        scored.append((score, start, end, text))
    # Sort high score first, then shortest duration
    scored.sort(key=lambda x: (-x[0], x[2]-x[1]))
    return [(s, e, t) for _, s, e, t in scored]


    

def main():
    assert os.path.exists(arg_video_path), f"File not found: {arg_video_path}"
    log('', 2)
    log(f"Start: {now()}")
    log(f"[+] Start processing for '{Path(arg_video_path).name}'")
    timer.start('A')

    transcript = transcribe_with_whisperx()
    word_segments = transcript['word_segments'] if 'word_segments' in transcript else transcript['segments']

    # Join into raw text
    raw_text = " ".join([w['text'] for w in word_segments])

    # Prompt with raw text
    log(f"[+] Querying '{MODEL_NAME}' with raw transcript...")
    prompt = get_prompt_rawtext(raw_text)
    timer.start('Q')
    chat_response = ollama.chat(
        model=f"{MODEL_NAME}",
        messages=[{'role': 'system', 'content': "You are a podcast clip extractor."},
                  {"role": "user", "content": prompt}],
        options={"temperature": 0.5, "top_p": 0.9, "top_k": 40}
    )
    llm_output = chat_response.message.content.strip()
    log(f"[+] Query took: {timer.end('Q')}")

    # Extract highlights as list of strings
    try:
        highlights = json.loads(llm_output)
        if not isinstance(highlights, list):
            raise ValueError("Not a list")
    except Exception:
        highlights = [line.strip("-• ") for line in llm_output.split("\n") if line.strip()]

    log(f"[+] LLM returned {len(highlights)} highlight candidates")

    # Map to timestamps
    mapped = fuzzy_map_text_to_timestamps(highlights, word_segments)
    log(f"[+] Mapped {len(mapped)} highlights to timestamps")

    # Optional postprocess
    ranked = postprocess_rank_and_filter(mapped)
    log(f"[+] Post-process kept {len(ranked)} highlights")

    # Save output to text file
    out_path = Path(DIR_OUTPUT) / f"output_{MODEL_NAME.replace(':','_')}_{guest_name}.txt"
    with open(out_path, "w") as f:
        for start, end, text in ranked:
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
    log(f"[v] Done! Saved output to {out_path}")






####








def main():
    log(f"[+] Start processing for '{guest_name}'")
    transcription = transcribe_video(video_path, guest_name, use_cached_transcription)
    chucks = chuck_transcription(transcription, 10)
    all_clips = []
    for chuck in chucks:
        # doesn't pass timecodes and is more efficent, then reconstruct the time codes form the clips 
        clips = query_fulltext(chuck)
        # filters out too short or too long videos
        clips = post_clean_obvious_clips(clips)
        all_clips.append(clips)
    
    post_clip = all_clips
    
    # queies for top N clips and cuts of the rest
    # post_clip = post_rank_top(post_clip, 10)
    # prompts to filter if the content is relevant and also trims possible begin or ends parts that might not be good
    post_clip = post_query_filter_relevant_clip(post_clip)
    # again apply to make sure we don't have any crap
    post_clip = post_clean_obvious_clips(post_clip)
    
    create_clips(post_clip, output_path)
    log(f"[v] Done! Saved output to {output_path}")






####



def query_fulltext(segments: Clip, model_name=MODEL_NAME, max_words_per_chunk=1500) -> Clip:
    """
    Query the LLM with raw text from segments, chunking if needed, and map highlights
    back to Clip using simple start/end fuzzy matching.

    Returns: Clip list with {start, end, text, words}
    """
    # Flatten to word-level list
    word_segments = []
    for seg in segments:
        for w in seg["words"]:
            word_segments.append({
                "word": w["word"],
                "start": w["start"],
                "end": w["end"],
                "score": w.get("score", 0.0)
            })

    # Helper to chunk words into max_words_per_chunk
    def chunk_words(words, chunk_size):
        for i in range(0, len(words), chunk_size):
            yield words[i:i+chunk_size]

    results_segments: Clip = []

    for chunk_idx, word_chunk in enumerate(chunk_words(word_segments, max_words_per_chunk)):
        raw_text = " ".join([w["word"] for w in word_chunk])
        log(f"[+] Querying fulltext chunk {chunk_idx+1} ({len(word_chunk)} words)")

        prompt = f"""
You are an expert podcast highlight selector.

You will be given a continuous block of podcast transcript text (no timestamps). 
Identify 0 to 4 emotionally or intellectually impactful highlights that:
- Are between 10 and 25 seconds long
- Make sense when viewed alone (self-contained, with enough setup and payoff)
- Contain meaningful insight, humor, tension, or emotional impact

Return ONLY the highlighted text excerpts, as plain text lines.
If no highlights are found, return an empty list: []

Transcript:
\"\"\"{raw_text}\"\"\"
"""

        # Query LLM
        chat_response = ollama.chat(
            model=model_name,
            messages=[{"role": "system", "content": "You are a podcast clip extractor."},
                      {"role": "user", "content": prompt}],
            options={"temperature": 0.5, "top_p": 0.9, "top_k": 40}
        )
        output = chat_response.message.content.strip()

        # Try to parse LLM output into list of strings
        try:
            highlights = json.loads(output)
            if not isinstance(highlights, list):
                raise ValueError("Not a list")
        except Exception:
            highlights = [line.strip("-• ") for line in output.split("\n") if line.strip()]

        log(f"[+] LLM returned {len(highlights)} highlight candidates in chunk {chunk_idx+1}")

        # Map highlights back to timestamps
        for h in highlights:
            mapped = fuzzy_map_text_to_timestamps_simple(h, word_chunk)
            if mapped:
                start, end, text = mapped
                # Build a Segment entry
                seg_words = [w for w in word_chunk if w["start"] >= start and w["end"] <= end]
                if seg_words:
                    results_segments.append({
                        "start": start,
                        "end": end,
                        "text": " ".join([w["word"] for w in seg_words]),
                        "words": seg_words
                    })

    log(f"[+] query_fulltext: total {len(results_segments)} clips across all chunks")
    return results_segments
