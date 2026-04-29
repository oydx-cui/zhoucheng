<?php
// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 获取POST请求中的用户名和密码
$name = $_POST['name'];
$pwd = $_POST['pwd'];

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 检查用户名是否已存在
$sql_check_user = "SELECT * FROM users WHERE name = '$name'";
$result_check_user = $conn->query($sql_check_user);

if ($result_check_user->num_rows > 0) {
    // 如果用户名已存在，输出提示信息
    echo "用户名已存在，请选择其他用户名";
} else {
    // 如果用户名不存在，将用户名和密码插入到users表中
    $sql_register_user = "INSERT INTO users (name, pwd) VALUES ('$name', '$pwd')";
    
    if ($conn->query($sql_register_user) === TRUE) {
        echo "注册成功";
    } else {
        echo "注册失败: " . $conn->error;
    }
}

// 关闭连接
$conn->close();
?>