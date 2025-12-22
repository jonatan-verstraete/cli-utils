# cli-utils
Quick personal setup for `OSX` .


Add path:
```sh
echo "\nsource '$(pwd)/__index.sh'" >> ~/.zshrc
# or
echo "\nsource '$HOME/Documents/GitHub/cli-utils/__index.sh'" >> ~/.zshrc
```


Install:
```sh
# fuzzy finder. It replaces half your brain. Rapid file navigation, command search, git integration
brew install fzf

# A cat replacement with syntax highlighting. Useful for quick code browsing.
brew install bat

# A prettier ls, because clarity is computational speed for the mind.
# See "./_alias.sh" if you use this
brew install eza
```

> note. If you did not have  `brew install eza`, comment L2 (alias ls='eza') in [_alias.sh](./_alias.sh).

## Customization
Commands to alter behavior.

```sh
# show hidden files in finder by default
defaults write com.apple.finder AppleShowAllFiles true


# disable emojis
# Go to `System Settings - Keyboard - Press "globe" key to - DO NOTHING`
sudo defaults write /Library/Preferences/FeatureFlags/Domain/UIKit.plist emoji_enhancements -dict-add Enabled -bool NO


# disable 2 finger swipe goes back in browsing history
defaults write com.google.Chrome AppleEnableSwipeNavigateWithScrolls -bool FALSE


# disable spotlight indexing - use Raycast
sudo mdutil -a -i off

# Disable itunes launcher (pressing f8)
launchctl unload -w /System/Library/LaunchAgents/com.apple.rcd.plist
```


**keepers**:
```sh
# can help with flickering vscode on external monitor (not persistent, wip)
code --disable-gpu

# Restart audio core
sudo launchctl kickstart -kp system/com.apple.audio.coreaudiod
```