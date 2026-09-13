# Author/Creator/Modifier: Neil Mitchell
$ErrorActionPreference='Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$compiler='C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$shared=@('/nologo','/r:System.dll','/r:System.Core.dll','/r:System.Web.Extensions.dll','/r:System.Drawing.dll','/r:System.Windows.Forms.dll','/resource:dist\catalog.json,LauSetup.Catalog.json','/resource:dist\baseline.json,LauSetup.Baseline.json','/resource:app\assets\Lau.ico,LauSetup.Icon.ico','app\AssemblyInfo.cs','app\Core.cs','app\LadyTest.cs')
& $compiler /target:winexe /main:LauSetup.LadyTest /out:dist\LauSetup.exe /win32icon:app\assets\Lau.ico /win32manifest:app\App.manifest @shared
if($LASTEXITCODE){throw 'App build failed'}
& $compiler /target:exe /main:LadyTestTests /out:dist\LadyTestTests.exe @shared tests\LadyTestTests.cs
if($LASTEXITCODE){throw 'Test build failed'}
@'
<?xml version="1.0" encoding="utf-8"?>
<configuration><startup><supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.8"/></startup></configuration>
'@ | Set-Content -LiteralPath dist\LauSetup.exe.config -Encoding utf8
