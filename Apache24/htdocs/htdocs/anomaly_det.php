<?php

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $machine_id = $_POST['machine_id'];
    $bearing_id = $_POST['bearing_id'];

    // 确保传递给命令的输入是安全的
    $machine_id = escapeshellarg($machine_id);
    $bearing_id = escapeshellarg($bearing_id);

    $command = "cd /d d:\\remote_interface && c:\\Users\\17109\\.conda\\envs\\argbearingEnv\\python.exe anomaly_detection.py process $machine_id $bearing_id";
    
    // 执行命令并捕获输出
    $output = shell_exec($command);

    // 解码 Python 脚本的 JSON 输出
    $json_output = json_decode($output, true);

    // 检查 json_decode 是否成功
    if (json_last_error() === JSON_ERROR_NONE) {
        // 将解码后的 JSON 作为响应返回
        header('Content-Type: application/json');
        echo json_encode($json_output);
    } else {
        // 如果解码 JSON 出错，返回错误信息
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Invalid JSON output from Python script']);
    }
} else {
    echo "Invalid request method.";
}
?>
