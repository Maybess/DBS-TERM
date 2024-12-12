<?php
require 'db.php';

$action = $_GET['action'] ?? '';

$db = connect_to_database();
if ($db === null) {
    die("데이터베이스 연결 실패");
}

if ($action === 'register') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $club_id = $_POST['club_id'];
        $year = $_POST['year'];
        $budget_plan = $_POST['budget_plan'];

        $sql_check = "SELECT * FROM 동아리예산 WHERE 동아리_id = ? AND 연도 = ?";
        $stmt_check = $db->prepare($sql_check);
        $stmt_check->bind_param("si", $club_id, $year);
        $stmt_check->execute();
        $result_check = $stmt_check->get_result();

        if ($result_check->num_rows > 0) {
            echo "해당 연도의 예산이 이미 등록되어 있습니다.";
             $stmt_check->close();
         } else {
                $sql_insert = "INSERT INTO 동아리예산 (동아리_id, 연도, 예산계획) VALUES (?, ?, ?)";
            $stmt_insert = $db->prepare($sql_insert);
             $stmt_insert->bind_param("sii", $club_id, $year, $budget_plan);
               if ($stmt_insert->execute()) {
                   echo "{$year}년도 동아리 예산이 등록되었습니다.";
                } else {
                    echo "예산 등록에 실패했습니다: " . $stmt_insert->error;
                }
             $stmt_insert->close();
         }
         ?>
          <br><a href="index.php">메인 메뉴</a>
         <?php
    } else {
        ?>
        <!DOCTYPE html>
        <html>
            <head><title>동아리 예산 등록</title></head>
            <body>
                <h2>동아리 예산 등록</h2>
                <form method="post">
                    동아리 ID: <input type="text" name="club_id" required><br>
                    연도 (YYYY): <input type="number" name="year" required><br>
                    예산 계획: <input type="number" step="0.01" name="budget_plan" required><br>
                    <input type="submit" value="등록">
                </form>
                <br><a href="index.php">메인 메뉴</a>
           </body>
      </html>
        <?php
    }
} elseif ($action === 'view') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
           $club_id = $_POST['club_id'];
            $year = $_POST['year'];

           $sql_budget = "SELECT * FROM 동아리예산 WHERE 동아리_id = ? AND 연도 = ?";
             $stmt_budget = $db->prepare($sql_budget);
            $stmt_budget->bind_param("si", $club_id, $year);
             $stmt_budget->execute();
            $budget_result = $stmt_budget->get_result();

        if ($budget_result->num_rows == 0) {
              echo "{$year}년도에 해당하는 동아리 예산이 없습니다.";
            $stmt_budget->close();
         } else {
             $budget = $budget_result->fetch_assoc();
             $budget_id = $budget["id"];
             echo "<p>{$year}년도 동아리 예산:</p>";
            echo "<p>예산 ID: {$budget_id}, 예산 계획: {$budget['예산계획']}, 지출 합계: {$budget['지출합계']}, 잔액: {$budget['잔액']}</p>";

            $sql_expenses = "SELECT * FROM 동아리예산지출내역 WHERE 예산_id = ?";
            $stmt_expenses = $db->prepare($sql_expenses);
            $stmt_expenses->bind_param("i", $budget_id);
            $stmt_expenses->execute();
             $expenses_result = $stmt_expenses->get_result();
             echo "<p>{$year}년도 지출 내역:</p>";
              if ($expenses_result->num_rows > 0) {
                  echo "<ul>";
                    while ($expense = $expenses_result->fetch_assoc()) {
                        echo "<li>ID: {$expense['id']}, 지출일: {$expense['지출일']}, 지출 항목: {$expense['지출항목']}, 금액: {$expense['금액']}, 비고: {$expense['비고']}</li>";
                    }
                    echo "</ul>";
            } else {
                 echo "<p>지출 내역이 없습니다.</p>";
            }
            $stmt_expenses->close();
            $stmt_budget->close();
          }
          ?>
           <br><a href="index.php">메인 메뉴</a>
         <?php
    }
     else {
         ?>
        <!DOCTYPE html>
        <html>
            <head><title>동아리 예산 및 지출 내역 조회</title></head>
            <body>
                  <h2>동아리 예산 및 지출 내역 조회</h2>
                <form method="post">
                     동아리 ID: <input type="text" name="club_id" required><br>
                    연도 (YYYY): <input type="number" name="year" required><br>
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