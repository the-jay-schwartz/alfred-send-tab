# Development

`info.plist` and `SendTab.alfredworkflow` are generated, not hand-edited. After changing a script under `scripts/`, run:

```
python3 build.py
```

then re-import `SendTab.alfredworkflow` into Alfred to test.

## How it works

- **Capturing the tab** ([scripts/capture-tab.applescript](scripts/capture-tab.applescript)) tries two AppleScript terms for "the tab that's showing" — Safari calls it the *current tab*, the Chromium family calls it the *active tab* — against whatever app is currently frontmost. If neither works (e.g. Firefox, which has no AppleScript dictionary), it falls back to a universal trick: send Cmd+L then Cmd+C to copy the address bar.
- **The browser picker** hands the captured URL to Alfred's native `Action in Alfred` object (jumps straight to `alfred.action.url.openin`), so there's no browser registry to maintain.
- **Viewing page source** ([scripts/view-source.sh](scripts/view-source.sh)) is a plain `curl` fetch of the URL, saved to a temp file.
- **Opening the source file** ([scripts/open-in-editor.sh](scripts/open-in-editor.sh)) reads the `editor_app` config variable; if it recognizes a VS Code-family app (VS Code, Insiders, VSCodium, Cursor, Windsurf) with its CLI shim on `$PATH`, it uses that CLI, otherwise falls back to `open -a "$editor_app"`.
