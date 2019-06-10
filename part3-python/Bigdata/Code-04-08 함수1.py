## 두 수를 받아서 더한 값을 반환하는 함수
def plus(v1, v2):
    ans = 0
    ans = v1 + v2
    return ans

def calc(v1, v2, v3 = 0):
    ans1 = v1 + v2 + v3
    ans2 = v1 - v2 - v3
    return ans1, ans2

def calc2(*para) : # *는 파라미터가 몇개인지 모를 때 씀
    res = 0
    for num in para:
        res += num
    return res

## 메인 코드부
if __name__ == "__main__":
    print(plus(3,4))
    hap = calc(100,200,300)
    hap1, hap2 = calc(100,200) # return 값이 두개인 함수 : 이런식으로 많이 쓴다
    print(hap[0], hap[1])
    print(hap1, hap2)

hap = calc2(12,3,4,12,412,412)
print(hap)

