param(
    [ValidateSet('prepare.py','attention_vocab.py','trace_sample.py','benchmark_interventions.py','review_audit.py','render_report.py','make_glossary_copy.py','verify_artifacts.py')]
    [string[]]$Stages = @('prepare.py','attention_vocab.py','trace_sample.py','benchmark_interventions.py','review_audit.py','render_report.py','make_glossary_copy.py','verify_artifacts.py')
)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/activate.ps1"
foreach ($ReproScript in $Stages) {
    $ReproLogs = Join-Path (Split-Path $PSScriptRoot -Parent) 'output/logs'
    New-Item -ItemType Directory -Force -Path $ReproLogs | Out-Null
    if ($ReproScript -eq 'render_report.py') {
        python (Join-Path $PSScriptRoot 'run_stage.py') 'package_evidence.py' '--inventory-only'
        if ($LASTEXITCODE -ne 0) { throw 'Evidence inventory failed' }
    }
    python (Join-Path $PSScriptRoot 'run_stage.py') $ReproScript 2>&1 | Tee-Object -FilePath (Join-Path $ReproLogs "$ReproScript.log")
    if ($LASTEXITCODE -ne 0) { throw "Failed: $ReproScript" }
}
if ($Stages -contains 'verify_artifacts.py') {
    python (Join-Path $PSScriptRoot 'package_evidence.py')
    if ($LASTEXITCODE -ne 0) { throw 'Evidence packaging or portable verification failed' }
}
