<#
.SYNOPSIS
    One-click installer for tutorial-animation-architect skill.
#>
$ErrorActionPreference = "Stop"
Write-Host ">>> Installing tutorial-animation-architect skill..." -ForegroundColor Cyan

$targetDir = "$env:USERPROFILE\.gemini\config\skills\tutorial-animation-architect"
$scriptsDir = Join-Path $targetDir "scripts"

if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
}

$baseUrl = "https://raw.githubusercontent.com/JeffreyHo0520/tutorial-animation-architect/main"

$files = @(
    "SKILL.md",
    "scripts/audio_pipeline.py",
    "scripts/render_pipeline.py",
    "scripts/qa_inspection.py"
)

foreach ($f in $files) {
    $src = "$baseUrl/$f"
    $dst = Join-Path $targetDir ($f -replace "/", "\")
    $parent = Split-Path $dst -Parent
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Write-Host "Downloading $f..." -ForegroundColor Gray
    Invoke-WebRequest -Uri $src -OutFile $dst -UseBasicParsing
}

Write-Host ">>> Skill installed successfully to: $targetDir" -ForegroundColor Green

# Environment verification
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    Write-Host ">>> Python is available at: $($pythonCmd.Source)" -ForegroundColor Green
} else {
    Write-Host ">>> Note: Python was not detected in PATH." -ForegroundColor Yellow
}

$ffmpegCmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpegCmd) {
    Write-Host ">>> FFmpeg is available at: $($ffmpegCmd.Source)" -ForegroundColor Green
} else {
    Write-Host ">>> Note: FFmpeg was not detected in PATH. Install via: winget install Gyan.FFmpeg" -ForegroundColor Yellow
}
