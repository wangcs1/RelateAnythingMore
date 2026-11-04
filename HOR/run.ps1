param([switch]$SkipInference)
$ErrorActionPreference = 'Stop'
$HorRoot = Split-Path $PSScriptRoot -Parent
$HorPython = Join-Path $HorRoot '.venv-eval/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $HorPython)) { throw 'Missing isolated Python environment .venv-eval' }
$env:PYTHONUTF8 = '1'
Set-Location $HorRoot
New-Item -ItemType Directory -Force (Join-Path $PSScriptRoot 'output') | Out-Null
if (-not $SkipInference) {
    & $HorPython -u (Join-Path $PSScriptRoot 'run_500.py') 2>&1 | Tee-Object -FilePath (Join-Path $PSScriptRoot 'output/run.log')
    if ($LASTEXITCODE -ne 0) { throw 'HOR 500-image inference failed' }
}
& $HorPython (Join-Path $PSScriptRoot 'report.py')
if ($LASTEXITCODE -ne 0) { throw 'HOR report generation failed' }
& $HorPython (Join-Path $PSScriptRoot 'verify.py')
if ($LASTEXITCODE -ne 0) { throw 'HOR verification failed' }
& $HorPython (Join-Path $PSScriptRoot 'export_reports.py')
if ($LASTEXITCODE -ne 0) { throw 'HOR report export or delivery verification failed' }
