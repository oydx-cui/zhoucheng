<?php
// 连接数据库的凭据
$servername = "172.20.10.3";
$username = "argSysAdmin";
$password = "argbearing";
$dbname = "argbearing_db";

// 获取POST请求中的用户名和新密码
$name = $_POST['name'];
$new_pwd = $_POST['new_pwd'];

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 查询users表，获取与指定用户名相匹配的密码
$sql_users = "SELECT pwd FROM users WHERE name = '$name'";
$result_users = $conn->query($sql_users);

// 检查是否有结果
if ($result_users->num_rows > 0) {
    // 执行更新密码的操作
    $sql_update_pwd = "UPDATE users SET pwd = '$new_pwd' WHERE name = '$name'";
    
    if ($conn->query($sql_update_pwd) === TRUE) {
        echo "密码修改成功";
    } else {
        echo "密码修改失败: " . $conn->error;
    }
} else {
    // 如果没有结果，输出提示信息
    echo "用户不存在";
}

// 关闭连接
$conn->close();
?>