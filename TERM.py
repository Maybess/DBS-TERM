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