# Sam owns shared setup scripts. Python 3.11+ must be installed.
param([string]$Python = "python")
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
& $Python -c "import sys; assert sys.version_info >= (3,11), 'Python 3.11 or newer is required'"
if ($LASTEXITCODE -ne 0) { throw "Python 3.11+ was not found. Supply -Python with the full executable path." }
& $Python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "Could not create the virtual environment." }
& .\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
Write-Host "Ready. Run: powershell -ExecutionPolicy Bypass -File scripts/run.ps1"
