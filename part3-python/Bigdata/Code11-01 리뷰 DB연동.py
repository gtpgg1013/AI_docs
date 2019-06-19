import pymysql

# DB config
IP_ADDR = '192.168.56.106'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'

con = pymysql.connect(host=IP,user=USER_NAME,password=USER_PASS,db=DB_NAME, charset=CHAR_SET)
cur = con.cursor()

sql = "INSERT INTO emp_tbl (emp_id, emp_name, emp_pay)"
sql += "VALUES ( 10002, N'깅기동', 5200)"

cur.execute(sql)

con.commit()
cur.close()
con.close()