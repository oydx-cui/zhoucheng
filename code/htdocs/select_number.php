<?php
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

$sql = "SELECT machineNumber, bearingNumber FROM machines";
$result = $conn->query($sql);

// 检查是否有结果
if ($result->num_rows > 0) {
    // 将结果转换为关联数组
    $data = array();
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    
    // 将数组转换为 JSON 格式并输出
    header('Content-Type: application/json');
    echo json_encode($data);
} else {
    // 如果没有结果，输出空数组
    echo json_encode(array());
}

$conn->close();
?>
