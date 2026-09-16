<#
Patch-Y guided contributor launcher.
Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell
#>
[CmdletBinding()]
param(
    [ValidateSet('Menu', 'Check', 'Fetch', 'Inspect', 'Build', 'Verify', 'PreparePR', 'Help')]
    [string]$Action = 'Menu',
    [string]$Server,
    [string]$Label,
    [string]$Edition,
    [string]$StormLib
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $RepoRoot

function Find-Python {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) { return @{ Exe = $py.Source; Prefix = @('-3.11') } }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) { return @{ Exe = $python.Source; Prefix = @() } }
    throw 'Python 3.11 or newer was not found. Install it from python.org, select Add python.exe to PATH, then reopen this launcher.'
}

function Test-PythonVersion([hashtable]$Python) {
    $code = 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 2)'
    & $Python.Exe @($Python.Prefix) -c $code
    if ($LASTEXITCODE -ne 0) { throw 'Patch-Y requires Python 3.11 or newer.' }
    & $Python.Exe @($Python.Prefix) --version
}

function Set-StormLibPath {
    if ($StormLib) { $candidate = $StormLib }
    elseif ($env:STORMLIB_DLL) { $candidate = $env:STORMLIB_DLL }
    else {
        try {
            Add-Type -AssemblyName System.Windows.Forms
            $picker = New-Object System.Windows.Forms.OpenFileDialog
            $picker.Title = 'Select the x64 Unicode StormLib.dll'
            $picker.Filter = 'StormLib.dll|StormLib.dll|DLL files (*.dll)|*.dll'
            $picker.CheckFileExists = $true
            if ($picker.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
                $candidate = $picker.FileName
            }
            else { $candidate = '' }
        }
        catch {
            $candidate = Read-Host 'Enter the full path to a trusted x64 Unicode StormLib.dll'
        }
    }
    if (-not $candidate -or -not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw 'StormLib.dll was not found at that exact path. See docs/PATCH-Y-QUICKSTART-WINDOWS.md.'
    }
    if ([IO.Path]::GetFileName($candidate) -ine 'StormLib.dll') {
        throw 'Select the file named StormLib.dll.'
    }
    $env:STORMLIB_DLL = (Resolve-Path -LiteralPath $candidate).Path
    Write-Host "StormLib: $env:STORMLIB_DLL"
}

$Python = Find-Python
Test-PythonVersion $Python

function Invoke-PatchY([string[]]$Arguments, [switch]$NeedsStormLib) {
    if ($NeedsStormLib) { Set-StormLibPath }
    Write-Host "`nRunning Patch-Y $($Arguments -join ' ')`n"
    & $Python.Exe @($Python.Prefix) (Join-Path $RepoRoot 'tools\patch_y.py') @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Patch-Y command failed with exit code $LASTEXITCODE." }
}

function Require-Value([string]$Value, [string]$Prompt) {
    if ($Value) { return $Value }
    $answer = Read-Host $Prompt
    if (-not $answer) { throw "$Prompt is required." }
    return $answer
}

if ($Action -eq 'Menu') {
    Write-Host @'

Patch-Y contributor helper
1. Check Python and StormLib
2. Fetch the verified 3.0.9 baseline
3. Inspect one edition
4. Build candidates
5. Verify candidates
6. Prepare pull-request proof (verify baseline, build, verify, diff)
7. Show help
'@
    $choice = Read-Host 'Choose 1-7'
    $Action = switch ($choice) {
        '1' { 'Check' }
        '2' { 'Fetch' }
        '3' { 'Inspect' }
        '4' { 'Build' }
        '5' { 'Verify' }
        '6' { 'PreparePR' }
        '7' { 'Help' }
        default { throw 'Choose a number from 1 through 7.' }
    }
}

switch ($Action) {
    'Help' {
        Write-Host 'Beginner guide: docs\PATCH-Y-QUICKSTART-WINDOWS.md'
        Write-Host 'Technical guide: docs\PATCH-Y-DEVELOPMENT.md'
    }
    'Check' {
        Set-StormLibPath
        Write-Host 'PASS: Python and StormLib paths are ready.'
    }
    'Fetch' { Invoke-PatchY @('fetch') }
    'Inspect' {
        $Edition = Require-Value $Edition 'Edition name (copy it from patch-y/baseline.json)'
        Invoke-PatchY @('inspect', $Edition) -NeedsStormLib
    }
    'Build' {
        $Server = Require-Value $Server 'Registered target ID (for example warmane or wowcircle)'
        $Label = Require-Value $Label 'Short lowercase development label'
        Invoke-PatchY @('build', '--server', $Server, '--label', $Label) -NeedsStormLib
    }
    'Verify' {
        $Server = Require-Value $Server 'Registered target ID used for the build'
        Invoke-PatchY @('verify', '--server', $Server) -NeedsStormLib
    }
    'PreparePR' {
        $Server = Require-Value $Server 'Registered target ID (for example warmane or wowcircle)'
        $Label = Require-Value $Label 'Short lowercase development label'
        Set-StormLibPath
        Invoke-PatchY @('verify-baseline')
        Invoke-PatchY @('build', '--server', $Server, '--label', $Label)
        Invoke-PatchY @('verify', '--server', $Server)
        Invoke-PatchY @('diff', '--server', $Server)
        Write-Host "`nPASS: attach patch-y\.work\patch-y-diff-$Server.md and the matching JSON file to your PR."
        & git status --short
    }
}
