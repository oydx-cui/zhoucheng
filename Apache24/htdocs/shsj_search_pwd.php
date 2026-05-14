<?php
// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "bs_showdata";

// 获取POST请求中的用户名
$name = $_POST['name'];

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 查询users表，获取与指定用户名相匹配的密码
$sql_users = "SELECT password FROM tb_admin WHERE username = '$name'";
$result_users = $conn->query($sql_users);

// 检查是否有结果
if ($result_users->num_rows > 0) {
    // 将结果存储到关联数组中
    $row = $result_users->fetch_assoc();
    
    // 输出密码
    echo $row['password'];
} else {
    // 如果没有结果，输出空
    echo "用户不存在或密码为空";
}

// 关闭连接
$conn->close();
?>