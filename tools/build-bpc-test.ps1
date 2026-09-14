# Author/Creator/Modifier: Neil Mitchell
$ErrorActionPreference='Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$compiler='C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if(!(Test-Path -LiteralPath 'dist\catalog.json') -or !(Test-Path -LiteralPath 'dist\baseline.json')){throw 'Generate the BPC payload first.'}
$shared=@('/nologo','/r:System.dll','/r:System.Core.dll','/r:System.Web.Extensions.dll','/r:System.Drawing.dll','/r:System.Windows.Forms.dll','/resource:dist\catalog.json,LauSetup.Catalog.json','/resource:dist\baseline.json,LauSetup.Baseline.json','/resource:app\assets\Lau.ico,LauSetup.Icon.ico','app\RangeTestAssemblyInfo.cs','app\Core.cs','app\MpqScan.cs','app\RangeTest.cs')
& $compiler /target:winexe /main:LauSetup.RangeTest /out:dist\LauBpcFloorMarkersTest.exe /win32icon:app\assets\Lau.ico /win32manifest:app\App.manifest @shared
if($LASTEXITCODE){throw 'BPC floor-marker installer build failed'}
@'
<?xml version="1.0" encoding="utf-8"?>
<configuration><startup><supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.8"/></startup></configuration>
'@ | Set-Content -LiteralPath dist\LauBpcFloorMarkersTest.exe.config -Encoding utf8
& $compiler /target:exe /main:RangeTestTests /out:dist\RangeTestTests.exe @shared tests\RangeTestTests.cs
if($LASTEXITCODE){throw 'BPC floor-marker installer tests build failed'}
Write-Host 'PASS BPC installer and fixture test runner compiled'
