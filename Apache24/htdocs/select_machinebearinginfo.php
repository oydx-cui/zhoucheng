<?php

// 设置允许跨域请求的域名，如果是通配符则表示允许所有域名
header('Access-Control-Allow-Origin: *');
// 允许的请求方法，比如GET、POST、OPTIONS等
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
// 允许的请求头字段
header('Access-Control-Allow-Headers: Content-Type');
// 是否允许发送Cookie，这里设置为true，表示允许发送
header('Access-Control-Allow-Credentials: true');

// 连接数据库的凭据
$servername = "localhost";
$username = "root";
$password = "";
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
    // 构建一个数组来存储所有的bearingNumber及其对应的记录列表
    $records = array();
    while ($row = $result_machines->fetch_assoc()) {
        $bearingNumber = $row['bearingNumber'];
        
        // 使用bearingNumber和machineNumber来查询bearinginfo表中的记录
        $sql_bearinginfo = "SELECT * FROM bearinginfo WHERE machineNumber = $machineNumber AND bearingNumber = $bearingNumber";
        $result_bearinginfo = $conn->query($sql_bearinginfo);
        
        // 检查是否有结果
        if ($result_bearinginfo->num_rows > 0) {
            // 将结果存储到数组中
            $records[$bearingNumber] = array();
            while ($row = $result_bearinginfo->fetch_assoc()) {
                $records[$bearingNumber][] = $row;
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
