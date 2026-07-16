#!/usr/bin/env python3
"""Generate info.plist from scripts/ and package SendTab.alfredworkflow.

Run after editing scripts/capture-tab.applescript or scripts/view-source.sh.
Object UIDs below are fixed (not regenerated) so re-running this script
produces a stable diff instead of churning every UID on each build.
"""
import pathlib
import plistlib
import re
import zipfile

ROOT = pathlib.Path(__file__).parent


def readme_for_plist():
    """info.plist's readme is shown as plain text (Alfred's own Get Info
    panel), not markdown-rendered, so drop the image embeds that make
    sense in README.md on GitHub but would just show up as raw syntax here.
    """
    path = ROOT / "README.md"
    if not path.exists():
        return ""
    lines = path.read_text().splitlines()
    kept = [ln for ln in lines if not re.match(r"^!\[.*\]\(.*\)\s*$", ln)]
    return "\n".join(kept).strip() + "\n"
CAPTURE_SCRIPT = (ROOT / "scripts" / "capture-tab.applescript").read_text()
CURL_SCRIPT = (ROOT / "scripts" / "view-source.sh").read_text()
OPEN_EDITOR_SCRIPT = (ROOT / "scripts" / "open-in-editor.sh").read_text()
TRIM_SCRIPT = (ROOT / "scripts" / "trim-newline.sh").read_text()

# Fixed UIDs (generated once; kept stable across rebuilds for readable diffs).
KW = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A10"
CAPTURE = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A11"
COND_EMPTY = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A12"
COND_EMPTY_MATCH_UID = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A13"
NOTIF_EMPTY = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A14"
SETVAR = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A15"
LISTFILTER = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A16"
COND_CHOICE = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A17"
COND_BROWSER_MATCH_UID = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A18"
SETVAR_BROWSER = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A19"
ACTION_BROWSER = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A1A"
SETVAR_SOURCE = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A1B"
SCRIPT_CURL = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A1C"
OPEN_EDITOR = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A1D"
TRIM = "3F1E1B10-6C2E-4F1C-9C1C-1B1E7B7C1A1E"


def obj(uid, type_, config, version=1):
    return {"uid": uid, "type": type_, "config": config, "version": version}


objects = [
    obj(KW, "alfred.workflow.input.keyword", {
        "keyword": "{var:keyword}",
        "text": "Send current tab",
        "subtext": "Capture the current browser tab, then open it elsewhere or view its source",
        "withspace": False,
        "argumenttype": 2,
    }),
    obj(CAPTURE, "alfred.workflow.action.script", {
        "type": 6,  # AppleScript
        "scriptargtype": 1,
        "scriptfile": "",
        "script": CAPTURE_SCRIPT,
        "concurrently": False,
        "escaping": 0,
    }),
    obj(TRIM, "alfred.workflow.action.script", {
        "type": 11,  # /bin/bash
        "scriptargtype": 1,
        "scriptfile": "",
        "script": TRIM_SCRIPT,
        "concurrently": False,
        "escaping": 0,
    }),
    obj(COND_EMPTY, "alfred.workflow.utility.conditional", {
        "conditions": [{
            "uid": COND_EMPTY_MATCH_UID,
            "inputstring": "{query}",
            "matchstring": "NONE",
            "matchmode": 0,
            "matchcasesensitive": False,
            "outputlabel": "Nothing captured",
        }],
        "elselabel": "Captured a URL",
        "hideelse": False,
    }),
    obj(NOTIF_EMPTY, "alfred.workflow.output.notification", {
        "title": "Send Tab",
        "text": "Couldn't capture a URL — make sure a browser window is frontmost.",
        "lastpathcomponent": False,
        "removeextension": False,
        "onlyshowifquerypopulated": False,
    }),
    obj(SETVAR, "alfred.workflow.utility.argument", {
        "argument": "",
        "passthroughargument": False,
        "variables": {"capturedurl": "{query}"},
    }),
    obj(LISTFILTER, "alfred.workflow.input.listfilter", {
        "title": "",
        "subtext": "",
        "runningsubtext": "",
        "withspace": True,
        "argumenttype": 1,
        "argumenttrimmode": 0,
        "matchmode": 0,
        "fixedorder": True,
        "items": (
            '[{"title":"Open tab in another browser",'
            '"subtitle":"Choose which browser to open it in",'
            '"arg":"browser"},'
            '{"title":"View page source in an editor",'
            '"subtitle":"Open the page’s HTML source in your editor",'
            '"arg":"source"}]'
        ),
    }),
    obj(COND_CHOICE, "alfred.workflow.utility.conditional", {
        "conditions": [{
            "uid": COND_BROWSER_MATCH_UID,
            "inputstring": "{query}",
            "matchstring": "browser",
            "matchmode": 0,
            "matchcasesensitive": False,
            "outputlabel": "Open in browser",
        }],
        "elselabel": "View source",
        "hideelse": False,
    }),
    obj(SETVAR_BROWSER, "alfred.workflow.utility.argument", {
        "argument": "{var:capturedurl}",
        "passthroughargument": False,
        "variables": {},
    }),
    obj(ACTION_BROWSER, "alfred.workflow.action.actioninalfred", {
        "jumpto": "alfred.action.url.openin",
        "path": "{query}",
        "type": 2,
    }),
    obj(SETVAR_SOURCE, "alfred.workflow.utility.argument", {
        "argument": "{var:capturedurl}",
        "passthroughargument": False,
        "variables": {},
    }),
    obj(SCRIPT_CURL, "alfred.workflow.action.script", {
        "type": 11,  # /bin/bash
        "scriptargtype": 1,
        "scriptfile": "",
        "script": CURL_SCRIPT,
        "concurrently": False,
        "escaping": 0,
    }),
    obj(OPEN_EDITOR, "alfred.workflow.action.script", {
        "type": 11,  # /bin/bash
        "scriptargtype": 1,
        "scriptfile": "",
        "script": OPEN_EDITOR_SCRIPT,
        "concurrently": False,
        "escaping": 0,
    }),
]


def conn(dest, sourceoutputuid=None):
    d = {"destinationuid": dest, "modifiers": 0, "modifiersubtext": "", "vitoclose": False}
    if sourceoutputuid:
        d["sourceoutputuid"] = sourceoutputuid
    return d


connections = {
    KW: [conn(CAPTURE)],
    CAPTURE: [conn(TRIM)],
    TRIM: [conn(COND_EMPTY)],
    COND_EMPTY: [
        conn(NOTIF_EMPTY, sourceoutputuid=COND_EMPTY_MATCH_UID),
        conn(SETVAR),
    ],
    SETVAR: [conn(LISTFILTER)],
    LISTFILTER: [conn(COND_CHOICE)],
    COND_CHOICE: [
        conn(SETVAR_BROWSER, sourceoutputuid=COND_BROWSER_MATCH_UID),
        conn(SETVAR_SOURCE),
    ],
    SETVAR_BROWSER: [conn(ACTION_BROWSER)],
    SETVAR_SOURCE: [conn(SCRIPT_CURL)],
    SCRIPT_CURL: [conn(OPEN_EDITOR)],
}

grid = [
    (KW, 0), (CAPTURE, 1), (TRIM, 2), (COND_EMPTY, 3), (NOTIF_EMPTY, 4),
    (SETVAR, 4), (LISTFILTER, 5), (COND_CHOICE, 6),
    (SETVAR_BROWSER, 7), (ACTION_BROWSER, 8),
    (SETVAR_SOURCE, 7), (SCRIPT_CURL, 8), (OPEN_EDITOR, 9),
]
uidata = {
    u: {"xpos": 200.0 + col * 220.0, "ypos": 150.0 + (i % 3) * 130.0}
    for i, (u, col) in enumerate(grid)
}

root = {
    "bundleid": "com.jayschwartz.sendtab",
    "category": "Productivity",
    "connections": connections,
    "createdby": "Jay Schwartz",
    "description": "Capture the current browser tab and send it to another browser, or view its page source in an editor",
    "disabled": False,
    "name": "Send Tab",
    "objects": objects,
    "readme": readme_for_plist(),
    "uidata": uidata,
    "userconfigurationconfig": [
        {
            "variable": "keyword",
            "label": "Keyword",
            "description": "",
            "type": "textfield",
            "config": {"default": "st", "placeholder": "", "required": False, "trim": True},
        },
        {
            "variable": "editor_app",
            "label": "Preferred editor",
            "description": "App to open page source in (e.g. Visual Studio Code, Sublime Text, Cursor). Must be installed.",
            "type": "textfield",
            "config": {"default": "Visual Studio Code", "placeholder": "", "required": False, "trim": True},
        },
    ],
    "variables": {},
    "variablesdontexport": [],
    "version": "2.1.1",
    "webaddress": "https://github.com/the-jay-schwartz/alfred-send-tab",
}

plist_path = ROOT / "info.plist"
with open(plist_path, "wb") as f:
    plistlib.dump(root, f)
print(f"wrote {plist_path}")

workflow_path = ROOT / "SendTab.alfredworkflow"
icon_path = ROOT / "icon.png"
with zipfile.ZipFile(workflow_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(plist_path, "info.plist")
    if icon_path.exists():
        zf.write(icon_path, "icon.png")
print(f"wrote {workflow_path}")
