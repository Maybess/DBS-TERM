<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'list') {
    $sql = "SELECT * FROM 동아리";
    $result = $db->query($sql);
    ?>
    <!DOCTYPE html>
    <html>
    <head><title>동아리 목록</title></head>
    <body>
    <h2>동아리 목록</h2>
    <?php
    if ($result->num_rows > 0) {
        echo "<ul>";
        while ($row = $result->fetch_assoc()) {
            echo "<li>ID: {$row['id']}, 이름: {$row['이름']}, 설립일: {$row['설립일']}, 소개: {$row['소개']}, 활동분야: {$row['활동분야']}</li>";
        }
        echo "</ul>";
    } else {
        echo "등록된 동아리가 없습니다.";
    }
    ?>
    <br><a href="index.php">메인 메뉴</a>
    </body>
    </html>
    <?php
} elseif ($action === 'search') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $club_name = $_POST['club_name'];
        $sql = "SELECT * FROM 동아리 WHERE 이름 LIKE ?";
        $stmt = $db->prepare($sql);
        $stmt->bind_param("s", $search_term = "%" . $club_name . "%");
        $stmt->execute();
        $result = $stmt->get_result();
        ?>
    <!DOCTYPE html>
    <html>
        <head><title>동아리 검색 결과</title></head>
        <body>
    <h2>동아리 검색 결과</h2>
    <?php
        if ($result->num_rows > 0) {
             echo "<ul>";
            while ($row = $result->fetch_assoc()) {
                echo "<li>ID: {$row['id']}, 이름: {$row['이름']}, 설립일: {$row['설립일']}, 소개: {$row['소개']}, 활동분야: {$row['활동분야']}</li>";
            }
             echo "</ul>";
        } else {
            echo "검색된 동아리가 없습니다.";
        }
        ?>
           <br><a href="index.php">메인 메뉴</a>
           </body>
        </html>
        <?php
        $stmt->close();

    } else {
        ?>
    <!DOCTYPE html>
    <html>
       <head><title>동아리 검색</title></head>
       <body>
        <h2>동아리 검색</h2>
         <form method="post">
            동아리 이름: <input type="text" name="club_name"><br>
            <input type="submit" value="검색">
        </form>
           <br><a href="index.php">메인 메뉴</a>
       </body>
    </html>
    <?php
    }
}
elseif ($action === 'insert') {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $name = $_POST['name'];
            $establishment_date = $_POST['establishment_date'];
            $introduction = $_POST['introduction'];
            $field = $_POST['field'];
            $logo = $_POST['logo'];
            
            $sql = "INSERT INTO 동아리 (이름, 설립일, 소개, 활동분야, 로고) VALUES (?, ?, ?, ?, ?)";
            $stmt = $db->prepare($sql);
            $stmt->bind_param("sssss", $name, $establishment_date, $introduction, $field, $logo);
             if ($stmt->execute()) {
            echo "동아리가 성공적으로 등록되었습니다.";
        } else {
             echo "동아리 등록에 실패했습니다: " . $stmt->error;
        }
            $stmt->close();
            ?>
            <br><a href="index.php">메인 메뉴</a>
            <?php
         } else {
            ?>
    <!DOCTYPE html>
    <html>
    <head><title>동아리 등록</title></head>
       <body>
        <h2>동아리 등록</h2>
        <form method="post">
            이름: <input type="text" name="name" required><br>
            설립일 (YYYY-MM-DD): <input type="date" name="establishment_date" required><br>
            소개: <textarea name="introduction" required></textarea><br>
            활동분야: <input type="text" name="field" required><br>
            로고 파일 경로: <input type="text" name="logo"><br>
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