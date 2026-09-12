# Author/Creator/Modifier: Neil Mitchell
$ErrorActionPreference='Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$compiler='C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$shared=@('/nologo','/r:System.dll','/r:System.Core.dll','/r:System.Web.Extensions.dll','/r:System.Drawing.dll','/r:System.Windows.Forms.dll','/resource:dist\catalog.json,LauSetup.Catalog.json','/resource:dist\baseline.json,LauSetup.Baseline.json','/resource:app\assets\Lau.ico,LauSetup.Icon.ico','app\AssemblyInfo.cs','app\Core.cs','app\HalionTest.cs')
& $compiler /target:winexe /main:LauSetup.HalionTest /out:dist\LauSetup.exe /win32icon:app\assets\Lau.ico /win32manifest:app\App.manifest @shared
if($LASTEXITCODE){throw 'App build failed'}
& $compiler /target:exe /main:HalionTestTests /out:dist\HalionTestTests.exe @shared tests\HalionTestTests.cs
if($LASTEXITCODE){throw 'Test build failed'}
