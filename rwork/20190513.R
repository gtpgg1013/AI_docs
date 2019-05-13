# R script Area
print("안녕녕")
#print{base}
#함수명{패키지명}

#r로 데이터를 불러와서 분석
#하드에 패키지 설치완료
install.packages("randomForest")

#패키지 메모리에 적재(부착)
library("randomForest")

#변수: 변할 수 있는 것 : 데이터가 저장되는 장소
a<-3
b<-2
#상수: 변할 수 없는 것

#스칼라: 0차원, 1,2,3..., 길이가 1인 데이터
#벡터: 1차원, 길이가 1 이상인 데이터 집합
#r에서는 벡터 단위로 처리
x<-1
print(x)
x2<-1.5
x3<-x+x2
x3
#NA : 상수 (값이 없음을 나타냄)
#NA와 0은 다름름!
NA

one<-70
two<-80
three<-90
four<-NA
five<-four+one

print(one+two)
print(one+four)
#NA와의 연산은 NA가 나오기 때문에 전처리 잘 해줘야 함!
is.na(five)
#na인지 확인하는 함수

#NULL : 변수가 초기화되지 않은 상태
#NULL : 빈 바구니 / NA : 바구니 조차도 없다

iseven<-NULL
iseven
#if 조건만족 : iseven true / 불만족 : false 이런식으로 씀
is.null(iseven)

a<-"hi"
a2<-'hellow'
#문자사용시 두개 따옴표 다 가능

# &연산자 AND / |연산자 OR / !연산자 NOT

#factor 자료형 : 범주형(카테고리, 데이터가 사전에 정해진 유형으로만 분류가 되는 경우)
#범주형 : 명목형, 순서형으로 나눌 수 있음
#수치형 : factor(범주형)의 반대 : 점수, 온도

#명목형 : 데이터간 크기 비교가 불가능 (좌파/우파 : 정치성향)
#순서형 : 소,중,대(크기 비교가 가능하다)

sex<-factor("f",c("m","f"))
sex<-m
sex
is.ordered(sex)

score<-factor(1,c(1,2))
score
is.ordered(score)

#c : combine 시켜주는 함수 : list / vector로로