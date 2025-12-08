# cli-utils
Add `source "$HOME/Documents/GitHub/cli-utils/__index.sh"` (or pwd) to your `~/.zhsrc` with:
```sh
echo "\nsource '$(pwd)/__index.sh'" >> ~/.zshrc
```

# Stuff/keepers
- disable emojis FT flag `sudo defaults write /Library/Preferences/FeatureFlags/Domain/UIKit.plist emoji_enhancements -dict-add Enabled -bool NO`
- can help with flickering vscode on external monitor `code --disable-gpu`