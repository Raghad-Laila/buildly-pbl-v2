$ProjectDir = Join-Path $PSScriptRoot "projectBPL"
$VenvPath = Join-Path $ProjectDir "venv"
$Requirements = Join-Path $ProjectDir "requirements.txt"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   إعادة إنشاء venv (مكان واحد فقط)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "المسار: $VenvPath" -ForegroundColor Gray
Write-Host ""

Write-Host "[1/5] التحقق من Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python غير مثبت!" -ForegroundColor Red
    exit 1
}
Write-Host "OK $pythonVersion" -ForegroundColor Green

Write-Host "[2/5] حذف venv القديم..." -ForegroundColor Yellow
if (Test-Path $VenvPath) {
    Remove-Item -Recurse -Force $VenvPath
}
$LegacyVenv = Join-Path $PSScriptRoot "venv"
if (Test-Path $LegacyVenv) {
    Remove-Item -Recurse -Force $LegacyVenv
    Write-Host "تم حذف venv القديم المكرر في backendPBL/venv" -ForegroundColor Green
}
Write-Host "OK" -ForegroundColor Green

Write-Host "[3/5] إنشاء venv جديد..." -ForegroundColor Yellow
python -m venv $VenvPath
if ($LASTEXITCODE -ne 0) { exit 1 }
Write-Host "OK" -ForegroundColor Green

Write-Host "[4/5] تثبيت الحزم..." -ForegroundColor Yellow
& (Join-Path $VenvPath "Scripts\python.exe") -m pip install --upgrade pip --quiet
& (Join-Path $VenvPath "Scripts\pip.exe") install -r $Requirements
if ($LASTEXITCODE -ne 0) { exit 1 }
Write-Host "OK" -ForegroundColor Green

Write-Host "[5/5] التحقق..." -ForegroundColor Yellow
& (Join-Path $VenvPath "Scripts\python.exe") --version
Write-Host ""
Write-Host "venv جاهز في: backendPBL/projectBPL/venv" -ForegroundColor Green
Write-Host "لتشغيل السيرفر: cd projectBPL; .\venv\Scripts\python.exe manage.py runserver" -ForegroundColor Cyan
