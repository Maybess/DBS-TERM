<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'register') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $student_id = $_POST['student_id'];
            $graduation_year = $_POST['graduation_year'];
            $current_job = $_POST['current_job'];
            $contact = $_POST['contact'];
            $email = $_POST['email'];

            $sql_check_student = "SELECT * FROM 학생 WHERE 학번 = ?";
             $stmt_check_student = $db->prepare($sql_check_student);
             $stmt_check_student->bind_param("s", $student_id);
                $stmt_check_student->execute();
            $result_student = $stmt_check_student->get_result();

                if ($result_student->num_rows == 0) {
                        echo "해당 학번의 학생 정보가 없습니다.";
                   $stmt_check_student->close();
                 }
           else{
                  $sql_check_alumni = "SELECT * FROM 동문 WHERE 학생_id = ?";
                   $stmt_check_alumni = $db->prepare($sql_check_alumni);
                 $stmt_check_alumni->bind_param("s", $student_id);
                  $stmt_check_alumni->execute();
                $result_alumni = $stmt_check_alumni->get_result();
                    if ($result_alumni->num_rows > 0) {
                        echo "해당 학생의 동문 정보가 이미 등록되어 있습니다.";
                        $stmt_check_alumni->close();
                  }
                 else{
                     $sql_insert = "INSERT INTO 동문 (학생_id, 졸업년도, 현재직업, 연락처, 이메일) VALUES (?, ?, ?, ?, ?)";
                    $stmt_insert = $db->prepare($sql_insert);
                     $stmt_insert->bind_param("sisss", $student_id, $graduation_year, $current_job, $contact, $email);
                     if ($stmt_insert->execute()) {
                           echo "동문 정보가 등록되었습니다.";
                    } else {
                         echo "동문 정보 등록에 실패했습니다: " . $stmt_insert->error;
                     }
                       $stmt_insert->close();
                }
            }
        ?>
         <br><a href="index.php">메인 메뉴</a>
        <?php
    } else {
        ?>
       <!DOCTYPE html>
        <html>
            <head><title>동문 정보 등록</title></head>
           <body>
                 <h2>동문 정보 등록</h2>
                <form method="post">
                   학생 학번: <input type="text" name="student_id" required><br>
                    졸업 연도: <input type="number" name="graduation_year" required><br>
                    현재 직업: <input type="text" name="current_job" required><br>
                  연락처: <input type="text" name="contact" required><br>
                   이메일: <input type="email" name="email" required><br>
                     <input type="submit" value="등록">
               </form>
                 <br><a href="index.php">메인 메뉴</a>
            </body>
        </html>
        <?php
    }
} elseif ($action === 'list') {
    $sql = "SELECT * FROM 동문";
    $result = $db->query($sql);
    ?>
    <!DOCTYPE html>
    <html>
    <head><title>동문 목록</title></head>
    <body>
       <h2>동문 목록</h2>
        <?php
        if ($result->num_rows > 0) {
            echo "<ul>";
            while ($row = $result->fetch_assoc()) {
                echo "<li>ID: {$row['id']}, 학번: {$row['학생_id']}, 졸업년도: {$row['졸업년도']}, 현재직업: {$row['현재직업']}, 연락처: {$row['연락처']}, 이메일: {$row['이메일']}</li>";
            }
             echo "</ul>";
        } else {
            echo "등록된 동문이 없습니다.";
        }
        ?>
        <br><a href="index.php">메인 메뉴</a>
    </body>
    </html>
    <?php
}

$db->close();
?>