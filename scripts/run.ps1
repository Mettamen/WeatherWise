param([int]$Port = 8000)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Test-Path .\.venv\Scripts\python.exe)) { throw "Run scripts/setup.ps1 first." }
& .\.venv\Scripts\python.exe -m uvicorn backend.be1_sam.app:app --host 127.0.0.1 --port $Port --reload
