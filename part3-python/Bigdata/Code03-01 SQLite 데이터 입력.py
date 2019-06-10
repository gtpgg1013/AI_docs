import sqlite3

conn = sqlite3.connect("samsongDB")  # 1. DB 연결 생성
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프) - 연결로 커서 생성
sql = "CREATE TABLE IF NOT EXISTS userTable(userId INT, userName CHAR(5))"
cur.execute(sql) #커서로 sql 쿼리 날리기

sql = "INSERT INTO userTable VALUES( 1 , '홍길동')";
cur.execute(sql)
sql = "INSERT INTO userTable VALUES( 2 , '이순신')";
cur.execute(sql)

cur.close() #커서 닫고
conn.commit() #커밋
conn.close() # 6. DB 닫기 (=연결 해제) # 연결 닫기
print('OK~')