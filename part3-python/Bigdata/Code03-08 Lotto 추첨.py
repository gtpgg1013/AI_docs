import random
## 전역 변수 선언 ##
num = 0
lotto = []
## 메인 코드부 ##
if __name__ == '__main__':
    while True :
        num = random.randint(1, 45)
        if num in lotto :
            pass
        else :
            lotto.append(num)
        if len(lotto) >= 6 :
            break
    lotto.sort()
    print('추카추카-->', lotto)

