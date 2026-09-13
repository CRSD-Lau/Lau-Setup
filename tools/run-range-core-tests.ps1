# Author/Creator/Modifier: Neil Mitchell
param([Parameter(Mandatory=$true)][string]$Output, [Parameter(Mandatory=$true)][string]$FixtureExe)
$ErrorActionPreference='Stop'
$repoRoot=Split-Path -Parent $PSScriptRoot
if(!( [IO.Path]::IsPathRooted($Output)) -or !( [IO.Path]::IsPathRooted($FixtureExe))){throw 'Use absolute fixture paths.'}
$fixtureRoot=[IO.Path]::GetFullPath($Output)
if(Test-Path -LiteralPath $fixtureRoot){throw 'Use a new fixture output directory.'}
if(!(Test-Path -LiteralPath $FixtureExe -PathType Leaf)){throw 'Fixture executable is missing.'}
$runner=Join-Path $repoRoot 'dist\CoreTests.exe'
$provenance=Join-Path $repoRoot 'dist\icc-range-build-provenance.json'
$build=Get-Content -LiteralPath $provenance -Raw | ConvertFrom-Json
$runnerHash=(Get-FileHash -LiteralPath $runner -Algorithm SHA256).Hash.ToLowerInvariant()
if($runnerHash -ne $build.CoreTestsSha256){throw 'Core test runner does not match build provenance.'}
New-Item -ItemType Directory -Path $fixtureRoot | Out-Null
$junctionTarget=Join-Path $fixtureRoot 'junction-target'
$junctionLink=Join-Path $fixtureRoot 'junction-link'
New-Item -ItemType Directory -Path $junctionTarget | Out-Null
New-Item -ItemType Junction -Path $junctionLink -Target $junctionTarget | Out-Null
$previousJunction=$env:LAU_TEST_JUNCTION
$previousStart=$env:LAU_TEST_START_AT
try {
    $env:LAU_TEST_JUNCTION=$junctionLink
    $env:LAU_TEST_START_AT=$null
    & $runner (Join-Path $fixtureRoot 'run') $FixtureExe *> (Join-Path $fixtureRoot 'run.log')
    if($LASTEXITCODE){throw "Core suite failed; see $fixtureRoot\run.log"}
    $resultsPath=Join-Path $fixtureRoot 'run\results.json'
    $results=Get-Content -LiteralPath $resultsPath -Raw | ConvertFrom-Json
    if($results.passed -ne 76 -or $results.results.Count -ne 76 -or $results.StartAt -or @($results.results | Where-Object status -ne 'PASS').Count){throw 'Expected the complete 76-group Core regression run.'}
    if((Get-FileHash -LiteralPath $runner -Algorithm SHA256).Hash.ToLowerInvariant() -ne $runnerHash){throw 'Core runner changed during validation.'}
    [ordered]@{Author='Neil Mitchell';Creator='Neil Mitchell';LastModifiedBy='Neil Mitchell';CoreTestsSha256=$runnerHash;ResultsSha256=(Get-FileHash -LiteralPath $resultsPath -Algorithm SHA256).Hash.ToLowerInvariant();Build=$build} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $fixtureRoot 'core-provenance.json') -Encoding utf8
    Write-Host "PASS all 76 Core regression groups; bound results: $fixtureRoot\core-provenance.json"
} finally {
    $env:LAU_TEST_JUNCTION=$previousJunction
    $env:LAU_TEST_START_AT=$previousStart
}
