import pymysql

# DB config
IP_ADDR = '192.168.56.101'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'review_DB'; CHAR_SET = 'utf8'

con = pymysql.connect(host=IP_ADDR,user=USER_NAME,password=USER_PASS,db=DB_NAME, charset=CHAR_SET)
cur = con.cursor()

sql = "select emp_id, emp_name, emp_pay from emp_tbl"
cur.execute(sql)

# rows = cur.fetchall()
# for row in rows:
#     print(row[0],row[1],row[2])

while True:
    row = cur.fetchone()
    if row is None:
        break
    print(row[0],row[1],row[2])

cur.close()
con.close()