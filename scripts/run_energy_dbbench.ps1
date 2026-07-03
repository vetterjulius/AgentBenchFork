# Configuration
$config = "configs/assignments/energy_db.yaml"
$liteConfig = "configs/start_task_lite.yaml"

Write-Host "Starting DBBench Task Workers..."

# Start the task worker in the background
$worker = Start-Process python `
    -ArgumentList "-m", "src.start_task", "-a", "--config", $liteConfig `
    -PassThru

Write-Host "Waiting for task workers to initialize (approx 1 minute)..."

Start-Sleep -Seconds 60

Write-Host "Starting Assigner for Energy Agent on DBBench..."

python -m src.assigner --config $config

Write-Host "Cleaning up task workers..."

if ($worker -and !$worker.HasExited) {
    Stop-Process -Id $worker.Id
}