import mysql.connector

config = {
    'user': 'leeminki',
    'password': '3051',
    'host': '192.168.56.101',
    'database': 'club_management',
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL 연결 오류: {err}")
        return None

def display_menu():
    print("-" * 40)
    print("1. 동아리 목록 조회")
    print("2. 동아리 검색")
    print("3. 동아리 등록")
    print("4. 학생 목록 조회")
    print("5. 학생 가입")
    print("6. 동아리 가입 신청")
    print("7. 동아리 가입 승인")
    print("8. 동아리 임원 목록 조회")
    print("9. 동아리 탈퇴")
    print("10. 동아리 임원 임명")
    print("11. 공지사항 등록")
    print("12. 동아리 활동 일정 등록")
    print("13. 동아리 활동 일정 조회")
    print("14. 물품 신청")
    print("15. 물품 신청 목록 조회")
    print("16. 물품 신청 승인/거절")
    print("17. 동아리 예산 등록")
    print("18. 동아리 지출 내역 등록")
    print("19. 동아리 예산 및 지출 내역 조회")
    print("20. 동아리 활동 보고서 등록")
    print("21. 동아리 활동 보고서 목록 조회")
    print("22. 동문 정보 등록")
    print("23. 동문 목록 조회")
    print("24. 동아리 회비 납부")
    print("25. 동아리별 회비 납부 현황 조회")
    print("00. 종료")
    print("-" * 40)

#1 동아리 목록 조회
def get_all_clubs():
    db = connect_to_database()
    if db is None:
        return

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM 동아리")
    clubs = cursor.fetchall()
    cursor.close()
    db.close()

    if clubs:
        print("동아리 목록:")
        for club in clubs:
            print(f"  ID: {club['id']}, 이름: {club['이름']}, 설립일: {club['설립일']}, 소개: {club['소개']}, 활동분야: {club['활동분야']}")
    else:
        print("등록된 동아리가 없습니다.")
#2 동아리 검색 
def find_club():
    db = connect_to_database()
    if db is None:
        return

    club_name = input("검색할 동아리 이름을 입력하세요: ")
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM 동아리 WHERE 이름 LIKE %s", (f"%{club_name}%",))
    clubs = cursor.fetchall()
    cursor.close()
    db.close()

    if clubs:
        print("검색 결과:")
        for club in clubs:
            print(f"  ID: {club['id']}, 이름: {club['이름']}, 설립일: {club['설립일']}, 소개: {club['소개']}, 활동분야: {club['활동분야']}")
    else:
        print("검색된 동아리가 없습니다.")

# 3. 동아리 등록 
def insert_club():
    db = connect_to_database()
    if db is None:
        return

    name = input("동아리 이름을 입력하세요: ")
    establishment_date = input("설립일을 입력하세요 (YYYY-MM-DD): ")
    introduction = input("소개를 입력하세요: ")
    field = input("활동분야를 입력하세요: ")
    logo = input("로고 파일 경로를 입력하세요: ")

    cursor = db.cursor()
    sql = "INSERT INTO 동아리 (이름, 설립일, 소개, 활동분야, 로고) VALUES (%s, %s, %s, %s, %s)"
    values = (name, establishment_date, introduction, field, logo)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("동아리가 성공적으로 등록되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 4. 학생 조회
def get_all_students():
    db = connect_to_database()
    if db is None:
        return

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM 학생")
    students = cursor.fetchall()
    cursor.close()
    db.close()

    if students:
        print("학생 목록:")
        for student in students:
            print(
                f"  학번: {student['학번']}, 이름: {student['이름']}, 학과: {student['학과']}, 이메일: {student['이메일']}, 연락처: {student['연락처']}"
            )
    else:
        print("등록된 학생이 없습니다.")

# 5. 학생 가입
def register_student():
    db = connect_to_database()
    if db is None:
        return

    student_id = input("학번을 입력하세요: ")
    name = input("이름을 입력하세요: ")
    department = input("학과를 입력하세요: ")
    email = input("이메일을 입력하세요: ")
    contact = input("연락처를 입력하세요: ")
    password = input("비밀번호를 입력하세요: ")

    cursor = db.cursor()
    sql = "INSERT INTO 학생 (학번, 이름, 학과, 이메일, 연락처, 비밀번호) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (student_id, name, department, email, contact, password)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("학생 가입이 성공적으로 완료되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()
    
# 6. 동아리 가입 신청
def apply_for_club():
    db = connect_to_database()
    if db is None:
        return

    student_id = input("학번을 입력하세요: ")
    club_id = input("가입 신청할 동아리 ID를 입력하세요: ")

    cursor = db.cursor()
    sql = "INSERT INTO 동아리가입신청 (동아리_id, 학생_id, 신청일, 상태) VALUES (%s, %s, CURDATE(), '대기')"
    values = (club_id, student_id)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("동아리 가입 신청이 완료되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 7. 동아리 가입 승인 기능
def approve_club_application():
    db = connect_to_database()
    if db is None:
        return

    application_id = input("승인할 가입 신청 ID를 입력하세요: ")

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM 동아리가입신청 WHERE id = %s", (application_id,))
    application = cursor.fetchone()

    if application is None:
        print("해당 가입 신청 ID가 존재하지 않습니다.")
        cursor.close()
        db.close()
        return

    if application["상태"] != "대기":
        print("이미 처리된 가입 신청입니다.")
        cursor.close()
        db.close()
        return

    insert_sql = "INSERT INTO 동아리회원 (동아리_id, 학생_id, 가입일) VALUES (%s, %s, CURDATE())"
    insert_values = (application["동아리_id"], application["학생_id"])

    update_sql = "UPDATE 동아리가입신청 SET 상태 = '승인' WHERE id = %s"
    update_values = (application_id,)

    try:
        cursor.execute(insert_sql, insert_values)
        cursor.execute(update_sql, update_values)
        db.commit()
        print("동아리 가입 신청이 승인되었습니다.")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

    cursor.close()
    db.close()
# 8. 동아리 임원 목록 조회 기능
def get_club_officers():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("임원 목록을 조회할 동아리 ID를 입력하세요: ")

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT o.역할, s.이름, s.학번, s.이메일, s.연락처 FROM 동아리임원 o JOIN 학생 s ON o.학생_id = s.학번 WHERE o.동아리_id = %s",
        (club_id,),
    )
    officers = cursor.fetchall()
    cursor.close()
    db.close()

    if officers:
        print(f"{club_id}번 동아리 임원 목록:")
        for officer in officers:
            print(
                f"  역할: {officer['역할']}, 이름: {officer['이름']}, 학번: {officer['학번']}, 이메일: {officer['이메일']}, 연락처: {officer['연락처']}"
            )
    else:
        print("해당 동아리의 임원 정보가 없습니다.")
# 9. 동아리 탈퇴 기능
def withdraw_from_club():
    db = connect_to_database()
    if db is None:
        return

    student_id = input("학번을 입력하세요: ")
    club_id = input("탈퇴할 동아리 ID를 입력하세요: ")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM 동아리회원 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    membership = cursor.fetchone()

    if membership is None:
        print("해당 동아리의 회원이 아닙니다.")
        cursor.close()
        db.close()
        return
    
    delete_sql = "DELETE FROM 동아리회원 WHERE 동아리_id = %s AND 학생_id = %s"
    delete_values = (club_id, student_id)

    try:
        cursor.execute(delete_sql, delete_values)
        db.commit()
        print("동아리에서 탈퇴 처리되었습니다.")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 10. 동아리 임원 임명
def assign_officer():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("임원을 임명할 동아리 ID를 입력하세요: ")
    student_id = input("임명할 학생의 학번을 입력하세요: ")
    role = input("부여할 역할을 입력하세요 (예: 회장, 부회장, 총무 등): ")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM 동아리회원 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    membership = cursor.fetchone()

    if membership is None:
        print("해당 학생은 동아리 회원이 아닙니다.")
        cursor.close()
        db.close()
        return

    cursor.execute("SELECT * FROM 동아리임원 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    existing_officer = cursor.fetchone()

    if existing_officer:
        print("해당 학생은 이미 임원입니다.")
        cursor.close()
        db.close()
        return

    insert_sql = "INSERT INTO 동아리임원 (동아리_id, 학생_id, 역할) VALUES (%s, %s, %s)"
    insert_values = (club_id, student_id, role)

    try:
        cursor.execute(insert_sql, insert_values)
        db.commit()
        print(f"{student_id} 학생을 {club_id} 동아리의 {role}으로 임명했습니다.")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

    cursor.close()
    db.close()
# 11. 공지사항 기능
def insert_club_notice():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("게시물을 등록할 동아리 ID를 입력하세요: ")
    title = input("제목을 입력하세요: ")
    content = input("내용을 입력하세요: ")

    cursor = db.cursor()
    sql = "INSERT INTO 동아리게시판 (동아리_id, 게시물제목, 게시물내용, 게시일, 게시물유형) VALUES (%s, %s, %s, CURDATE(), '공지사항')"
    values = (club_id, title, content)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("게시물이 성공적으로 등록되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 12. 동아리 활동 일정 등록
def insert_club_schedule():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("활동 일정을 등록할 동아리 ID를 입력하세요: ")
    title = input("제목을 입력하세요: ")
    description = input("설명을 입력하세요: ")
    date = input("일정일을 입력하세요 (YYYY-MM-DD): ")
    location = input("장소를 입력하세요: ")

    cursor = db.cursor()
    sql = "INSERT INTO 동아리활동일정 (동아리_id, 제목, 설명, 일정일, 장소) VALUES (%s, %s, %s, %s, %s)"
    values = (club_id, title, description, date, location)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("활동 일정이 성공적으로 등록되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 13. 동아리 활동 일정 조회 기능
def get_club_schedule():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("활동 일정을 조회할 동아리 ID를 입력하세요: ")

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, 제목, 설명, 일정일, 장소 FROM 동아리활동일정 WHERE 동아리_id = %s ORDER BY 일정일",
        (club_id,),
    )
    schedules = cursor.fetchall()
    cursor.close()
    db.close()

    if schedules:
        print(f"{club_id}번 동아리 활동 일정:")
        for schedule in schedules:
            print(
                f"  ID: {schedule['id']}, 제목: {schedule['제목']}, 설명: {schedule['설명']}, 일정일: {schedule['일정일']}, 장소: {schedule['장소']}"
            )
    else:
        print("해당 동아리의 활동 일정이 없습니다.")


# 14. 물품 신청 기능
def request_item():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("물품을 신청할 동아리 ID를 입력하세요: ")
    item_name = input("물품명을 입력하세요: ")
    quantity = int(input("수량을 입력하세요: "))
    applicant_id = input("신청자의 학번을 입력하세요: ")
    purpose = input("용도를 입력하세요: ")

    cursor = db.cursor()
    sql = "INSERT INTO 물품신청 (동아리_id, 물품명, 수량, 신청일, 상태, 신청자_id, 용도) VALUES (%s, %s, %s, CURDATE(), '대기', %s, %s)"
    values = (club_id, item_name, quantity, applicant_id, purpose)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("물품 신청이 완료되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 15. 물품 신청 목록 조회
def list_item_requests():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("물품 신청 목록을 조회할 동아리 ID를 입력하세요(전체는 'all'): ")

    cursor = db.cursor(dictionary=True)
    if club_id.lower() == 'all':
        cursor.execute("SELECT * FROM 물품신청")
    else:
        cursor.execute("SELECT * FROM 물품신청 WHERE 동아리_id = %s", (club_id,))
    requests = cursor.fetchall()

    if requests:
        print("물품 신청 목록:")
        for req in requests:
            print(
                f"ID: {req['id']}, 동아리ID: {req['동아리_id']}, 물품명: {req['물품명']}, 수량: {req['수량']}, 신청일: {req['신청일']}, 상태: {req['상태']}, 신청자: {req['신청자_id']}, 용도: {req['용도']}"
            )
    else:
        print("신청된 물품이 없습니다.")

    cursor.close()
    db.close()

# 16. 물품 신청 승인/거절
def process_item_request():
    db = connect_to_database()
    if db is None:
        return

    request_id = int(input("처리할 물품 신청 ID를 입력하세요: "))
    action = input("승인/거절 중 하나를 입력하세요 (승인/거절): ")

    if action.lower() not in ["승인", "거절"]:
        print("잘못된 입력입니다.")
        return

    cursor = db.cursor()
    sql = "UPDATE 물품신청 SET 상태 = %s WHERE id = %s"
    values = (action, request_id)

    try:
        cursor.execute(sql, values)
        db.commit()
        print(f"물품 신청 ID {request_id}이(가) {action} 처리되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()
# 17. 동아리 예산 등록
def register_club_budget():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("예산을 등록할 동아리 ID를 입력하세요: ")
    year = int(input("연도를 입력하세요 (YYYY): "))
    budget_plan = float(input("예산 계획을 입력하세요: "))

    cursor = db.cursor()
    
    check_sql = "SELECT * FROM 동아리예산 WHERE 동아리_id = %s AND 연도 = %s"
    cursor.execute(check_sql, (club_id, year))
    existing_budget = cursor.fetchone()

    if existing_budget:
        print("해당 연도의 예산이 이미 등록되어 있습니다.")
        cursor.close()
        db.close()
        return

    sql = "INSERT INTO 동아리예산 (동아리_id, 연도, 예산계획) VALUES (%s, %s, %s)"
    values = (club_id, year, budget_plan)

    try:
        cursor.execute(sql, values)
        db.commit()
        print(f"{year}년도 동아리 예산이 등록되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 18. 동아리 지출 내역 등록
def register_club_expense():
    db = connect_to_database()
    if db is None:
        return

    budget_id = int(input("지출 내역을 등록할 예산 ID를 입력하세요: "))
    expense_date = input("지출일을 입력하세요 (YYYY-MM-DD): ")
    expense_item = input("지출 항목을 입력하세요: ")
    amount = float(input("금액을 입력하세요: "))
    note = input("비고를 입력하세요: ")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM 동아리예산 WHERE id = %s", (budget_id,))
    budget = cursor.fetchone()

    if budget is None:
        print("해당 예산 ID가 존재하지 않습니다.")
        cursor.close()
        db.close()
        return

    insert_sql = "INSERT INTO 동아리예산지출내역 (예산_id, 지출일, 지출항목, 금액, 비고) VALUES (%s, %s, %s, %s, %s)"
    insert_values = (budget_id, expense_date, expense_item, amount, note)

    update_sql = "UPDATE 동아리예산 SET 지출합계 = 지출합계 + %s, 잔액 = 예산계획 - 지출합계 WHERE id = %s"
    update_values = (amount, budget_id)

    try:
        cursor.execute(insert_sql, insert_values)
        cursor.execute(update_sql, update_values)
        db.commit()
        print("지출 내역이 등록되었습니다.")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 19. 동아리 예산 및 지출 내역 조회
def view_club_budget():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("예산 및 지출 내역을 조회할 동아리 ID를 입력하세요: ")
    year = int(input("연도를 입력하세요 (YYYY): "))

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM 동아리예산 WHERE 동아리_id = %s AND 연도 = %s", (club_id, year))
    budget = cursor.fetchone()

    if budget is None:
        print(f"{year}년도에 해당하는 동아리 예산이 없습니다.")
        cursor.close()
        db.close()
        return
    
    budget_id = budget["id"]
    print(f"\n{year}년도 동아리 예산:")
    print(f"  예산 ID: {budget_id}, 예산 계획: {budget['예산계획']}, 지출 합계: {budget['지출합계']}, 잔액: {budget['잔액']}")

    cursor.execute("SELECT * FROM 동아리예산지출내역 WHERE 예산_id = %s", (budget_id,))
    expenses = cursor.fetchall()

    print(f"\n{year}년도 지출 내역:")
    if expenses:
        for expense in expenses:
            print(
                f"  ID: {expense['id']}, 지출일: {expense['지출일']}, 지출 항목: {expense['지출항목']}, 금액: {expense['금액']}, 비고: {expense['비고']}"
            )
    else:
        print("  지출 내역이 없습니다.")

    cursor.close()
    db.close()

# 20. 동아리 활동 보고서 등록
def submit_club_report():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("활동 보고서를 등록할 동아리 ID를 입력하세요: ")
    title = input("보고서 제목을 입력하세요: ")
    content = input("내용을 입력하세요: ")
    author_id = input("작성자 학번을 입력하세요: ")

    cursor = db.cursor()
    sql = "INSERT INTO 동아리활동보고서 (동아리_id, 보고서제목, 내용, 제출일, 작성자_id) VALUES (%s, %s, %s, CURDATE(), %s)"
    values = (club_id, title, content, author_id)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("활동 보고서가 등록되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 21. 동아리 활동 보고서 목록 조회
def list_club_reports():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("활동 보고서 목록을 조회할 동아리 ID를 입력하세요: ")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM 동아리활동보고서 WHERE 동아리_id = %s", (club_id,))
    reports = cursor.fetchall()

    if reports:
        print("동아리 활동 보고서 목록:")
        for report in reports:
            print(
                f"ID: {report['id']}, 제목: {report['보고서제목']}, 제출일: {report['제출일']}, 작성자: {report['작성자_id']}"
            )
            print(f"내용: {report['내용']}\n")
    else:
        print("등록된 활동 보고서가 없습니다.")

    cursor.close()
    db.close()

# 22. 동문 정보 등록
def register_alumni():
    db = connect_to_database()
    if db is None:
        return

    student_id = input("동문으로 등록할 학생의 학번을 입력하세요: ")
    graduation_year = int(input("졸업 연도를 입력하세요: "))
    current_job = input("현재 직업을 입력하세요: ")
    contact = input("연락처를 입력하세요: ")
    email = input("이메일을 입력하세요: ")
    
    cursor = db.cursor()

    cursor.execute("SELECT * FROM 학생 WHERE 학번 = %s", (student_id,))
    student = cursor.fetchone()
    
    if student is None:
        print("해당 학번의 학생 정보가 없습니다.")
        cursor.close()
        db.close()
        return

    cursor.execute("SELECT * FROM 동문 WHERE 학생_id = %s", (student_id,))
    existing_alumni = cursor.fetchone()

    if existing_alumni:
        print("해당 학생의 동문 정보가 이미 등록되어 있습니다.")
        cursor.close()
        db.close()
        return

    sql = "INSERT INTO 동문 (학생_id, 졸업년도, 현재직업, 연락처, 이메일) VALUES (%s, %s, %s, %s, %s)"
    values = (student_id, graduation_year, current_job, contact, email)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("동문 정보가 등록되었습니다.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    db.close()

# 23. 동문 목록 조회
def list_alumni():
    db = connect_to_database()
    if db is None:
        return

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM 동문")
    alumni_list = cursor.fetchall()

    if alumni_list:
        print("동문 목록:")
        for alumni in alumni_list:
            print(
                f"ID: {alumni['id']}, 학번: {alumni['학생_id']}, 졸업년도: {alumni['졸업년도']}, 현재직업: {alumni['현재직업']}, 연락처: {alumni['연락처']}, 이메일: {alumni['이메일']}"
            )
    else:
        print("등록된 동문이 없습니다.")

    cursor.close()
    db.close()
#24 동아리 회비 납부 기능
def pay_club_membership_fee():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("회비를 납부할 동아리 ID를 입력하세요: ")
    student_id = input("납부하는 학생의 학번을 입력하세요: ")
    amount = float(input("납부할 금액을 입력하세요: "))

    cursor = db.cursor()

    cursor.execute("SELECT * FROM 동아리회원 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    membership = cursor.fetchone()

    if membership is None:
        print("해당 학생은 동아리 회원이 아닙니다.")
        cursor.close()
        db.close()
        return

    cursor.execute("SELECT * FROM 동아리회비 WHERE 동아리_id = %s AND 학생_id = %s AND 납부여부 = 'Y'", (club_id, student_id))
    existing_payment = cursor.fetchone()

    if existing_payment:
        print("해당 학생은 이미 회비를 납부했습니다.")
        cursor.close()
        db.close()
        return
    
    cursor.execute("SELECT * FROM 동아리회비 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    existing_record = cursor.fetchone()

    if existing_record:
        update_sql = "UPDATE 동아리회비 SET 납부금액 = %s, 납부일 = CURDATE(), 납부여부 = 'Y' WHERE id = %s"
        update_values = (amount, existing_record['id'])
        try:
            cursor.execute(update_sql, update_values)
            db.commit()
            print("회비 납부 정보가 업데이트되었습니다.")
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
    else:
        insert_sql = "INSERT INTO 동아리회비 (동아리_id, 학생_id, 납부금액, 납부일, 납부여부) VALUES (%s, %s, %s, CURDATE(), 'Y')"
        insert_values = (club_id, student_id, amount)
        try:
            cursor.execute(insert_sql, insert_values)
            db.commit()
            print("회비 납부 정보가 등록되었습니다.")
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")

    cursor.close()
    db.close()
#25 동아리별 회비 납부 현황 조회 기능
def view_club_membership_fee():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("회비 납부 현황을 조회할 동아리 ID를 입력하세요: ")

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
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
        WHERE m.동아리_id = %s
    """, (club_id,))
    members = cursor.fetchall()

    if members:
        print(f"{club_id}번 동아리 회비 납부 현황:")
        print("-" * 60)
        print(f"{'학번':<10} {'이름':<8} {'학과':<10} {'납부금액':<8} {'납부일':<12} {'납부여부':<6}")
        print("-" * 60)
        for member in members:
            print(
                f"{member['학생_id']:<10} {member['이름']:<8} {member['학과']:<10} {member['납부금액']:<8.2f} {str(member['납부일'] if member['납부일'] else ''):<12} {member['납부여부']:<6}"
            )
        print("-" * 60)
    else:
        print("해당 동아리의 회원이 없거나 회비 정보가 없습니다.")

    cursor.close()
    db.close()
# 메인 함수
def main():
    while True:
        display_menu()
        choice = input("메뉴를 선택하세요: ")

        if choice == "1":
            get_all_clubs()
        elif choice == "2":
            find_club()
        elif choice == "3":
            insert_club()
        elif choice == "4":
            get_all_students()
        elif choice == "5":
            register_student()
        elif choice == "6":
            apply_for_club()
        elif choice == "7":
            approve_club_application()
        elif choice == "8":
            get_club_officers()
        elif choice == "9":
            withdraw_from_club()
        elif choice == "10":
            assign_officer()  
        elif choice == "11":
            insert_club_notice()
        elif choice == "12":
            insert_club_schedule()
        elif choice == "13":
            get_club_schedule()
        elif choice == "14":
            request_item()
        elif choice == "15":
            list_item_requests()
        elif choice == "16":
            process_item_request()
        elif choice == "17":
            register_club_budget()
        elif choice == "18":
            register_club_expense()
        elif choice == "19":
            view_club_budget()
        elif choice == "20":
            submit_club_report()
        elif choice == "21":
            list_club_reports()
        elif choice == "22":
            register_alumni()
        elif choice == "23":
            list_alumni()
        elif choice == "24":
            pay_club_membership_fee()
        elif choice == "25":
            view_club_membership_fee()
        elif choice == "00":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 메뉴 선택입니다. 다시 선택하세요.")

if __name__ == "__main__":
    main()