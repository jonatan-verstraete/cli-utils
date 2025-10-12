# will be imported by the index of the utils

SCRIPT_DIR="$PATH_CLI_UTILS/pod-automation"

source $SCRIPT_DIR/fn-pod-cfr.sh
source $SCRIPT_DIR/fn-pod-compress.sh


:pod-thumbnail() {
    python3 "$SCRIPT_DIR/thumbnail/update-thumbnail.py" "$@"
}



:pod-sync() {
  input="$1"
  if [ -z "$input" ] || [ ! -f "$input" ]; then
    echo "Usage: fix-av-sync /path/to/input.mov"
    return 1
  fi

  dir=$(dirname "$input")
  base=$(basename "$input")
  name="${base%.*}"
  ext="${base##*.}"
  date_tag=$(date '+%Y%m%d_%H%M%S')
  output="${dir}/${name}_${date_tag}.mp4"

  ffmpeg -hide_banner -loglevel info -y -fflags +genpts -i "$input" \
    -vf "fps=25" -vsync cfr \
    -c:v libx264 -preset fast -crf 23 \
    -c:a aac -b:a 192k -af "aresample=async=1" \
    -movflags +faststart \
    "$output"

  if [ $? -eq 0 ]; then
    echo "✅ Fixed file saved to: $output"
  else
    echo "❌ Conversion failed."
    return 1
  fi
}
``



