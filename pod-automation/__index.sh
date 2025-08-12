# will be imported by the index of the utils

SCRIPT_DIR="$PATH_CLI_UTILS/pod-automation"

source $SCRIPT_DIR/cfr.sh


pod-thumbnail() {
    python3 "$SCRIPT_DIR/thumbnail/update-thumbnail.py" "$@"
}



# Pure video compression, audio untouched
pod-compress() {
  input_file="$1"
  shift

  if [ -z "$input_file" ]; then
    cat <<EOF
Usage: pod-compress /path/to/input.mov [options]

Options:
  -m MODE      Compression mode: normal (default), fast, superfast
               normal    - libx264, preset medium
               fast      - libx264, preset fast
               superfast - libx264, preset ultrafast

Examples:
  pod-compress input.mov
  pod-compress input.mov -m fast
  pod-compress input.mov -m superfast
EOF
    return 1
  fi

  if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' does not exist."
    return 1
  fi

  # Default settings
  mode="normal"
  audio_args=(-c:a copy) # Keep original audio

  filename=$(basename "$input_file" | sed 's/\.[^.]*$//')
  dirname=$(dirname "$input_file")
  timestamp=$(date '+%d-%m-%Y_%H%M%S')

  # Parse options
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -m)
        mode="$2"
        shift 2
        ;;
      *)
        echo "Unknown option: $1"
        return 1
        ;;
    esac
  done

  # Set video encoding speed
  case "$mode" in
    normal)
      echo "🎯 Mode: NORMAL (preset medium)"
      video_args=(-c:v libx264 -preset medium)
      ;;
    fast)
      echo "⚡ Mode: FAST (preset fast)"
      video_args=(-c:v libx264 -preset fast)
      ;;
    superfast)
      echo "🚀 Mode: SUPERFAST (preset ultrafast)"
      video_args=(-c:v libx264 -preset ultrafast)
      ;;
    *)
      echo "❌ Unknown mode: $mode"
      return 1
      ;;
  esac

  output_file="${dirname}/${filename}_${timestamp}_${mode}_compressed.mp4"

  echo "▶️ Compressing '$input_file'..."
  ffmpeg -hide_banner -loglevel info -y -i "$input_file" \
    "${video_args[@]}" \
    "${audio_args[@]}" \
    -movflags +faststart \
    "$output_file" 
    #2>&1 | tail -n 5 -f

  if [ $? -eq 0 ]; then
    echo "✅ Compression finished! Output file: $output_file"
  else
    echo "❌ Compression failed!"
    return 1
  fi
}
