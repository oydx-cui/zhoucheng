<?php
// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 获取POST请求中的machineNumber
$machineNumber = $_POST['machineNumber'];

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 查询machines表，获取与指定machineNumber相匹配的所有bearingNumber
$sql_machines = "SELECT bearingNumber FROM machines WHERE machineNumber = $machineNumber";
$result_machines = $conn->query($sql_machines);

// 检查是否有结果
if ($result_machines->num_rows > 0) {
    // 构建一个数组来存储所有的bearingNumber
    $bearingNumbers = array();
    while ($row = $result_machines->fetch_assoc()) {
        $bearingNumbers[] = $row['bearingNumber'];
    }

    // 使用bearingNumber和machineNumber来查询bearinginfo表中的记录
    $records = array();
    foreach ($bearingNumbers as $bearingNumber) {
        $sql_rul_pred = "SELECT * FROM rul_pred WHERE machineNumber = $machineNumber AND bearingNumber = $bearingNumber";
        $result_rul_pred = $conn->query($sql_rul_pred);
        
        // 检查是否有结果
        if ($result_rul_pred->num_rows > 0) {
            // 将结果存储到数组中
            while ($row = $result_rul_pred->fetch_assoc()) {
                $records[] = $row;
            }
        }
    }
    
    // 将数组转换为 JSON 格式并输出
    header('Content-Type: application/json');
    echo json_encode($records);
} else {
    // 如果没有结果，输出空数组
    echo json_encode(array());
}

// 关闭连接
$conn->close();
?>
