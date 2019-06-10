def func1():
    global a # 글로벌 a 써주면 이제 a는 지역변수가 아니라 전역임을 알림
    a = 10
    print('func1()-->', a)

def func2():
    global a # 얘도 글로벌임을 알림! : 글로벌 변수면 함수 위에 다 써줘라 : 보통 지역 / 전역변수는 이름 규칙이 다름! : gName 등
    print('func1()-->', a)

#변수 선언부
a=1234

##메인 코드부
func1()
print(a)
func2()