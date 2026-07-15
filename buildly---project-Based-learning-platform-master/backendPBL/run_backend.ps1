$ProjectDir = Join-Path $PSScriptRoot "projectBPL"
$PythonExe = Join-Path $ProjectDir "venv\Scripts\python.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   تشغيل الباك إند - Django Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (-not (Test-Path $PythonExe)) {
    Write-Host "venv غير موجود في projectBPL/venv" -ForegroundColor Red
    Write-Host "شغّل: .\recreate_venv.ps1" -ForegroundColor Yellow
    exit 1
}

Set-Location $ProjectDir
Write-Host "Python: $(& $PythonExe --version)" -ForegroundColor Green
Write-Host "تطبيق migrations..." -ForegroundColor Yellow
& $PythonExe manage.py migrate
Write-Host ""
Write-Host "السيرفر: http://localhost:8000" -ForegroundColor Green
& $PythonExe manage.py runserver
