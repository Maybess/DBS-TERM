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
    print("12. 동아리 활동 일정")  
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

    # 가입 신청 정보 조회
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

    # 동아리 회원으로 추가
    insert_sql = "INSERT INTO 동아리회원 (동아리_id, 학생_id, 가입일) VALUES (%s, %s, CURDATE())"
    insert_values = (application["동아리_id"], application["학생_id"])

    # 가입 신청 상태 업데이트
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

    # 동아리 회원 여부 확인
    cursor.execute("SELECT * FROM 동아리회원 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    membership = cursor.fetchone()

    if membership is None:
        print("해당 동아리의 회원이 아닙니다.")
        cursor.close()
        db.close()
        return

    # 동아리 회원에서 삭제
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

    # 동아리 회원인지 확인
    cursor.execute("SELECT * FROM 동아리회원 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    membership = cursor.fetchone()

    if membership is None:
        print("해당 학생은 동아리 회원이 아닙니다.")
        cursor.close()
        db.close()
        return

    # 이미 임원인지 확인
    cursor.execute("SELECT * FROM 동아리임원 WHERE 동아리_id = %s AND 학생_id = %s", (club_id, student_id))
    existing_officer = cursor.fetchone()

    if existing_officer:
        print("해당 학생은 이미 임원입니다.")
        cursor.close()
        db.close()
        return

    # 동아리 임원으로 추가
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
# 12. 동아리 활동 일정 조회 기능
def get_club_schedule():
    db = connect_to_database()
    if db is None:
        return

    club_id = input("활동 일정을 조회할 동아리 ID를 입력하세요: ")

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT 제목, 설명, 일정일, 장소 FROM 동아리활동일정 WHERE 동아리_id = %s",
        (club_id,),
    )
    schedules = cursor.fetchall()
    cursor.close()
    db.close()

    if schedules:
        print(f"{club_id}번 동아리 활동 일정:")
        for schedule in schedules:
            print(
                f"  제목: {schedule['제목']}, 설명: {schedule['설명']}, 일정일: {schedule['일정일']}, 장소: {schedule['장소']}"
            )
    else:
        print("해당 동아리의 활동 일정이 없습니다.")

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
            get_club_schedule()
        elif choice == "00":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 메뉴 선택입니다. 다시 선택하세요.")

if __name__ == "__main__":
    main()