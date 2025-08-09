import os, json, subprocess
from utils import Clips, log
from utils import DIR_OUTPUT

def cut_clips(all_clips: Clips, guest_name:str, model_name:str, video_phth: str):
    clip_prefix= f"{guest_name}_{re.sub('[^0-9]','', now()) }"
    cip_suffix = f"{model_name}"
    
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