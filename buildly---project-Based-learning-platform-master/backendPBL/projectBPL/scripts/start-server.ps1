# Starts a single Django dev server on port 8000.
# Stops any existing process bound to that port first.

$ErrorActionPreference = "Continue"
$Port = 8000
$ProjectRoot = Split-Path -Parent $PSScriptRoot

function Stop-PortListeners {
    param([int]$TargetPort)

    $pids = @()

    try {
        $connections = Get-NetTCPConnection -LocalPort $TargetPort -State Listen -ErrorAction SilentlyContinue
        foreach ($connection in $connections) {
            if ($connection.OwningProcess -and $pids -notcontains $connection.OwningProcess) {
                $pids += $connection.OwningProcess
            }
        }
    } catch {
        $netstat = netstat -ano | Select-String ":$TargetPort\s"
        foreach ($line in $netstat) {
            $parts = ($line -replace '\s+', ' ').Trim().Split(' ')
            $pidValue = [int]$parts[-1]
            if ($pidValue -gt 0 -and $pids -notcontains $pidValue) {
                $pids += $pidValue
            }
        }
    }

    foreach ($processId in $pids) {
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Stopping process on port $TargetPort -> PID $processId ($($process.ProcessName))"
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }

    if ($pids.Count -gt 0) {
        Start-Sleep -Seconds 1
    }
}

Write-Host "Preparing Django server on http://127.0.0.1:$Port/"
Stop-PortListeners -TargetPort $Port

Set-Location $ProjectRoot

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Error "Virtual environment not found. Run: python -m venv venv"
    exit 1
}

Write-Host "Starting server..."
& .\venv\Scripts\python.exe manage.py runserver "127.0.0.1:$Port"
