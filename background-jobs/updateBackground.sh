#!/bin/bash

# This script will be executed every 10 min
# launcher: ~/Library/LaunchAgents/com.custom.background.plist
# launchctl load ~/Library/LaunchAgents/com.custom.background.plist
# launchctl unload ~/Library/LaunchAgents/com.custom.background.plist

python3 "$HOME/Documents/GitHub/cli-utils/fn-setRandomBackground.py" "$HOME/Documents/ai-quotes"