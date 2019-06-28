import pymysql

# DB 접속 정보
IP = '192.168.56.107'; USER='root'; PASS='1234'; DB='review_db'; PORT='3306'
try :
    conn = pymysql.connect(host=IP, user=USER, password=PASS,
                       db=DB, charset="utf8")  # 1. DB 연결
except :
    print('DB 연결 실패')
    exit()

cur = conn.cursor()
sql = "INSERT INTO emp_tbl(emp_id, emp_name, emp_pay)"
sql += " VALUES ( 10002, N'이순신', 5000 )"
try :
    cur.execute(sql)
except :
    print('입력 실패~~ 확인요망..')

conn.commit()
cur.close()
conn.close()
