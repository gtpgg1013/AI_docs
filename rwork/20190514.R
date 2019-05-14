var1<-c(1,3,5,7,9) #백터 구성
var1+1 #각각각 값에 대해 1씩 더함 (벡터화연산)
var1
var2<-c(1:5) #연속된 숫자의 벡터 구성 / 동일 타입

var1+var2 #벡터화 연산(요소간 덧셈셈)

var2
var3<-seq(1,5) #연속된 숫자 만드는 함수수
var3
var4<-seq(1,5,by=3) #점프 크기도 설정 가능 seq함수는 1,5사이에서만 만듬
var4

str1<-"a"
str2<-"text"
str3<-"hello world"

c(str1,str2)
str4<-c(str1,str2,str3)
str4+2 #에러뜸 : 문자에 숫자 더하려고 하면 일케되긔 (이항연산자 사용불가)
str1+str2 #에러뜸 : 문자 + 문자 안됨(이항연산자 못씀)
c(str1,str2,str3,var3) #뭉치는건 상관 없음

x<-c(1,2,3)
x_mean<-mean(x) #평균
max(x) #최대
min(x)

str4
str5<-paste(str4,collapse=",") #하나의 단어로 합칠 때 사용 
(nth <- paste0(1:12, c("st", "nd", "rd", rep("th", 9))))
paste(month.abb, nth, sep = ": ", collapse = "; ") #두개 합칠때 같은 덩어리 사이에: sep

#패키지 사용법 : pakages.install -> library
install.packages("ggplot2") #시각화
library("ggplot2")

x<-c("a","a","b","c")
x
qplot(x) #빈도그래프 확인할때
mpg #데이터프레임 - 엑셀의 시트와 같은 것

#한 행의 데이터 : 관측치
#행을 구성하는 각각의 요소 하나하나 : 관측값

str(mpg) #구조를 확인하는 함수
qplot(mpg) #에러뜸 : 데이터 인풋 속성이 다르다
qplot(data = mpg,x = year) #속성 써주면 됨
qplot(data = mpg,x = drv,y = hwy) #x,y 속성 보여줄 수 있다
#EDA : 탐색적 분석 방법 : 데이터를 보면서 분석해나간다
qplot(data = mpg,x = drv,y = hwy,geom = "line")
qplot(data = mpg,x = drv,y = hwy,geom = "boxplot")
#통계의 이상치를 파악할 때 쉽게 파악할 수 있게 하는 그래프 : boxplot
#25%씩 나눠짐 : IQR = Q3-Q1 / IQR*1.5만큼 박스에서 벗어나면 outlier다
#박스 플롯을 봤을 때 점 찍혀있는애들 : outlier
#이상치 : outliner
qplot(data = mpg,x = drv,y = hwy,geom = "boxplot",colour = drv) # 색상

qplot(mpg$trans) # $는 컬럼참조

#1. 3명 점수 (80,90,50)을 저장 : 변수 3개로
sa<-80
sb<-90
sc<-50
scores<-c(sa,sb,sc)
scores
#2. 평균점수 출력
min(scores)
mean(scores)

#데이터프레임 : 엑셀의 시트(행(관측치): 한사람의 정보 / 열: 속성)
eng<-c(90,100,70,60)
math<-c(50,60,100,9)
class(eng) #python type 함수
#stringAsFactors : 문자를 팩터(카테고리)로 읽을 거니?

df<-data.frame(eng) #eng 벡터, 열이 1개인 표 만듬
df
class(df)

df2<-data.frame(eng,math) #eng 벡터, 열이 1개인 표 만듬
df2
class(df2)
str(df2)

#1,2,3,4,5 는 행 index (row)
#eng, math는 열 index (col)

class<-c(1,1,2,3)
df3<-data.frame(eng,math,class)
df3

#eng의 평균출력
mean(df3$eng)

df4<-data.frame(eng=c(90,100,70,60),
math=c(50,60,100,9),
class=c(1,1,2,3)) #<-연산자 사용하면 안됨
df4

#과일 df만들기
fruits<-data.frame(가격=c(1000,2000,500),
                     판매수량=c(20,10,5),
                     row.names=c("포도","사과","배"))

fruits
mean(fruits$가격)
mean(fruits$판매수량)

#cafe.naver.com/ai4you
#Data의 내용들 중 xlsx 읽으려면
install.packages("readxl")
library(readxl)

df<-read_excel("Data/excel_exam.xlsx")
mean(df$science)
df<-data.frame(df,row.names = c(2:21))

df2<-read_excel("Data/excel_exam_novar.xlsx",col_names = FALSE) #f1누르면 도움말 / false주면 default로 줌
df2

df3<-read_excel("Data/excel_exam_sheet.xlsx",sheet=3) #3번째 sheet에서 가져와야 함
df3

df4<-read.csv("Data/csv_exam.csv") 
#table형식의 file을 dataframe으로 바꿔주는 것 / sep 옵션으로 구분자 선택 가능
df4
str(df4)

df5<-data.frame(a=c(1,2,3),
                b=c(1,2,3),
                c=c(1,2,3),
                row.names = c("강낭콩","완두콩","팥"))
df5

write.csv(df5,file = "mydf.csv")

#파일 용량 작고 빠르게
save(df5,file = "mydf_s.rda")
rm(df5)

df5

load("mydf_s.rda")

df5

exam<-read.csv("Data/csv_exam.csv")
exam
str(exam)

head(exam,10)
tail(exam)

View(exam) #새 창 띄워서 내용 보여주기
dim(exam) #row col 수 확인

summary(exam) #기술통계 보여주는 명령어

mpg
str(mpg)
class(mpg)
head(mpg)

mpg<-as.data.frame(mpg) #일케하면 tbl, tbl_df 아닌 진짜 data.frame의 속성만 가짐
str(mpg)
View(mpg)
dim(mpg)
summary(mpg)

#데이터 변경
df<-data.frame(var1=c(1,2,1),
           var2=c(1,2,3))
df
df_new<-df #데이터프레임 복사
library(plyr)
rename(df_new, replace=c("var2"="v2")) #이름변경 var2->v2로

install.packages("dplyr")
library("dplyr")
df_new<-rename(df_new,v1=var1) #이름변경 var1->v1으로
df_new<-rename(df_new,v2=var2)
df_new

#변수 (features)
#dataset에서 제공되는 데이터를 가공해 새로운 feature를 만들 수 있다 (빈번)
#파생변수라고 부름

mydf<-data.frame(eng=c(70,80,90),
                 mat=c(50,60,70))
mydf$sum<-mydf$eng+mydf$mat #새로운 컬럼 추가
mydf$mymean<-mydf$sum/2
mydf

mpg
mpg$tot<-(mpg$cty+mpg$hwy)/2
mpg$tot

head(mpg)
mean(mpg$tot) #tot col의 평균
summary(mpg$tot) #숫자로 보긴 조금 힘들구만
#히스토그램
hist(mpg$tot)
boxplot(mpg$tot)

#삼항연산
#평균연비(tot)가 23이상이면->gr_h, 미만이면 gr_l라고 쓰고싶음
#ifelse함수 : 조건식, 참, 거짓
mpg$yesOrNo<-ifelse(mpg$tot>=23,"gr_h","gr_l")
mpg<-rename(mpg,test=yesOrNo)
mpg

#table 함수
table(mpg$test) #빈도표
#뭐가 얼마만큼 나왔는지 확인 가능

#qplot이용 그래프 시각화
qplot(mpg$test)

#tot
#28이상 -> grade:A
#20이상 28미만 -> grade:B
#나머지 -> grade:C
#범주 만들기는 ifelse()함수를 중첩해서 사용하면 됨
mpg$grade<-ifelse(mpg$tot>=28,"A",
                  ifelse(mpg$tot>=20,"B","C"))

table(mpg$grade) #빈도확인
qplot(mpg$grade)

#cancer data 분류기 : 공부에 좋다(질병분류기)

exam<-read.csv("Data/csv_exam.csv")
exam
#3반만 출력하고 싶다
#filter기능 : 원하는 자료만 추출
#ctrl+shift+m : filter(pipe) 기호 : 앞에 것 중에서 걸러내라
exam %>% filter(class==3)
#exam에 있는 것 중에서 class가 3인것만 걸러내라

exam %>% filter(class!=3)
#아닌것만 골라내라

#3반이 아니면서 sci 50점 이상
exam %>% filter(class!=3 & science>=50)
#math가 70점 이상|eng가 90점 이상
exam %>% filter(math>=70|english>=90)

#class 1,4,5만 추출하고 싶음 : %in% + c() 써주자
exam %>% filter(class %in% c(1,4,5))

class3<-exam %>% filter(class==3)
class3
mean(class3$english)

#실습
#displ값이 3이하를 추출->mpg3
#displ값이 5이상을 추출->mpg5
#mpg3 hwy 평균
#mpg5 hwy 평균

mpg3<-mpg %>% filter(displ<=3)
mpg5<-mpg %>% filter(displ>=5)
hwy3<-mean(mpg3$hwy)
hwy5<-mean(mpg5$hwy)
hwy3
hwy5

#mpg 생산자 분포 궁금
qplot(mpg$manufacturer)
table(mpg$manufacturer)
str(mpg)
mpg

#volkswagen과 audi 중 cty가 평균적으로 어디가 높은지
vmpg<-mpg %>% filter(manufacturer=="volkswagen")
ampg<-mpg %>% filter(manufacturer=="audi")
vcty_avg<-mean(vmpg$cty)
acty_avg<-mean(ampg$cty)
vcty_avg
acty_avg

#현대, 쉐보레, 닛산 => 데이터 추출
#cty의 전체 평균 출력
table(mpg$manufacturer)
hcnmpg<-mpg %>% filter(manufacturer %in% c("hyundai","chevrolet","nissan"))
hcnmpg$cty
avg1<-mean(hcnmpg$cty)
avg1

#컬럼 추출 : select
exam %>% select(science)
exam %>% select(science,math,class)
exam %>% select(-science,-math,-id)

#%>% : dplyr패키지 설치 & 로드 상태에서만 사용 가능

#3반 추출 -> math 추출
#보통 이런식으로 가독성 좋게 써줌
#head함수로 원하는 수만큼 볼 수도 있다
exam %>%
  filter(class==3) %>%
  select(math,class) %>% 
  head(2)

#math를 기준으로 오름차순 정렬렬
exam %>% arrange(math)

#내림차순
exam %>% arrange(desc(math))

exam %>% arrange(math, science)
exam %>% arrange(class,math)

#연습문제 
#mpg
#1. mpg 데이터는 11개 변수로 구성되어 있습니다.
#이 중 일부만 추출해서 분석에 활용하려고 합니다.
#mpg 데이터에서 class(자동차 종류), cty(도시 연비) 변수를 추출해
#새로운 데이터를 만드세요. 새로 만든 데이터의 일부를 출력해서 
#두 변수로만 구성되어 있는지 확인하세요.

nmpg<-mpg %>% select(class,cty) 
nmpg %>% head

#2
suv_nmpg<-nmpg %>% filter(class=="suv")
str(suv_nmpg$cty)
mean(suv_nmpg$cty)
compact_nmpg<-nmpg %>% filter(class=="compact")
mean(compact_nmpg$cty)

#3
audi_car<-mpg %>% filter(manufacturer=="audi") %>% arrange(desc(hwy)) %>% head(5)
audi_car

#4 : midwest
midwest
str(midwest)
n_midwest<-as.data.frame(midwest)
n_midwest

#5
library(dplyr)
n_midwest<-rename(n_midwest,"total"="poptotal")
n_midwest<-rename(n_midwest,"asian"="popasian")

n_midwest

#6
n_midwest$AsianPerTotal<-(n_midwest$asian/n_midwest$total)*100
hist(n_midwest$AsianPerTotal)
n_midwest$AsianPerTotal

#7
mean_APT<-mean(n_midwest$AsianPerTotal)
mean_APT
n_midwest$asianCheck<-ifelse(n_midwest$AsianPerTotal>mean_APT,"large","small")
n_midwest

#8
table(n_midwest$asianCheck)
qplot(n_midwest$asianCheck)

qplot(data = n_midwest,x = popblack,y = popother,geom = "boxplot")

hist(n_midwest$percollege)
qplot(data = n_midwest,x = state,y = area,geom = "boxplot")

n_midwest %>% arrange(desc(popwhite)) %>% select(popwhite)

midwest %>% head
