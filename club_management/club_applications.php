<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}
if ($action === 'apply') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
         $student_id = $_POST['student_id'];
        $club_id = $_POST['club_id'];
        
        $sql = "INSERT INTO 동아리가입신청 (동아리_id, 학생_id, 신청일, 상태) VALUES (?, ?, CURDATE(), '대기')";
         $stmt = $db->prepare($sql);
         $stmt->bind_param("ss", $club_id, $student_id);
          if ($stmt->execute()) {
                echo "동아리 가입 신청이 완료되었습니다.";
           } else {
                 echo "동아리 가입 신청에 실패했습니다: " . $stmt->error;
           }
        $stmt->close();
            ?>
           <br><a href="index.php">메인 메뉴</a>
            <?php
    } else {
         ?>
         <!DOCTYPE html>
         <html>
            <head><title>동아리 가입 신청</title></head>
            <body>
                <h2>동아리 가입 신청</h2>
                <form method="post">
                 학번: <input type="text" name="student_id" required><br>
                    동아리 ID: <input type="text" name="club_id" required><br>
                    <input type="submit" value="신청">
                </form>
                <br><a href="index.php">메인 메뉴</a>
            </body>
         </html>
         <?php
    }
}
 elseif ($action === 'approve') {
     if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $application_id = $_POST['application_id'];
            $sql_select = "SELECT * FROM 동아리가입신청 WHERE id = ?";
            $stmt_select = $db->prepare($sql_select);
            $stmt_select->bind_param("i", $application_id);
             $stmt_select->execute();
            $result = $stmt_select->get_result();

            if ($result->num_rows == 0) {
                echo "해당 가입 신청 ID가 존재하지 않습니다.";
            }
            else{
            $application = $result->fetch_assoc();
                 if ($application['상태'] != '대기') {
                     echo "이미 처리된 가입 신청입니다.";
                }
                else{
                       $insert_sql = "INSERT INTO 동아리회원 (동아리_id, 학생_id, 가입일) VALUES (?, ?, CURDATE())";
                       $stmt_insert = $db->prepare($insert_sql);
                        $stmt_insert->bind_param("ss", $application['동아리_id'], $application['학생_id']);
                    if($stmt_insert->execute()){
                          $update_sql = "UPDATE 동아리가입신청 SET 상태 = '승인' WHERE id = ?";
                        $stmt_update = $db->prepare($update_sql);
                         $stmt_update->bind_param("i", $application_id);
                       if($stmt_update->execute()){
                              echo "동아리 가입 신청이 승인되었습니다.";
                       }else{
                                echo "동아리 가입 신청 승인에 실패했습니다: " . $stmt_update->error;
                           }
                           $stmt_update->close();
                       } else {
                                echo "동아리 가입 신청 승인에 실패했습니다: " . $stmt_insert->error;
                       }
                        $stmt_insert->close();

                 }

            }
           $stmt_select->close();
        ?>
         <br><a href="index.php">메인 메뉴</a>
         <?php
     }
     else{
    ?>
    <!DOCTYPE html>
    <html>
       <head><title>동아리 가입 승인</title></head>
        <body>
             <h2>동아리 가입 승인</h2>
              <form method="post">
                가입 신청 ID: <input type="number" name="application_id" required><br>
                  <input type="submit" value="승인">
             </form>
            <br><a href="index.php">메인 메뉴</a>
        </body>
     </html>
    <?php
     }
 }
$db->close();
?>