<?php

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $machine_id = $_POST['machine_id'];
    $bearing_id = $_POST['bearing_id'];
    $machine_id = escapeshellarg($machine_id);
    $bearing_id = escapeshellarg($bearing_id);
    $python_path = "E:\\exp comter\\算法模型\\remote_interface\\argbearingEnv\\Scripts\\python.exe";
    $script_dir = "E:\\exp comter\\算法模型\\remote_interface";
    
    $command = "cd /d $script_dir && $python_path anomaly_detection.py process $machine_id $bearing_id";
    
    $output = shell_exec($command);

    if (empty($output)) {
        $output = json_encode(['error' => 'No output from Python script', 'command' => $command]);
    }
    $json_output = json_decode($output, true);
    if (json_last_error() === JSON_ERROR_NONE) {
        header('Content-Type: application/json');
        echo json_encode($json_output);
    } else {
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Invalid JSON output', 'raw_output' => $output]);
    }
} else {
    echo "Invalid request method.";
}
?>