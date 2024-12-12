<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'list') {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                $club_id = $_POST['club_id'];
            $sql = "SELECT o.역할, s.이름, s.학번, s.이메일, s.연락처 FROM 동아리임원 o JOIN 학생 s ON o.학생_id = s.학번 WHERE o.동아리_id = ?";
        $stmt = $db->prepare($sql);
        $stmt->bind_param("s", $club_id);
        $stmt->execute();
        $result = $stmt->get_result();

    ?>
    <!DOCTYPE html>
    <html>
        <head><title>동아리 임원 목록</title></head>
        <body>
    <h2><?php echo $club_id; ?>번 동아리 임원 목록</h2>
     <?php
            if ($result->num_rows > 0) {
                echo "<ul>";
                while ($row = $result->fetch_assoc()) {
                    echo "<li>역할: {$row['역할']}, 이름: {$row['이름']}, 학번: {$row['학번']}, 이메일: {$row['이메일']}, 연락처: {$row['연락처']}</li>";
                }
                echo "</ul>";
            } else {
                echo "해당 동아리의 임원 정보가 없습니다.";
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
             <head><title>동아리 임원 목록 조회</title></head>
             <body>
                 <h2>동아리 임원 목록 조회</h2>
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
elseif ($action === 'assign') {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $club_id = $_POST['club_id'];
            $student_id = $_POST['student_id'];
            $role = $_POST['role'];
             $sql_check_member = "SELECT * FROM 동아리회원 WHERE 동아리_id = ? AND 학생_id = ?";
              $stmt_check_member = $db->prepare($sql_check_member);
            $stmt_check_member->bind_param("ss", $club_id, $student_id);
             $stmt_check_member->execute();
             $result_member = $stmt_check_member->get_result();

            if ($result_member->num_rows == 0) {
                    echo "해당 학생은 동아리 회원이 아닙니다.";
                }
           else{
               $sql_check_officer = "SELECT * FROM 동아리임원 WHERE 동아리_id = ? AND 학생_id = ?";
                 $stmt_check_officer = $db->prepare($sql_check_officer);
                   $stmt_check_officer->bind_param("ss", $club_id, $student_id);
                 $stmt_check_officer->execute();
                 $result_officer = $stmt_check_officer->get_result();
                      if ($result_officer->num_rows > 0) {
                         echo "해당 학생은 이미 임원입니다.";
                       }
                     else{
                          $sql_insert = "INSERT INTO 동아리임원 (동아리_id, 학생_id, 역할) VALUES (?, ?, ?)";
                          $stmt_insert = $db->prepare($sql_insert);
                             $stmt_insert->bind_param("sss", $club_id, $student_id, $role);
                        if ($stmt_insert->execute()) {
                             echo "{$student_id} 학생을 {$club_id} 동아리의 {$role}으로 임명했습니다.";
                         } else {
                            echo "동아리 임명에 실패했습니다: " . $stmt_insert->error;
                        }
                          $stmt_insert->close();
                     }
                       $stmt_check_officer->close();
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
            <head><title>동아리 임원 임명</title></head>
            <body>
                <h2>동아리 임원 임명</h2>
                <form method="post">
                    동아리 ID: <input type="text" name="club_id" required><br>
                    학생 학번: <input type="text" name="student_id" required><br>
                    역할: <input type="text" name="role" required><br>
                    <input type="submit" value="임명">
                </form>
                 <br><a href="index.php">메인 메뉴</a>
            </body>
         </html>
        <?php
       }
    }


$db->close();
?>