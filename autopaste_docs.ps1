# autopaste_docs.ps1 - Robust OS Robot for Google Docs Auto-Paste
param(
    [string]$FilePath
)

if (-not (Test-Path -LiteralPath $FilePath)) {
    exit 1
}

# 1. Read UTF-8 text and inject into Windows Clipboard
Get-Content -LiteralPath $FilePath -Raw -Encoding UTF8 | Set-Clipboard

# 2. Open Google Docs in default web browser
Start-Process "https://docs.new"

# 3. Wait for browser window and Google Docs Canvas Kix editor initialization
# Google Docs typically requires 3.5 to 5.0 seconds to initialize the canvas editing layer
Start-Sleep -Milliseconds 4500

$wshell = New-Object -ComObject WScript.Shell

# 4. Bring the browser window to the foreground
$activated = $wshell.AppActivate("Google Docs")
if (-not $activated) { $activated = $wshell.AppActivate("Google Chrome") }
if (-not $activated) { $activated = $wshell.AppActivate("Microsoft Edge") }
if (-not $activated) { $activated = $wshell.AppActivate("Chrome") }
if (-not $activated) { $activated = $wshell.AppActivate("Edge") }

Start-Sleep -Milliseconds 500

# 5. Dispatch Paste (Ctrl+V) keystroke
$wshell.SendKeys('^v')
Write-Host "Auto-paste successfully dispatched to Google Docs editor."
