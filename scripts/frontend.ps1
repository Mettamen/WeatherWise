param([int]$Port = 5173)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
Write-Host "Frontend-only preview: http://127.0.0.1:$Port/?mock=1"
& .\.venv\Scripts\python.exe -m http.server $Port --bind 127.0.0.1 --directory frontend_shreshta
