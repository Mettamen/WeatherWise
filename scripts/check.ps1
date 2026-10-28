$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
& .\.venv\Scripts\python.exe -m pytest
if ($LASTEXITCODE -ne 0) { throw "Tests failed." }
& .\.venv\Scripts\python.exe scripts/export_contracts.py --check
if ($LASTEXITCODE -ne 0) { throw "Shared contracts or mock fixtures have drifted." }
