<?php
// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 从 POST 请求中获取参数
$machineNumber = $_POST['machineNumber'];
$bearingNumber = $_POST['bearingNumber'];

// 创建数据库连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 准备 SQL 查询语句
$sql = "SELECT faultDia1, faultDia2, detectTime FROM bearinginfo WHERE machineNumber = $machineNumber AND bearingNumber = $bearingNumber";

// 执行查询
$result = $conn->query($sql);

// 检查查询结果
if ($result->num_rows > 0) {
    // 构造 JSON 数据数组
    $data = array();
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    // 输出 JSON 数据
    header('Content-Type: application/json');
    echo json_encode($data);
} else {
    // 输出空数组
    header('Content-Type: application/json');
    echo json_encode(array());
}

// 关闭数据库连接
$conn->close();
?>
