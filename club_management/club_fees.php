<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}
if ($action === 'pay') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $club_id = $_POST['club_id'];
             $student_id = $_POST['student_id'];
            $amount = $_POST['amount'];

             $sql_check_member = "SELECT * FROM 동아리회원 WHERE 동아리_id = ? AND 학생_id = ?";
             $stmt_check_member = $db->prepare($sql_check_member);
               $stmt_check_member->bind_param("ss", $club_id, $student_id);
             $stmt_check_member->execute();
            $result_member = $stmt_check_member->get_result();
                 if ($result_member->num_rows == 0) {
                    echo "해당 학생은 동아리 회원이 아닙니다.";
                    $stmt_check_member->close();
                 }
           else{
                    $sql_check_payment = "SELECT * FROM 동아리회비 WHERE 동아리_id = ? AND 학생_id = ? AND 납부여부 = 'Y'";
                    $stmt_check_payment = $db->prepare($sql_check_payment);
                    $stmt_check_payment->bind_param("ss", $club_id, $student_id);
                       $stmt_check_payment->execute();
                   $result_payment = $stmt_check_payment->get_result();
                    if ($result_payment->num_rows > 0) {
                      echo "해당 학생은 이미 회비를 납부했습니다.";
                       $stmt_check_payment->close();
                    }else{
                         $sql_check_existing_record = "SELECT * FROM 동아리회비 WHERE 동아리_id = ? AND 학생_id = ?";
                            $stmt_check_existing_record = $db->prepare($sql_check_existing_record);
                           $stmt_check_existing_record->bind_param("ss", $club_id, $student_id);
                            $stmt_check_existing_record->execute();
                             $result_existing_record = $stmt_check_existing_record->get_result();

                         if ($result_existing_record->num_rows > 0) {
                                $existing_record = $result_existing_record->fetch_assoc();
                                $update_sql = "UPDATE 동아리회비 SET 납부금액 = ?, 납부일 = CURDATE(), 납부여부 = 'Y' WHERE id = ?";
                                    $stmt_update = $db->prepare($update_sql);
                                      $stmt_update->bind_param("di", $amount, $existing_record['id']);
                                   if($stmt_update->execute()){
                                       echo "회비 납부 정보가 업데이트되었습니다.";
                                   } else {
                                      echo "회비 납부 정보 업데이트에 실패했습니다: " . $stmt_update->error;
                                   }
                                   $stmt_update->close();
                             } else {
                                $insert_sql = "INSERT INTO 동아리회비 (동아리_id, 학생_id, 납부금액, 납부일, 납부여부) VALUES (?, ?, ?, CURDATE(), 'Y')";
                               $stmt_insert = $db->prepare($insert_sql);
                               $stmt_insert->bind_param("ssd", $club_id, $student_id, $amount);
                              if($stmt_insert->execute()){
                                echo "회비 납부 정보가 등록되었습니다.";
                             } else {
                                 echo "회비 납부 정보 등록에 실패했습니다: " . $stmt_insert->error;
                               }
                                  $stmt_insert->close();
                          }
                        $stmt_check_existing_record->close();
                    }
            }
               ?>
           <br><a href="index.php">메인 메뉴</a>
         <?php
       }
     else {
        ?>
        <!DOCTYPE html>
        <html>
             <head><title>동아리 회비 납부</title></head>
              <body>
                  <h2>동아리 회비 납부</h2>
                    <form method="post">
                         동아리 ID: <input type="text" name="club_id" required><br>
                         학생 학번: <input type="text" name="student_id" required><br>
                        납부 금액: <input type="number" step="0.01" name="amount" required><br>
                        <input type="submit" value="납부">
                    </form>
                   <br><a href="index.php">메인 메뉴</a>
            </body>
        </html>
        <?php
       }
}
elseif ($action === 'view') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $club_id = $_POST['club_id'];

        $sql = "
        SELECT 
            m.학생_id, 
            s.이름, 
            s.학과,
            COALESCE(f.납부금액, 0) as 납부금액, 
            f.납부일, 
            COALESCE(f.납부여부, 'N') as 납부여부
        FROM 동아리회원 m
        JOIN 학생 s ON m.학생_id = s.학번
        LEFT JOIN 동아리회비 f ON m.동아리_id = f.동아리_id AND m.학생_id = f.학생_id
        WHERE m.동아리_id = ?
    ";
        $stmt = $db->prepare($sql);
        $stmt->bind_param("s", $club_id);
        $stmt->execute();
        $result = $stmt->get_result();

         ?>
        <!DOCTYPE html>
        <html>
           <head><title>동아리별 회비 납부 현황 조회</title></head>
           <body>
             <h2><?php echo $club_id; ?>번 동아리 회비 납부 현황</h2>
            <?php
           if ($result->num_rows > 0) {
                echo "<table border='1'>";
                echo "<tr><th>학번</th><th>이름</th><th>학과</th><th>납부금액</th><th>납부일</th><th>납부여부</th></tr>";
               while ($member = $result->fetch_assoc()) {
                    echo "<tr>";
                    echo "<td>{$member['학생_id']}</td>";
                    echo "<td>{$member['이름']}</td>";
                   echo "<td>{$member['학과']}</td>";
                    echo "<td>{$member['납부금액']}</td>";
                    echo "<td>" . ($member['납부일'] ? $member['납부일'] : '') . "</td>";
                     echo "<td>{$member['납부여부']}</td>";
                  echo "</tr>";
             }
                 echo "</table>";
           } else {
                echo "해당 동아리의 회원이 없거나 회비 정보가 없습니다.";
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
             <head><title>동아리별 회비 납부 현황 조회</title></head>
              <body>
                  <h2>동아리별 회비 납부 현황 조회</h2>
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