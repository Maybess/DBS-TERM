<!DOCTYPE html>
<html>
<head>
    <title>동아리 관리 시스템</title>
    <style>
        body { font-family: sans-serif; }
        h2 { border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 10px; }
        ul { list-style-type: none; padding: 0; }
        li { margin-bottom: 5px; }
        a { display: block; padding: 10px; background-color: #f0f0f0; text-decoration: none; color: #333; border: 1px solid #ddd; border-radius: 5px; }
        a:hover { background-color: #e0e0e0; }
        .container { width: 80%; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
        .form-container { margin-top: 20px; padding: 15px; border: 1px solid #eee; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>동아리 관리 시스템 메뉴</h2>
        <ul>
            <li><a href="clubs.php?action=list">1. 동아리 목록 조회</a></li>
            <li><a href="clubs.php?action=search">2. 동아리 검색</a></li>
            <li><a href="clubs.php?action=insert">3. 동아리 등록</a></li>
            <li><a href="students.php?action=list">4. 학생 목록 조회</a></li>
            <li><a href="students.php?action=register">5. 학생 가입</a></li>
             <li><a href="club_applications.php?action=apply">6. 동아리 가입 신청</a></li>
            <li><a href="club_applications.php?action=approve">7. 동아리 가입 승인</a></li>
            <li><a href="club_officers.php?action=list">8. 동아리 임원 목록 조회</a></li>
            <li><a href="club_members.php?action=withdraw">9. 동아리 탈퇴</a></li>
            <li><a href="club_officers.php?action=assign">10. 동아리 임원 임명</a></li>
            <li><a href="club_notices.php?action=insert">11. 공지사항 등록</a></li>
            <li><a href="club_schedules.php?action=insert">12. 동아리 활동 일정 등록</a></li>
            <li><a href="club_schedules.php?action=list">13. 동아리 활동 일정 조회</a></li>
           <li><a href="item_requests.php?action=request">14. 물품 신청</a></li>
            <li><a href="item_requests.php?action=list">15. 물품 신청 목록 조회</a></li>
            <li><a href="item_requests.php?action=process">16. 물품 신청 승인/거절</a></li>
            <li><a href="club_budgets.php?action=register">17. 동아리 예산 등록</a></li>
            <li><a href="club_expenses.php?action=register">18. 동아리 지출 내역 등록</a></li>
            <li><a href="club_budgets.php?action=view">19. 동아리 예산 및 지출 내역 조회</a></li>
            <li><a href="club_reports.php?action=submit">20. 동아리 활동 보고서 등록</a></li>
            <li><a href="club_reports.php?action=list">21. 동아리 활동 보고서 목록 조회</a></li>
            <li><a href="alumni.php?action=register">22. 동문 정보 등록</a></li>
            <li><a href="alumni.php?action=list">23. 동문 목록 조회</a></li>
           <li><a href="club_fees.php?action=pay">24. 동아리 회비 납부</a></li>
            <li><a href="club_fees.php?action=view">25. 동아리별 회비 납부 현황 조회</a></li>
        </ul>
    </div>
</body>
</html>