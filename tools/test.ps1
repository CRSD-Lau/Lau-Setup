# Author, Creator, Last Modified By: Neil Mitchell
param([string]$ClientExecutable,[switch]$CompileOnly)
$ErrorActionPreference='Stop'
$project=Split-Path -Parent $PSScriptRoot
$compiler='C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$testArgs=@('/nologo','/target:exe','/main:Tests','/platform:anycpu','/optimize+','/warnaserror+','/warn:4',"/out:$project\build\Tests.exe",'/reference:System.dll','/reference:System.Core.dll','/reference:System.Web.Extensions.dll','/reference:System.Drawing.dll','/reference:System.Windows.Forms.dll',"$project\app\AssemblyInfo.cs","$project\app\Core.cs","$project\app\MpqScan.cs","$project\app\Downloader.cs","$project\app\Main.cs","$project\tests\Tests.cs")
$testArgs += @("$project\app\Localization.cs","$project\tests\LocalizationTests.cs","/resource:$project\app\translations.json,LauSetup.Translations.json")
& $compiler @testArgs
if($LASTEXITCODE-ne 0){throw 'Test build failed.'}
if($CompileOnly){return}
$source=if($ClientExecutable){[IO.Path]::GetFullPath($ClientExecutable)}elseif(Test-Path -LiteralPath "$project\build\source-index.json"){(Get-Content -LiteralPath "$project\build\source-index.json" -Raw|ConvertFrom-Json).sources.Executable}else{throw 'Pass -ClientExecutable with a WoW 3.3.5a build 12340 executable. Tests copy it into isolated fixtures.'}
$output=Join-Path $project ('reports\tests-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
$junctionRoot=Join-Path $project ('build\junction-'+[Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory((Join-Path $junctionRoot 'target'))|Out-Null
$env:LAU_TEST_JUNCTION=Join-Path $junctionRoot 'link'
New-Item -ItemType Junction -Path $env:LAU_TEST_JUNCTION -Target (Join-Path $junctionRoot 'target')|Out-Null
& "$project\build\Tests.exe" $output $source
if($LASTEXITCODE-ne 0){throw "Tests failed. Evidence: $output"}
Write-Output "Evidence: $output"
