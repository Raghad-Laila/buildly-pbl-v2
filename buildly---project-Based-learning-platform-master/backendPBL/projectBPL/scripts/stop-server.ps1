# Stops any process listening on Django dev server port 8000.

$ErrorActionPreference = "Continue"
$Port = 8000

$pids = @()

try {
    $connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    foreach ($connection in $connections) {
        if ($connection.OwningProcess -and $pids -notcontains $connection.OwningProcess) {
            $pids += $connection.OwningProcess
        }
    }
} catch {
    $netstat = netstat -ano | Select-String ":$Port\s"
    foreach ($line in $netstat) {
        $parts = ($line -replace '\s+', ' ').Trim().Split(' ')
        $pidValue = [int]$parts[-1]
        if ($pidValue -gt 0 -and $pids -notcontains $pidValue) {
            $pids += $pidValue
        }
    }
}

if ($pids.Count -eq 0) {
    Write-Host "No server found on port $Port."
    exit 0
}

foreach ($processId in $pids) {
    Write-Host "Stopping PID $processId"
    Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
}

Write-Host "Done."
