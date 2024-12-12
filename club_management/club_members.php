<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'withdraw') {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $student_id = $_POST['student_id'];
            $club_id = $_POST['club_id'];
            $sql_check_member = "SELECT * FROM 동아리회원 WHERE 동아리_id = ? AND 학생_id = ?";
            $stmt_check_member = $db->prepare($sql_check_member);
              $stmt_check_member->bind_param("ss", $club_id, $student_id);
               $stmt_check_member->execute();
            $result_member = $stmt_check_member->get_result();

                if ($result_member->num_rows == 0) {
                     echo "해당 동아리의 회원이 아닙니다.";
                    }
                 else{
                           $delete_sql = "DELETE FROM 동아리회원 WHERE 동아리_id = ? AND 학생_id = ?";
                       $stmt_delete = $db->prepare($delete_sql);
                        $stmt_delete->bind_param("ss", $club_id, $student_id);
                         if($stmt_delete->execute()){
                             echo "동아리에서 탈퇴 처리되었습니다.";
                        } else {
                            echo "동아리 탈퇴 처리에 실패했습니다: " . $stmt_delete->error;
                          }
                          $stmt_delete->close();
                 }
                $stmt_check_member->close();
            ?>
             <br><a href="index.php">메인 메뉴</a>
            <?php
         }
        else {
        ?>
    <!DOCTYPE html>
    <html>
        <head><title>동아리 탈퇴</title></head>
       <body>
        <h2>동아리 탈퇴</h2>
        <form method="post">
            학번: <input type="text" name="student_id" required><br>
            동아리 ID: <input type="text" name="club_id" required><br>
            <input type="submit" value="탈퇴">
       </form>
        <br><a href="index.php">메인 메뉴</a>
       </body>
     </html>
    <?php
        }
}

$db->close();
?>