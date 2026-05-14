<?php
// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 获取POST请求中的数据
$detectSN = $_POST['detectSN'];
$machineNumber = $_POST['machineNumber'];
$bearingNumber = $_POST['bearingNumber'];
$faultDia1 = $_POST['faultDia1'];
$faultLoc1 = $_POST['faultLoc1'];
$faultScore1 = $_POST['faultScore1'];
$faultDia2 = $_POST['faultDia2'];
$faultLoc2 = $_POST['faultLoc2'];
$faultScore2 = $_POST['faultScore2'];
$faultDia3 = $_POST['faultDia3'];
$faultLoc3 = $_POST['faultLoc3'];
$faultScore3 = $_POST['faultScore3'];
$detectTime = $_POST['detectTime'];

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 准备SQL语句
$sql = "INSERT INTO bearinginfo (detectSN, machineNumber, bearingNumber, faultDia1, faultLoc1, faultScore1, faultDia2, faultLoc2, faultScore2, faultDia3, faultLoc3, faultScore3, detectTime) 
        VALUES ($detectSN, $machineNumber, $bearingNumber, $faultDia1, $faultLoc1, $faultScore1, $faultDia2, $faultLoc2, $faultScore2, $faultDia3, $faultLoc3, $faultScore3, '$detectTime')";

// 执行SQL语句
if ($conn->query($sql) === TRUE) {
    echo "新记录插入成功";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

// 关闭连接
$conn->close();
?>
