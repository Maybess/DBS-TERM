<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'request') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $club_id = $_POST['club_id'];
        $item_name = $_POST['item_name'];
        $quantity = $_POST['quantity'];
        $applicant_id = $_POST['applicant_id'];
        $purpose = $_POST['purpose'];
        $sql = "INSERT INTO 물품신청 (동아리_id, 물품명, 수량, 신청일, 상태, 신청자_id, 용도) VALUES (?, ?, ?, CURDATE(), '대기', ?, ?)";
        $stmt = $db->prepare($sql);
        $stmt->bind_param("ssiis", $club_id, $item_name, $quantity, $applicant_id, $purpose);
        if ($stmt->execute()) {
            echo "물품 신청이 완료되었습니다.";
        } else {
            echo "물품 신청에 실패했습니다: " . $stmt->error;
        }
        $stmt->close();
        ?>
        <br><a href="index.php">메인 메뉴</a>
        <?php
    } else {
        ?>
        <!DOCTYPE html>
        <html>
        <head><title>물품 신청</title></head>
        <body>
        <h2>물품 신청</h2>
        <form method="post">
            동아리 ID: <input type="text" name="club_id" required><br>
            물품명: <input type="text" name="item_name" required><br>
            수량: <input type="number" name="quantity" required><br>
            신청자 학번: <input type="text" name="applicant_id" required><br>
            용도: <input type="text" name="purpose" required><br>
            <input type="submit" value="신청">
        </form>
        <br><a href="index.php">메인 메뉴</a>
        </body>
        </html>
        <?php
    }
} elseif ($action === 'list') {
     if ($_SERVER['REQUEST_METHOD'] === 'POST') {
         $club_id = $_POST['club_id'];
         if(strtolower($club_id) == 'all'){
             $sql = "SELECT * FROM 물품신청";
             $stmt = $db->prepare($sql);
                $stmt->execute();
                $result = $stmt->get_result();
          } else {
            $sql = "SELECT * FROM 물품신청 WHERE 동아리_id = ?";
              $stmt = $db->prepare($sql);
                $stmt->bind_param("s", $club_id);
                $stmt->execute();
             $result = $stmt->get_result();
          }
        ?>
        <!DOCTYPE html>
        <html>
            <head><title>물품 신청 목록</title></head>
           <body>
           <h2>물품 신청 목록</h2>
            <?php
            if ($result->num_rows > 0) {
                echo "<ul>";
                while ($row = $result->fetch_assoc()) {
                    echo "<li>ID: {$row['id']}, 동아리ID: {$row['동아리_id']}, 물품명: {$row['물품명']}, 수량: {$row['수량']}, 신청일: {$row['신청일']}, 상태: {$row['상태']}, 신청자: {$row['신청자_id']}, 용도: {$row['용도']}</li>";
                }
                echo "</ul>";
            } else {
                echo "신청된 물품이 없습니다.";
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
            <head><title>물품 신청 목록 조회</title></head>
            <body>
                 <h2>물품 신청 목록 조회</h2>
                <form method="post">
                     동아리 ID (전체는 'all' 입력): <input type="text" name="club_id" required><br>
                     <input type="submit" value="조회">
                </form>
                <br><a href="index.php">메인 메뉴</a>
             </body>
       </html>
         <?php
     }
} elseif ($action === 'process') {
     if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $request_id = $_POST['request_id'];
        $action_type = $_POST['action_type'];
        if (strtolower($action_type) !== '승인' && strtolower($action_type) !== '거절') {
            echo "잘못된 입력입니다.";
            exit;
          }

         $sql = "UPDATE 물품신청 SET 상태 = ? WHERE id = ?";
         $stmt = $db->prepare($sql);
        $stmt->bind_param("si", $action_type, $request_id);
         if ($stmt->execute()) {
            echo "물품 신청 ID {$request_id}이(가) {$action_type} 처리되었습니다.";
        } else {
            echo "물품 신청 처리 오류: " . $stmt->error;
         }
          $stmt->close();
         ?>
          <br><a href="index.php">메인 메뉴</a>
         <?php
     } else {
    ?>
        <!DOCTYPE html>
        <html>
        <head><title>물품 신청 승인/거절</title></head>
        <body>
            <h2>물품 신청 승인/거절</h2>
            <form method="post">
                물품 신청 ID: <input type="number" name="request_id" required><br>
                 승인/거절 (승인/거절): <input type="text" name="action_type" required><br>
                <input type="submit" value="처리">
            </form>
            <br><a href="index.php">메인 메뉴</a>
         </body>
        </html>
        <?php
    }
}
$db->close();
?>