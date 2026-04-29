<?php
// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 创建数据库连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 获取请求参数（这里假设通过POST请求传递了machineNumber和bearingNumber参数）
$machineNumber = $_POST['machineNumber'];
$bearingNumber = $_POST['bearingNumber'];

// 执行SQL查询语句
$sql = "SELECT detectTime, machineNumber, bearingNumber, faultDia1, faultLoc1, faultScore1,
        faultDia2, faultLoc2, faultScore2,
        faultDia3, faultLoc3, faultScore3 FROM bearinginfo 
        WHERE machineNumber = $machineNumber AND bearingNumber = $bearingNumber 
        ORDER BY detectSN DESC";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 将查询结果转换为关联数组
    $data = array();
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }

    // 将数组转换为JSON格式并输出到页面
    header('Content-Type: application/json');
    echo json_encode($data);
} else {
    // 没有数据时输出空的JSON对象
    echo json_encode(array());
}

// 关闭数据库连接
$conn->close();
?>
