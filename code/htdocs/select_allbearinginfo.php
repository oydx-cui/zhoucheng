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

// 执行 SQL 查询
$sql = "SELECT detectTime, machineNumber, bearingNumber, faultDia1, faultLoc1, faultScore1, faultDia2, faultLoc2, faultScore2, faultDia3, faultLoc3, faultScore3 FROM bearinginfo ORDER BY detectTime ASC";
$result = $conn->query($sql);

// 输出数据为 JSON 格式
$output = array();
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $output[] = $row;
    }
} 

// 输出 JSON 数据
echo json_encode($output);

// 关闭连接
$conn->close();

?>
