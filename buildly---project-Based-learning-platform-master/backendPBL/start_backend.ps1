$ProjectDir = Join-Path $PSScriptRoot "projectBPL"
$PythonExe = Join-Path $ProjectDir "venv\Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "venv غير موجود. شغّل: .\recreate_venv.ps1" -ForegroundColor Red
    exit 1
}

Set-Location $ProjectDir
Write-Host "تشغيل السيرفر على http://localhost:8000" -ForegroundColor Green
& $PythonExe manage.py runserver
