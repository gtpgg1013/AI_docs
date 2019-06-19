import pymysql

# DB config
IP_ADDR = '192.168.56.101'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'quiz_db'; CHAR_SET = 'utf8'

con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
cur = con.cursor()

sql = "CREATE TABLE IF NOT EXISTS quiz_tbl (" \
      " id INT AUTO_INCREMENT PRIMARY KEY," \
      " idNum VARCHAR(20)," \
      " email VARCHAR(20))"

cur.execute(sql)

idNum = "920920-2320222"
email = "gtpgg1013@naks.com"

sql = "INSERT INTO quiz_tbl (id, idNum, email) " \
      "VALUES (NULL, '" + idNum + "','" + email + "')"

cur.execute(sql)
con.commit()

sql = "select * from quiz_tbl"
cur.execute(sql)

rows = cur.fetchall()

for row in rows:
    print(row[0],":",row[1],":",row[2])
