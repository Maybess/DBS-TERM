<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'submit') {
     if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $club_id = $_POST['club_id'];
        $title = $_POST['title'];
        $content = $_POST['content'];
        $author_id = $_POST['author_id'];

        $sql = "INSERT INTO 동아리활동보고서 (동아리_id, 보고서제목, 내용, 제출일, 작성자_id) VALUES (?, ?, ?, CURDATE(), ?)";
        $stmt = $db->prepare($sql);
        $stmt->bind_param("sssi", $club_id, $title, $content, $author_id);
        if ($stmt->execute()) {
                echo "활동 보고서가 등록되었습니다.";
        } else {
             echo "활동 보고서 등록에 실패했습니다: " . $stmt->error;
        }
         $stmt->close();
        ?>
        <br><a href="index.php">메인 메뉴</a>
        <?php
    } else {
        ?>
        <!DOCTYPE html>
        <html>
            <head><title>동아리 활동 보고서 등록</title></head>
           <body>
             <h2>동아리 활동 보고서 등록</h2>
             <form method="post">
                 동아리 ID: <input type="text" name="club_id" required><br>
               보고서 제목: <input type="text" name="title" required><br>
                 내용: <textarea name="content" required></textarea><br>
                 작성자 학번: <input type="text" name="author_id" required><br>
                <input type="submit" value="등록">
            </form>
             <br><a href="index.php">메인 메뉴</a>
            </body>
        </html>
        <?php
    }
} elseif ($action === 'list') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $club_id = $_POST['club_id'];
             $sql = "SELECT * FROM 동아리활동보고서 WHERE 동아리_id = ?";
              $stmt = $db->prepare($sql);
                $stmt->bind_param("s", $club_id);
                $stmt->execute();
              $result = $stmt->get_result();

        ?>
        <!DOCTYPE html>
        <html>
            <head><title>동아리 활동 보고서 목록</title></head>
            <body>
               <h2>동아리 활동 보고서 목록</h2>
                 <?php
                  if ($result->num_rows > 0) {
                     echo "<ul>";
                    while ($row = $result->fetch_assoc()) {
                        echo "<li>ID: {$row['id']}, 제목: {$row['보고서제목']}, 제출일: {$row['제출일']}, 작성자: {$row['작성자_id']}</li>";
                            echo "<p>내용: {$row['내용']}</p>";
                    }
                    echo "</ul>";
                } else {
                   echo "등록된 활동 보고서가 없습니다.";
                }
                ?>
                 <br><a href="index.php">메인 메뉴</a>
           </body>
        </html>
         <?php
        $stmt->close();
    }
    else {
        ?>
        <!DOCTYPE html>
        <html>
           <head><title>동아리 활동 보고서 목록 조회</title></head>
             <body>
               <h2>동아리 활동 보고서 목록 조회</h2>
              <form method="post">
                  동아리 ID: <input type="text" name="club_id" required><br>
                   <input type="submit" value="조회">
                </form>
                <br><a href="index.php">메인 메뉴</a>
            </body>
        </html>
        <?php
    }
}

$db->close();
?>