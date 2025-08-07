import os, json, subprocess
from datetime import datetime
from pathlib import Path
from time import time
import whisperx, ollama

from clips.helpers import load_cache, save_cache, timer


# -------- Configs -------- #
CHUNK_CHAR_LEN = 1500  # max chunk len for LLM prompt
OVERLAP = 150          # char overlap between chunks
MAX_CLIPS_PER_CHUNK = 2
MODEL_NAME = "llama3"
TRANSCRIPT_CACHE_DIR = "./cache"


# -------- Helpers -------- #

def transcribe_with_whisperx(video_path: str, use_cached=True) -> dict:
    os.makedirs(TRANSCRIPT_CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(TRANSCRIPT_CACHE_DIR, Path(video_path).stem + ".json")
    if use_cached:
        return load_cache(cache_path)

    timer.start()
    print("[+] Transcribing with WhisperX...")
    model = whisperx.load_model("large-v3", device="cpu", compute_type="int8")
    audio = whisperx.load_audio(video_path)
    result = model.transcribe(audio, batch_size=16)

    print("[+] Performing word-level alignment...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device="cpu")
    result = whisperx.align(result["segments"], model_a, metadata, audio, device="cpu")

    save_cache(cache_path, result)
    print(f"🎉 Transcription done: {(timer.end()):.2f} s")
    return result


def chunk_transcript_text(transcript: dict):
    text = " ".join([seg["text"] for seg in transcript["segments"]])
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + CHUNK_CHAR_LEN)
        chunks.append(text[start:end])
        start += CHUNK_CHAR_LEN - OVERLAP
    print(chunks[0])
    exit()
    return chunks


def prompt_llama3_for_clips(chunk: str) -> list:
    prompt = f"""
You are an AI podcast editor. Your task is to identify up to 2 short social media clips from the following podcast transcript chunk. 
Reply in JSON format as a list of clips. Each clip should include a short quote (up to 20 words) and a reason.
[
  {{
    "quote": "...",
    "reason": "..."
  }}
]

Transcript chunk:
\"\"\"
{chunk}
\"\"\"
"""
    print("[+] Querying Llama3 via Ollama...")
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    
    try:
        json_start = response['message']['content'].find("[")
        json_data = json.loads(response['message']['content'][json_start:])
        return json_data
    except Exception as e:
        print("[-] Failed to parse LLM output:", e)
        return []


def find_timecode_for_quote(quote: str, transcript: dict):
    quote = quote.lower().strip().replace("…", "...")[:50]
    for seg in transcript["segments"]:
        if quote in seg["text"].lower():
            return seg["start"], seg["end"], seg["text"]
    return None, None, None


def slugify(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text[:30].lower()).strip("-")


def cut_clip(input_path: str, output_path: str, start: float, end: float):
    duration = end - start
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-ss", str(start), "-t", str(duration),
        "-c", "copy", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# -------- Main Logic -------- #

def main(video_path: str):
    assert os.path.exists(video_path), f"File not found: {video_path}"
    transcript = transcribe_with_whisperx(video_path)
    chunks = chunk_transcript_text(transcript)

    all_clips = []
    for idx, chunk in enumerate(chunks):
        print(f"[Chunk {idx+1}/{len(chunks)}]")
        llm_clips = prompt_llama3_for_clips(chunk)
        for clip in llm_clips[:MAX_CLIPS_PER_CHUNK]:
            start, end, full_text = find_timecode_for_quote(clip["quote"], transcript)
            if start is not None:
                all_clips.append({
                    "quote": clip["quote"],
                    "reason": clip["reason"],
                    "start": start,
                    "end": end,
                    "text": full_text
                })

    if not all_clips:
        print("[-] No valid clips found.")
        return

    output_dir = f"./clips-{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(output_dir, exist_ok=True)

    for i, clip in enumerate(all_clips):
        clip_name = slugify(clip["text"]) or f"clip-{i}"
        output_path = os.path.join(output_dir, f"{clip_name}.mp4")
        cut_clip(video_path, output_path, clip["start"], clip["end"])
        print(f"[+] Saved: {output_path}")

    with open(os.path.join(output_dir, "metadata.json"), 'w') as f:
        json.dump(all_clips, f, indent=2)

    print(f"[✓] Done! Clips saved to: {output_dir}")


if __name__ == "__main__":
    main('/Users/VJONA/code/cli-utils/pod-automation/clips/test.mp4')
    # if len(sys.argv) != 2:
    #     print("Usage: pod-clips path/to/video.mp4")
    #     sys.exit(1)

    # video_file = sys.argv[1]
    # main(video_file)
