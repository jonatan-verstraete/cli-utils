# function that trigger custom scripts or serve as wrapper

cli_pth_scripts="$PATH_CLI_UTILS/scripts"
cli_pth_configs="$PATH_CLI_UTILS/saved-configs"
cli_pth_vendors="$PATH_CLI_UTILS/vendor"


:download-yt() {
    $cli_pth_vendors/yt-dlp_macos -x --audio-format mp3 --audio-quality 0 "$1"
}

:blink() {
    bash "$cli_pth_scripts/fn-blink.sh" "$@"
}


:random-bg() {
	local URL="${1:-'$HOME/Documents/ai-quotes'}"
	python3 "$cli_pth_scripts/fn-setRandomBackground.py" $URL
}

:compress(){
	python3 "$cli_pth_scripts/app-compress-screenrecordings.py" "$1"
}

:grep-component() {
    python3 "$cli_pth_scripts/grep-react-component.py" "$@"
}