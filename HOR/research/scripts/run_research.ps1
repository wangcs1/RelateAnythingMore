param(
    [switch]$RerunModels
)

$ErrorActionPreference = 'Stop'
$researchRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$researchPython = Join-Path $researchRoot '.venv-eval\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $researchPython -PathType Leaf)) {
    throw 'The isolated .venv-eval environment does not exist.'
}

function Invoke-ResearchScript {
    param([string]$ScriptName, [string[]]$ScriptArguments = @())
    Write-Host "Running $ScriptName"
    & $researchPython (Join-Path $PSScriptRoot $ScriptName) @ScriptArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Research script failed: $ScriptName (exit $LASTEXITCODE)"
    }
}

Push-Location $researchRoot
try {
    if ($RerunModels) {
        foreach ($researchOutputName in @('regions', 'active_detection')) {
            $researchOutput = Join-Path $researchRoot ('HOR\research\output\' + $researchOutputName)
            if (-not (Test-Path -LiteralPath $researchOutput)) {
                continue
            }
            $archiveParent = Join-Path $researchRoot 'HOR\research\.work\model_reruns'
            $archiveName = $researchOutputName + '_' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfff')
            $archiveTarget = [System.IO.Path]::GetFullPath((Join-Path $archiveParent $archiveName))
            $resolvedOutput = (Resolve-Path -LiteralPath $researchOutput).Path
            $requiredPrefix = $researchRoot + [System.IO.Path]::DirectorySeparatorChar
            if (-not $resolvedOutput.StartsWith($requiredPrefix, [StringComparison]::OrdinalIgnoreCase) -or
                -not $archiveTarget.StartsWith($requiredPrefix, [StringComparison]::OrdinalIgnoreCase)) {
                throw 'The generated-output archive must remain inside this workspace.'
            }
            if (Test-Path -LiteralPath $archiveTarget) {
                throw "The archive target already exists: $archiveTarget"
            }
            New-Item -ItemType Directory -Path $archiveParent -Force | Out-Null
            Write-Host "Archiving generated $researchOutputName outputs to $archiveTarget"
            Move-Item -LiteralPath $resolvedOutput -Destination $archiveTarget
        }
        Invoke-ResearchScript -ScriptName 'region_study.py' -ScriptArguments @('--visualization-count', '12')
        Invoke-ResearchScript -ScriptName 'profile_region_study.py'
        Invoke-ResearchScript -ScriptName 'predict_coco_keypoints.py'
    }
    Invoke-ResearchScript -ScriptName 'audit_mask2former.py'
    Invoke-ResearchScript -ScriptName 'decode_study.py'
    Invoke-ResearchScript -ScriptName 'analyze_region_study.py'
    Invoke-ResearchScript -ScriptName 'part_evidence_study.py'
    Invoke-ResearchScript -ScriptName 'controlled_3d_damage_study.py'
    if ($RerunModels) {
        Invoke-ResearchScript -ScriptName 'active_detection_study.py' -ScriptArguments @('--prepare')
        Invoke-ResearchScript -ScriptName 'active_detection_study.py' -ScriptArguments @('--infer')
    }
    else {
        Invoke-ResearchScript -ScriptName 'active_detection_study.py'
    }
    Invoke-ResearchScript -ScriptName 'verify_research.py'
}
finally {
    Pop-Location
}
