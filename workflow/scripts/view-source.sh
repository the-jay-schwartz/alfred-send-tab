url="$1"
tmpdir="$(mktemp -d)"
outfile="$tmpdir/page-source.html"

http_code=$(curl -sL --max-time 15 -w '%{http_code}' -o "$outfile" "$url")
curl_exit=$?

if [ $curl_exit -eq 0 ] && [ -s "$outfile" ]; then
	printf '%s' "$outfile"
else
	NOTIF_DETAIL="curl exit $curl_exit, HTTP $http_code, URL: $url" osascript <<'APPLESCRIPT'
on run
	display notification (system attribute "NOTIF_DETAIL") with title "Send Tab: couldn't fetch page source"
end run
APPLESCRIPT
	printf '%s' "CURL_FAILED"
fi
