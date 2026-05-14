<?php

// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 获取表单提交的参数
$machineNumber = $_POST['machineNumber'];
$bearingNumber = $_POST['bearingNumber'];

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 准备 SQL 查询语句
$sql = "SELECT faultDia1, faultLoc1, faultScore1, 
               faultDia2, faultLoc2, faultScore2, 
               faultDia3, faultLoc3, faultScore3 
        FROM bearinginfo 
        WHERE machineNumber = $machineNumber AND bearingNumber = $bearingNumber 
        ORDER BY detectSN DESC";

// 执行 SQL 查询
$result = $conn->query($sql);

// 将查询结果转换为 JSON 格式
$rows = array();
while ($row = $result->fetch_assoc()) {
    $rows[] = $row;
}
echo json_encode($rows);

// 关闭数据库连接
$conn->close();

?>
