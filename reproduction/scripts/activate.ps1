$ReproWorkspace = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$env:PYTHONUTF8 = '1'
$env:HF_HOME = Join-Path $ReproWorkspace '.hf_cache_eval'
$env:HTTP_PROXY = 'http://127.0.0.1:7897'
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'
$env:HF_HUB_DISABLE_XET = '1'
& (Join-Path $ReproWorkspace '.venv-eval/Scripts/Activate.ps1')
Set-Location $ReproWorkspace
