<?php
require 'config.php';

function connect_to_database() {
    global $config;
    try {
        $conn = new mysqli($config['host'], $config['user'], $config['password'], $config['database']);
        if ($conn->connect_error) {
            throw new Exception("MySQL 연결 오류: " . $conn->connect_error);
        }
        $conn->set_charset("utf8"); // UTF-8 설정
        return $conn;
    } catch (Exception $e) {
        echo "MySQL 연결 오류: " . $e->getMessage();
        return null;
    }
}
?>