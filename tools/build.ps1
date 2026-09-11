# Author, Creator, Last Modified By: Neil Mitchell
param([switch]$Release)
$ErrorActionPreference='Stop'
$project=Split-Path -Parent $PSScriptRoot
$compiler='C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$catalog=Join-Path $project 'build\catalog.json'
if($Release) {
    $data=Get-Content -LiteralPath $catalog -Raw | ConvertFrom-Json
    if(-not $data.PublicReady){throw 'Release catalog has not passed publication verification.'}
    foreach($asset in $data.Assets.PSObject.Properties.Value){foreach($part in $asset.Parts){if(-not $part.Url){throw 'Public asset URL is missing.'}}}
}
$dist=Join-Path $project 'dist'
[IO.Directory]::CreateDirectory($dist)|Out-Null
$app=Join-Path $project 'app'
$buildArgs=@('/nologo','/target:winexe','/platform:anycpu','/optimize+','/warn:4',"/out:$dist\LauSetup.exe","/win32manifest:$app\App.manifest","/resource:$catalog,LauSetup.Catalog.json",'/reference:System.dll','/reference:System.Core.dll','/reference:System.Drawing.dll','/reference:System.Windows.Forms.dll','/reference:System.Web.Extensions.dll',"$app\AssemblyInfo.cs","$app\Core.cs","$app\Downloader.cs","$app\Main.cs")
$buildArgs += @("/win32icon:$app\assets\Lau.ico","/resource:$app\assets\Lau.ico,LauSetup.Icon.ico")
& $compiler @buildArgs
if($LASTEXITCODE-ne 0){throw 'Installer build failed.'}
@'
<?xml version="1.0" encoding="utf-8"?>
<configuration><startup><supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.8"/></startup></configuration>
'@ | Set-Content -LiteralPath "$dist\LauSetup.exe.config" -Encoding utf8
Get-Item -LiteralPath "$dist\LauSetup.exe" | Select-Object Name,Length,@{n='Product';e={$_.VersionInfo.ProductName}},@{n='Creator';e={$_.VersionInfo.CompanyName}} | ConvertTo-Json
