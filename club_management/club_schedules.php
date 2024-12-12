<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}
if ($action === 'insert') {
     if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $club_id = $_POST['club_id'];
            $title = $_POST['title'];
            $description = $_POST['description'];
            $date = $_POST['date'];
            $location = $_POST['location'];
             $sql = "INSERT INTO 동아리활동일정 (동아리_id, 제목, 설명, 일정일, 장소) VALUES (?, ?, ?, ?, ?)";
             $stmt = $db->prepare($sql);
             $stmt->bind_param("sssss", $club_id, $title, $description, $date, $location);
             if ($stmt->execute()) {
                 echo "활동 일정이 성공적으로 등록되었습니다.";
             } else {
                echo "활동 일정 등록에 실패했습니다: " . $stmt->error;
            }
             $stmt->close();
            ?>
            <br><a href="index.php">메인 메뉴</a>
            <?php
     } else {
        ?>
        <!DOCTYPE html>
        <html>
             <head><title>동아리 활동 일정 등록</title></head>
             <body>
                  <h2>동아리 활동 일정 등록</h2>
                  <form method="post">
                       동아리 ID: <input type="text" name="club_id" required><br>
                        제목: <input type="text" name="title" required><br>
                        설명: <textarea name="description" required></textarea><br>
                        일정일 (YYYY-MM-DD): <input type="date" name="date" required><br>
                        장소: <input type="text" name="location" required><br>
                        <input type="submit" value="등록">
                   </form>
                   <br><a href="index.php">메인 메뉴</a>
            </body>
        </html>
        <?php
      }
}
elseif ($action === 'list') {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $club_id = $_POST['club_id'];
            $sql = "SELECT id, 제목, 설명, 일정일, 장소 FROM 동아리활동일정 WHERE 동아리_id = ? ORDER BY 일정일";
             $stmt = $db->prepare($sql);
             $stmt->bind_param("s", $club_id);
             $stmt->execute();
            $result = $stmt->get_result();
        ?>
        <!DOCTYPE html>
        <html>
            <head><title>동아리 활동 일정 조회</title></head>
            <body>
                <h2><?php echo $club_id; ?>번 동아리 활동 일정</h2>
                 <?php
                     if ($result->num_rows > 0) {
                         echo "<ul>";
                            while ($row = $result->fetch_assoc()) {
                                echo "<li>ID: {$row['id']}, 제목: {$row['제목']}, 설명: {$row['설명']}, 일정일: {$row['일정일']}, 장소: {$row['장소']}</li>";
                            }
                           echo "</ul>";
                    } else {
                        echo "해당 동아리의 활동 일정이 없습니다.";
                   }
                 ?>
                   <br><a href="index.php">메인 메뉴</a>
            </body>
        </html>
        <?php
          $stmt->close();
         }
     else{
         ?>
        <!DOCTYPE html>
        <html>
            <head><title>동아리 활동 일정 조회</title></head>
            <body>
                  <h2>동아리 활동 일정 조회</h2>
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