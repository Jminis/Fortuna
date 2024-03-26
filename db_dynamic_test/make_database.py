import mysql.connector
import os
from mysql.connector import Error

# 데이터베이스 연결 정보
host = 'localhost'  # 데이터베이스 호스트
user = 'root'  # 데이터베이스 사용자 이름
password = '1234'  # 사용자 비밀번호

# 생성할 데이터베이스 이름
database_name = 'test'

# 환경 변수 'fortuna_database'의 값을 가져옴
database_name = os.getenv('fortuna_database')

# 환경 변수 값이 제대로 설정되었는지 확인
if database_name is None:
    print("The 'fortuna_database' environment variable is not set.")
else:
    print(f"The database name is: `{database_name}`")

try:
    # MySQL 데이터베이스 서버에 연결
    conn = mysql.connector.connect(host=host, user=user, password=password)
    
    # 커서 생성
    cursor = conn.cursor()
    
    # 데이터베이스 존재 여부 확인
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    
    if database_name not in databases:
        # 데이터베이스가 존재하지 않으면 생성
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' created successfully.")
    else:
        print(f"Database '{database_name}' already exists.")
    
    # 연결 닫기
    cursor.close()
    conn.close()
except Error as e:
    print(f"Error creating database: {e}")

