#!/bin/bash

# Usage: ./split_by_speaker.sh input_video.mp4

set -e

INPUT_VIDEO="$1"
BASENAME=$(basename "$INPUT_VIDEO" | cut -d. -f1)

# 1. Convert video to WAV
echo "Extracting audio..."
ffmpeg -y -i "$INPUT_VIDEO" -ar 16000 -ac 1 -c:a pcm_s16le "${BASENAME}.wav"

# 2. Run WhisperX diarization (Python script)
echo "Running WhisperX transcription and diarization..."
python3 whisperx_pipeline.py "${BASENAME}.wav"

# 3. Split audio by speaker
echo "Splitting audio by speaker..."
python3 split_audio_by_speaker.py "${BASENAME}.wav" diarization_segments.json

echo "Done. Output files: speaker_1.wav, speaker_2.wav"


