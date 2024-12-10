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
    print("10. 공지사항 등록")  
    print("11. 동아리 활동 일정")  
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
# 4. 학생 목록 조회
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
        elif choice == "00":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 메뉴 선택입니다. 다시 선택하세요.")

if __name__ == "__main__":
    main()  