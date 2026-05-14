<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode([
        'ok' => false,
        'error' => 'Invalid request method',
        'method' => $_SERVER['REQUEST_METHOD'],
        'expected' => 'POST'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$machine_id_raw = isset($_POST['machine_id']) ? trim($_POST['machine_id']) : '';
$bearing_id_raw = isset($_POST['bearing_id']) ? trim($_POST['bearing_id']) : '';

if ($machine_id_raw === '' || $bearing_id_raw === '') {
    echo json_encode([
        'ok' => false,
        'error' => 'Missing parameters',
        'required' => ['machine_id', 'bearing_id'],
        'received' => [
            'machine_id' => $machine_id_raw,
            'bearing_id' => $bearing_id_raw
        ]
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// 可选：限制为数字（建议）
if (!ctype_digit($machine_id_raw) || !ctype_digit($bearing_id_raw)) {
    echo json_encode([
        'ok' => false,
        'error' => 'Parameters must be positive integers',
        'received' => [
            'machine_id' => $machine_id_raw,
            'bearing_id' => $bearing_id_raw
        ]
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$machine_id = escapeshellarg($machine_id_raw);
$bearing_id = escapeshellarg($bearing_id_raw);

// ====== 按你的真实路径改这两行 ======
$python_path = 'E:\\exp comter\\remote_interface\\argbearingEnv\\Scripts\\python.exe';
$script_dir  = 'E:\\exp comter\\remote_interface';
// ====================================

$command = 'cd /d "' . $script_dir . '" && "' . $python_path . '" lstm_model.py process ' . $machine_id . ' ' . $bearing_id . ' 2>&1';
$output = shell_exec($command);

if ($output === null || trim($output) === '') {
    echo json_encode([
        'ok' => false,
        'error' => 'Python script returned no output',
        'command' => $command
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$json_output = json_decode($output, true);
if (json_last_error() === JSON_ERROR_NONE) {
    echo json_encode([
        'ok' => true,
        'data' => $json_output
    ], JSON_UNESCAPED_UNICODE);
} else {
    echo json_encode([
        'ok' => false,
        'error' => 'Invalid JSON from Python',
        'json_error' => json_last_error_msg(),
        'raw_output' => $output,
        'command' => $command
    ], JSON_UNESCAPED_UNICODE);
}
?>