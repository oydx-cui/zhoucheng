<?php
// 连接数据库的凭据
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

// 查询bearinginfo表中detectSN的最大值
$sql = "SELECT IFNULL(MAX(detectSN), 0) AS max_detectSN FROM bearinginfo";
$result = $conn->query($sql);

// 检查是否有结果
if ($result->num_rows > 0) {
    // 获取查询结果的第一行
    $row = $result->fetch_assoc();
    
    // 将结果转换为 JSON 格式并输出
    header('Content-Type: application/json');
    echo json_encode($row);
} else {
    // 如果没有结果，输出 max_detectSN 为 0
    echo json_encode(array('max_detectSN' => 0));
}

// 关闭连接
$conn->close();
?>
