#!/bin/bash

## note: this file should imported in ~/.zprofile 
export PATH_CLI_UTILS="$HOME/Documents/GitHub/cli-utils"

############################################################
##################### pod utils ############################
############################################################

source "$PATH_CLI_UTILS/pod-automation/__index.sh"



############################################################
######################## utils #############################
############################################################

download-spotify() {
    URL="${1:-'https://open.spotify.com/playlist/6xycakrzgflOZ8Ru1yvHK6'}"
    spotdl $URL
}


download-yt() {
    $PATH_CLI_UTILS/yt-dlp_macos -x --audio-format mp3 --audio-quality 0 "$@"
}


blink() {
    bash "$PATH_CLI_UTILS/blink" "$@"
}

############################################################
################ copied from basic setup ###################
############################################################


# kodo aka Kodokushi (孤独死) or lonely death refers to a Japanese phenomenon of people dying alone and remaining undiscovered for a long period of time.
:kodo() (
	if [[ $1 ]]; then
		newtab
		clear
	fi
	kill -9 $$
	:close
)

# closes current terminal
:close() (
	v="green-mile"
	echo -n -e "\033]0;$v\007"
	osascript -e 'tell application "Terminal" to close (every window whose name contains "'$v'")' &
)

# easy mkdir -p
:mkdir() {
    mkdir -p $1
    cd $1
}


:clearcache() {
	rm -rf ~/Library/Application\ Support/CrashReporter/*
	rm -rf ~/Library/Application\ Support/stremio-server/stremio-cache
	# rm -rf ~/Library/Caches/*
	rm -rf ~/Library/Logs/*
	yarn cache clean
	
	if [[ $1 ]]; then
		rm -rf ~/Library/Application\ Support/Adobe/Common/Media\ Cache\ Files/*
		rm -rf ~/Library/Application\ Support/Adobe/Common/Analyzer\ Cache\ Files/*
		rm -rf ~/Library/Application\ Support/Adobe/Common/Peak\ Files/*
		# rm -rf ~/Library/Application\ Support/Code/Cache/Cache_Data
	fi
	clear
	echo "Cache cleared!"
}


alias l='ls'
alias ll='ls -l'
alias la='ls -a'
alias l1='ls -1'
alias sl="ls"
alias lsl="ls -lhFA | less"

alias c='clear'

alias t1='tree -L 1'
alias t2='tree -L 2'
alias t3='tree -L 3'
# usage of file size (only 2levels as it might do insane search otherwise)
alias t2m='tree --du -h -L 2 | grep M]'
#alias tsg='tree --du -h | grep G]'

alias psg="ps aux | grep -v grep | grep -i -e VSZ -e"
