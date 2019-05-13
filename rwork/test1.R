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
NA
