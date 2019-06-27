import smtplib
from email.mime.text import MIMEText
from datetime import datetime

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('gangkkformailing@gmail.com', '')
msg = MIMEText('CPU 수치가 ' +" 몃분" + "을 초과한 지 " + "몃" + "초 되었습니다."
                                                                               "컴퓨터 사용량을 확이핸주세요.")

msg['Subject'] = "현재시각: " + str(datetime.now()) + "CPU 사용량 임계점 초과 경고 메일"
s.sendmail("gangkkformailing@gmail.com", "gtpgg1013@gmail.com", msg.as_string())
s.quit()