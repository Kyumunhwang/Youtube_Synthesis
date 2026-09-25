# run_app.ps1 - Automated Streamlit Launcher with Port Collision Avoidance
$TargetPort = 3055

# Ensure chosen port is completely free
while (Get-NetTCPConnection -LocalPort $TargetPort -ErrorAction SilentlyContinue) {
    Write-Host "Port $TargetPort is currently in use. Incrementing to $($TargetPort + 1)..." -ForegroundColor Yellow
    $TargetPort++
}

Write-Host "Starting YouTube Intelligence Extractor UI on http://localhost:$TargetPort..." -ForegroundColor Green

$StreamlitBin = "$env:USERPROFILE\.agent-reach-venv\Scripts\streamlit.exe"
& $StreamlitBin run app.py --server.port $TargetPort --server.headless false
