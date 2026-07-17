# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.1] - 2026-07-16

### Fixed

- Captured tab URLs had a trailing newline that `curl` silently rejected,
  breaking "View page source" on every attempt. Added a trim step
  immediately after capture.
- `view-source.sh` now reports curl's exit code, HTTP status, and the URL
  in a notification on failure, instead of a bare sentinel.
- `open-in-editor.sh` now checks the file actually exists before trying to
  open it, instead of opening a fake "CURL_FAILED" document in the editor.

## [2.1.0] - 2026-07-16

### Added

- Configurable keyword (default `st`, was `sendtab`) and preferred editor
  (default Visual Studio Code), via the Workflow's Configuration.
- VS Code-family CLI detection (code / code-insiders / codium / cursor /
  windsurf) for opening page source, falling back to `open -a`.
- Workflow icon.

### Fixed

- "View page source" no longer routes through Alfred's Action in Alfred
  "Open With" panel — a plain Run Script string isn't typed as a File for
  that panel, which produced a "No Items To Action" error. It now opens
  directly in the configured editor instead.

### Changed

- Rewrote README to match the Alfred gallery style guide.

## [2.0.0] - 2026-07-16

### Added

- Initial standalone rewrite: a single keyword captures the current
  browser tab (Safari's "current tab" and the Chromium family's "active
  tab" AppleScript terms, falling back to a universal Cmd+L/Cmd+C
  address-bar copy for anything else, e.g. Firefox), then either hands the
  URL to Alfred's native "Open URL in…" panel or fetches the page's HTML
  via curl to view its source.
- No hardcoded browser list — the destination picker is Alfred's own
  native panel, populated from whatever's actually installed.
- MIT license.

### Changed

- Replaced the 5 per-browser AppleScript files (one per Safari/Chrome/
  Edge/Opera/Firefox round-trip) inherited from the original fork with one
  generic capture script.
