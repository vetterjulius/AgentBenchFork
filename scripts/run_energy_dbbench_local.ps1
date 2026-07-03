# Configuration
$config = "configs/assignments/energy_db_local.yaml"
$liteConfig = "configs/start_task_lite.yaml"
$dockerLite = "extra/docker-compose-lite.yml"

Write-Host "Starting minimal Docker infrastructure (Controller & Redis)..."
docker compose -f $dockerLite up -d

Write-Host "Waiting for infrastructure to be ready..."
Start-Sleep -Seconds 5

Write-Host "Starting DBBench Task Workers locally..."
# Start the task worker in the background
$worker = Start-Process python `
    -ArgumentList "-m", "src.start_task", "-a", "--config", $liteConfig `
    -PassThru

Write-Host "Waiting for task workers to initialize..."
Start-Sleep -Seconds 10

Write-Host "Starting Assigner for Energy Agent on DBBench (LOCAL)..."
python -m src.assigner --config $config

Write-Host "Cleaning up..."
if ($worker -and !$worker.HasExited) {
    Stop-Process -Id $worker.Id
}
docker compose -f $dockerLite down
