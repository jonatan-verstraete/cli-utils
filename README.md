# cli-utils
Add `source "$HOME/Documents/GitHub/cli-utils/__index.sh"` (or pwd) to your `~/.zhsrc` with:
```sh
echo "\nsource '$(pwd)/__index.sh'" >> ~/.zshrc
```

# OSX keepers
- disable emojis FT flag:
`sudo defaults write /Library/Preferences/FeatureFlags/Domain/UIKit.plist emoji_enhancements -dict-add Enabled -bool NO`
- disable swipe goes back history:
`defaults write com.google.Chrome AppleEnableSwipeNavigateWithScrolls -bool FALSE`
- can help with flickering vscode on external monitor: `code --disable-gpu`
- disable spotlight indexing: `sudo mdutil -a -i off`


**Tools**:
-  `brew install fzf`. fuzzy finder. It replaces half your brain. Rapid file navigation, command search, git integration
- `brew install bat`. A cat replacement with syntax highlighting. Useful for quick code browsing.
- `brew install eza`. Pprettier ls, because clarity is computational speed for the mind.