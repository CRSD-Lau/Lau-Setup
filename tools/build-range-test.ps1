# Author/Creator/Modifier: Neil Mitchell
$ErrorActionPreference='Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$compiler='C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if(!(Test-Path -LiteralPath 'dist\catalog.json') -or !(Test-Path -LiteralPath 'dist\baseline.json')){throw 'Generate dist\catalog.json and dist\baseline.json before building the ICC range-circle test.'}
$shared=@('/nologo','/r:System.dll','/r:System.Core.dll','/r:System.Web.Extensions.dll','/r:System.Drawing.dll','/r:System.Windows.Forms.dll','/resource:dist\catalog.json,LauSetup.Catalog.json','/resource:dist\baseline.json,LauSetup.Baseline.json','/resource:app\assets\Lau.ico,LauSetup.Icon.ico','app\RangeTestAssemblyInfo.cs','app\Core.cs','app\MpqScan.cs','app\RangeTest.cs')
& $compiler /target:winexe /main:LauSetup.RangeTest /out:dist\LauIccRangeTest.exe /win32icon:app\assets\Lau.ico /win32manifest:app\App.manifest @shared
if($LASTEXITCODE){throw 'ICC range-circle app build failed'}
@'
<?xml version="1.0" encoding="utf-8"?>
<configuration><startup><supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.8"/></startup></configuration>
'@ | Set-Content -LiteralPath dist\LauIccRangeTest.exe.config -Encoding utf8
$core=@('/nologo','/r:System.dll','/r:System.Core.dll','/r:System.Web.Extensions.dll','/r:System.Drawing.dll','/r:System.Windows.Forms.dll','/resource:build\catalog.json,LauSetup.Catalog.json','/resource:app\assets\Lau.ico,LauSetup.Icon.ico','/resource:app\translations.json,LauSetup.Translations.json','app\AssemblyInfo.cs','app\Core.cs','app\MpqScan.cs','app\Downloader.cs','app\Localization.cs','app\Main.cs','tests\LocalizationTests.cs','tests\Tests.cs')
& $compiler /target:exe /main:Tests /out:dist\CoreTests.exe @core
if($LASTEXITCODE){throw 'Shared CoreTests build failed'}
$sha={param([string]$p)if(Test-Path -LiteralPath $p){(Get-FileHash -Algorithm SHA256 -LiteralPath $p).Hash.ToLowerInvariant()}else{$null}}
$writeProvenance={$inputs=[ordered]@{};foreach($path in @('app\Core.cs','app\MpqScan.cs','app\RangeTest.cs','app\RangeTestAssemblyInfo.cs','tests\RangeTestTests.cs','dist\catalog.json','dist\baseline.json','app\assets\Lau.ico','app\App.manifest','app\AssemblyInfo.cs','app\Downloader.cs','app\Localization.cs','app\Main.cs','tests\LocalizationTests.cs','tests\Tests.cs','app\translations.json','build\catalog.json','tools\build-range-test.ps1')){$inputs[$path]=& $sha $path};[ordered]@{Author='Neil Mitchell';Creator='Neil Mitchell';LastModifiedBy='Neil Mitchell';RangeInstallerSha256=& $sha 'dist\LauIccRangeTest.exe';CoreTestsSha256=& $sha 'dist\CoreTests.exe';RangeTestTestsSha256=& $sha 'dist\RangeTestTests.exe';InputSha256=$inputs} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath 'dist\icc-range-build-provenance.json' -Encoding utf8}
if(!(Test-Path -LiteralPath 'dist\payload')){& $writeProvenance;Write-Host 'Payload is absent; app compiled, RangeTestTests.exe intentionally not compiled.';exit 0}
& $compiler /target:exe /main:RangeTestTests /out:dist\RangeTestTests.exe @shared tests\RangeTestTests.cs
if($LASTEXITCODE){throw 'ICC range-circle test build failed'}
& $writeProvenance
