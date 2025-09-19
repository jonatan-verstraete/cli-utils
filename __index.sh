#!/bin/bash
# Please import me :)

# path to this repo
export PATH_CLI_UTILS="$HOME/Documents/GitHub/cli-utils"


source "$PATH_CLI_UTILS/_alias.sh"
source "$PATH_CLI_UTILS/_scripts.sh"
source "$PATH_CLI_UTILS/_utils.sh"

source "$PATH_CLI_UTILS/pod-automation/__index.sh"


code() {
	# default is mac vs code settings
	local file="${1:-$HOME/Library/Application Support/Code/User/settings.json}"
    open -a "Visual Studio Code" --args "$file"
}


