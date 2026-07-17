# Development

`workflow/info.plist` and `dist/*.alfredworkflow` are generated, not hand-edited. The checked-in source is `build.py` plus everything under `workflow/` except `info.plist` itself. After changing a script under `workflow/scripts/` or `workflow/readme.md`, run:

```
python3 build.py
```

then import `dist/send-tab-vX.Y.Z.alfredworkflow` into Alfred to test.

## Releasing

1. Bump `VERSION` in `build.py`.
2. Add a matching `## [X.Y.Z] - YYYY-MM-DD` section to `CHANGELOG.md`.
3. Commit, then tag and push: `git tag vX.Y.Z && git push origin vX.Y.Z`.

`.github/workflows/release.yml` builds the workflow, verifies the tag matches `build.py`'s version, and publishes a GitHub Release with the `.alfredworkflow` attached and that CHANGELOG section as the release notes.

## How it works

- **Capturing the tab** ([workflow/scripts/capture-tab.applescript](workflow/scripts/capture-tab.applescript)) tries two AppleScript terms for "the tab that's showing" — Safari calls it the *current tab*, the Chromium family calls it the *active tab* — against whatever app is currently frontmost. If neither works (e.g. Firefox, which has no AppleScript dictionary), it falls back to a universal trick: send Cmd+L then Cmd+C to copy the address bar.
- **The browser picker** hands the captured URL to Alfred's native `Action in Alfred` object (jumps straight to `alfred.action.url.openin`), so there's no browser registry to maintain.
- **Viewing page source** ([workflow/scripts/view-source.sh](workflow/scripts/view-source.sh)) is a plain `curl` fetch of the URL, saved to a temp file.
- **Opening the source file** ([workflow/scripts/open-in-editor.sh](workflow/scripts/open-in-editor.sh)) reads the `editor_app` config variable; if it recognizes a VS Code-family app (VS Code, Insiders, VSCodium, Cursor, Windsurf) with its CLI shim on `$PATH`, it uses that CLI, otherwise falls back to `open -a "$editor_app"`.
