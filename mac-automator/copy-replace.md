```apple-script
-- Clipboard swap: replaces selection with clipboard, and puts selection into clipboard
set oldClipboard to the clipboard

tell application "System Events"
    keystroke "c" using {command down} -- copy current selection
end tell

delay 0.05 -- tiny pause to let clipboard update
set newClipboard to the clipboard

set the clipboard to oldClipboard

tell application "System Events"
    keystroke "v" using {command down} -- paste the old clipboard over the selection
end tell

delay 0.05
set the clipboard to newClipboard
```

- Open Automator → create a new Quick Action.
- Set “Workflow receives” to “no input” in “any application.”
- Add a “Run AppleScript” action and paste the script above.
- Save the Quick Action as something like “Clipboard Swap.”
- Open System Settings → Keyboard → Keyboard Shortcuts → Services, find “Clipboard Swap,” and give it a shortcut like ⇧⌘V.