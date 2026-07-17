file="$1"

if [ ! -f "$file" ]; then
	osascript -e 'display notification "Could not fetch the page source." with title "Send Tab"'
	exit 0
fi

editor="${editor_app:-Visual Studio Code}"

cli=""
case "$(printf '%s' "$editor" | tr '[:upper:]' '[:lower:]')" in
	"visual studio code") cli="code" ;;
	"visual studio code - insiders"|"visual studio code insiders") cli="code-insiders" ;;
	"vscodium"|"codium") cli="codium" ;;
	"cursor") cli="cursor" ;;
	"windsurf") cli="windsurf" ;;
esac

if [ -n "$cli" ] && command -v "$cli" >/dev/null 2>&1; then
	"$cli" "$file" >/dev/null 2>&1 &
	exit 0
fi

if open -a "$editor" "$file" 2>/dev/null; then
	exit 0
fi

NOTIF_EDITOR="$editor" osascript <<'APPLESCRIPT'
on run
	display notification ("Couldn't open with \"" & (system attribute "NOTIF_EDITOR") & "\" — check the app name in the workflow's configuration.") with title "Send Tab"
end run
APPLESCRIPT
