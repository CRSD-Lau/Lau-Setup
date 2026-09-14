# Author, Creator, Last Modified By: Neil Mitchell
param([switch]$CompileOnly)
$ErrorActionPreference='Stop'
$project=Split-Path -Parent $PSScriptRoot
$compiler='C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
[IO.Directory]::CreateDirectory((Join-Path $project 'build'))|Out-Null
$app=Join-Path $project 'app'
$testArgs=@('/nologo','/target:exe','/main:LocalizationProbe','/platform:anycpu','/optimize+','/warnaserror+','/warn:4',"/out:$project\build\LocalizationTests.exe",'/reference:System.dll','/reference:System.Core.dll','/reference:System.Web.Extensions.dll','/reference:System.Drawing.dll','/reference:System.Windows.Forms.dll',"$app\AssemblyInfo.cs","$app\Core.cs","$app\MpqScan.cs","$app\MapAddons.cs","$app\Downloader.cs","$app\Main.cs","$app\Localization.cs","$project\tests\LocalizationTests.cs","$project\tests\LocalizationProbe.cs","/resource:$app\translations.json,LauSetup.Translations.json")
& $compiler @testArgs
if($LASTEXITCODE-ne 0){throw 'Localization test build failed.'}
if(-not $CompileOnly){
    & "$project\build\LocalizationTests.exe"
    if($LASTEXITCODE-ne 0){throw 'Localization tests failed.'}
}
