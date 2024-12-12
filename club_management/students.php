<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'list') {
    $sql = "SELECT * FROM 학생";
    $result = $db->query($sql);
    ?>
    <!DOCTYPE html>
    <html>
    <head><title>학생 목록</title></head>
    <body>
    <h2>학생 목록</h2>
    <?php
    if ($result->num_rows > 0) {
         echo "<ul>";
        while ($row = $result->fetch_assoc()) {
            echo "<li>학번: {$row['학번']}, 이름: {$row['이름']}, 학과: {$row['학과']}, 이메일: {$row['이메일']}, 연락처: {$row['연락처']}</li>";
        }
        echo "</ul>";
    } else {
        echo "등록된 학생이 없습니다.";
    }
    ?>
        <br><a href="index.php">메인 메뉴</a>
    </body>
    </html>
    <?php
}
elseif ($action === 'register') {
     if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $student_id = $_POST['student_id'];
        $name = $_POST['name'];
        $department = $_POST['department'];
        $email = $_POST['email'];
        $contact = $_POST['contact'];
        $password = $_POST['password'];
         $sql = "INSERT INTO 학생 (학번, 이름, 학과, 이메일, 연락처, 비밀번호) VALUES (?, ?, ?, ?, ?, ?)";
         $stmt = $db->prepare($sql);
         $stmt->bind_param("ssssss", $student_id, $name, $department, $email, $contact, $password);
         if ($stmt->execute()) {
            echo "학생 가입이 성공적으로 완료되었습니다.";
          } else {
            echo "학생 가입에 실패했습니다: " . $stmt->error;
          }
          $stmt->close();
        ?>
         <br><a href="index.php">메인 메뉴</a>
        <?php
    } else {
        ?>
        <!DOCTYPE html>
        <html>
        <head><title>학생 등록</title></head>
        <body>
             <h2>학생 등록</h2>
             <form method="post">
                 학번: <input type="text" name="student_id" required><br>
                이름: <input type="text" name="name" required><br>
                학과: <input type="text" name="department" required><br>
                이메일: <input type="email" name="email" required><br>
                연락처: <input type="text" name="contact" required><br>
                비밀번호: <input type="password" name="password" required><br>
                 <input type="submit" value="등록">
             </form>
            <br><a href="index.php">메인 메뉴</a>
        </body>
        </html>
        <?php
     }
}


$db->close();
?>