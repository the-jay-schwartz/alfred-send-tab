on run argv
	set frontApp to ""
	try
		tell application "System Events"
			set frontApp to name of first application process whose frontmost is true
		end tell
	end try

	set capturedURL to ""

	-- Tier 1: Safari and every Chromium-based browser (Chrome, Edge, Opera,
	-- Brave, Vivaldi, Arc, ...) expose a scriptable "current tab"/"active tab"
	-- URL, so asking whatever's frontmost works without naming any browser.
	-- Safari and the Chromium family use two different terms for "the tab
	-- that's showing," so both are tried before falling through to Tier 2.
	try
		using terms from application "Safari"
			tell application frontApp
				set capturedURL to URL of current tab of front window
			end tell
		end using terms from
	end try

	if capturedURL is "" then
		try
			using terms from application "Google Chrome"
				tell application frontApp
					set capturedURL to URL of active tab of front window
				end tell
			end using terms from
		end try
	end if

	if capturedURL is "" then
		-- Tier 2: universal address-bar copy, for anything without an
		-- AppleScript dictionary (Firefox today, and future non-scriptable browsers).
		set oldClipboard to ""
		try
			set oldClipboard to the clipboard as text
		end try

		try
			tell application "System Events"
				tell process frontApp
					keystroke "l" using command down
					delay 0.15
					keystroke "c" using command down
				end tell
			end tell
		end try
		delay 0.2

		try
			set capturedURL to the clipboard as text
		on error
			set capturedURL to ""
		end try

		try
			set the clipboard to oldClipboard
		end try

		if capturedURL does not start with "http" then
			set capturedURL to ""
		end if
	end if

	if capturedURL is "" then
		return "NONE"
	else
		return capturedURL
	end if
end run
