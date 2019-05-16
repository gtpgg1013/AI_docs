library(dplyr)
library(ggplot2)

#지난시간 복습
mpg %>% 
  group_by(manufacturer) %>%
  summarize(meanCty=mean(cty),
            count=n()) %>% 
  head(20)

#read.csv
#option : na.strings : 이 조건에 파라미터로 준 단어는 NA처리해줌
#stringsAsFactors : factor로 읽을 것?

#df 좌우로 합치는 법 : left_join, cbind
#위아래로 합치는 법 : rbind

rbind(c(1,2,3),c(4,5,6))
cbind(c(1,2,3),c(4,5,6))

x<-data.frame(id=c(1,2),
              name=c("a","b"),
              stringsAsFactors = F)
# F주면 name col이 chr로 읽혀짐 / 모든문자열 chr로 읽어버림
# 자료형이 chr이 많다 싶으면 F주고 factor이어야 하는애들은 as.factor로 형변환

x
str(x)

x<-rbind(x,c(3,"c"))
x<-cbind(x,hobby=c(1,2,3))
x

#apply 함수 : ~자료에 ~함수를 적용해라
#argument ; X, margin, FUN
#lapply : list / sapply : vector 등 / tapply : 그룹핑 후 처리 / mapply
#자료형에 대한 정리가 필요할 듯...?
#scalar(0) - vector(1) - matrix(2) <같은 자료형>
#list : 자료형이 달라도 상관 없음 list 안에 모든 자료구조 올 수 있음

a<-matrix(1:9,ncol=3)
a
apply(a,1,sum) # margin 1로주면 왼오 : row들의 합 나열
apply(a,2,sum) # 2로주면 위아래  : col들의 합 나열

head(iris)
str(iris)

apply(iris[,1:4],2,sum)
apply(iris[,1:4],2,mean)

#다른 여러 방법의 함수들도 있다
rowSums(iris[,1:4])
colSums(iris[,1:4])
rowMeans(iris[,1:4])
colMeans((iris[,1:4]))

res<-lapply(1:3, function(x) {x*2})
res #list 자료구조 형태! : [[1]] [1] [2] .../ [[2]] [1] [2] ... 형식!
res[[3]]
class(res)

#list를 해지할 때는
res<-unlist(res)
res
class(res)

res<-list(res,c(1,2))
res
res[[2]]

x<-list(a=1:3,b=4:6)
x
str(x$a)

lapply(x,mean)
lapply(iris[,1:4],mean)

#list에서 df로, df에서 list로 변환작업
class(lapply(iris[,1:4],mean)) #list이다
as.data.frame(lapply(iris[,1:4],mean)) #df로 다시 변경
class(as.data.frame(lapply(iris[,1:4],mean))) # 확인

class(sapply(iris[,1:4],mean)) #numeric이다
sapply(iris,class)
str(iris)

sapply(iris[,1:4], function(x) {x>3}) #fuction을 바로 만들어 넣어 쓸 수도 있다

class(1:10 %% 2==1) # 짝수홀수 결과 벡터(logical)

#tapply(데이터,그룹별 index, function)
tapply(1:10,rep(1,10),sum) #1그룹만 있는 상태
tapply(1:10,1:10%%2==1,sum) #그룹단위로 적용할 때 사용할 수 있다!

tapply(iris$Sepal.Length,iris$Species,mean) #iris 종별로 min값 구할 수 있다 : 간단히 응용 가능

rep(1,10) #arg1을 arg2만큼 반복복

iris[1,] #row 1에 있는 모든 자료
iris[,1] #col 1에 있는 모든 자료

#doBy 패키지 : 데이터 그룹단위 처리
install.packages("doBy")
library(doBy)
summary(iris)
boxplot(iris$Sepal.Width)
quantile(iris$Sepal.Length) #5 numbers 출력해주는 함수 (4사분위 수들)
quantile(iris$Sepal.Length,seq(0,1,0.1)) #두번째 인자로 0,1사이의 숫자들 벡터로 줘서 원하는 분위 검색

summaryBy(Sepal.Length+Sepal.Width~Species,iris) #mean값을 summary해주는 구만

order(iris$Sepal.Length) #정렬된 결과에 대한 index 제공(row의 index)
iris$Sepal.Length[14]
iris$Sepal.Length[132]
iris[order(iris$Sepal.Length,iris$Petal.Length),] #order안에 여러개 쓰면 기준 순차적용

orderBy(~Sepal.Length+Sepal.Width,iris) #~뒤의 column으로 정렬 +로 여려개 적용
#임의의 data 추출할 때 사용하는 sample함수
sample(1:45,6) #비복원추출
sample(1:45,6,replace = T) #복원

NROW(iris) #row 갯수
NCOL(iris)

iris[sample(NROW(iris),NROW(iris)),] #iris index를 뒤죽박죽 섞어서 넣어줌

sampleBy(~Species,frac = 0.1,data=iris) #조건주고 데이터 추출 : ~뒤에거 기준 / frac ; 추출%

split(iris,iris$Species) #종별로 나눈 데이터
class(split(iris,iris$Species)) #결과값은 list 구조

subset(iris, Species=="setosa") #걸러내기 부분집합
subset(iris, Species!="setosa" & Sepal.Length>5.0) # 여러 조건 한꺼번에 줄 수도 있음
subset(iris, select=-c(Species,Sepal.Length)) #원하는 열들만 추출 가능

names(iris) #col의 이름들

iris[,!names(iris) %in% c("Species","Sepal.Length")] #iris의 name이 뒤에 것에 해당하지 않는 것만!

#merge함수

x<-data.frame(name=c("a","b","c"),math=c(1,2,3))
y<-data.frame(name=c("c","b","d"),eng=c(6,4,9))

cbind(x,y)
merge(x,y)
merge(x,y,all = TRUE)

x<-c(5,2,1,4,3)
order(x) #낮은 숫자의 index를 순서대로 써줌
order(x,decreasing = T)
sort(x,decreasing = T)

rbind(x,y)

data=list()

n=10
for(c in 1:n){
  data[[c]]<-data.frame(Index=c,
            myChar=sample(letters,1),
            z=runif(1))
}
data

#fomular 형식 : Y~X (Y; 결과/X; 변수)

#df병합!
#1. rbind
do.call(rbind,data)

install.packages("plyr")
library(plyr)

#2. ldply (list-dataframe-apply) 리스트 넣고 df 리턴
ldply(data,rbind())

#3, rbindlist
install.packages("data.table")
library(data.table)
rbindlist(data)

#rbindlist가 가장 빠름

#with구문은 무엇인가?
mean(iris$Sepal.Length)
with(iris,{
  mean(Sepal.Length)
})

#which구문 : 조건에 맞는 index를 return 해주는 function
which(letters=="a")
which(iris$Species=="setosa")

which.min(iris$Sepal.Length) #speal.length가 최솟값인 index return 
which.max(iris$Sepal.Length)

#실습 : 최빈수 찾기
x<-c(1,1,2,2,2,7,7,1,7,7)

names(which.max(table(x))) #names함수로 column의 이름 추출

#df<-as.data.frame(table(x)) 
#df[which.max(as.data.frame(table(x))$Freq),1]
#이렇게 하면 되긴 하는데 좀 필요없다... 위처럼 하자

letters #알파벳
runif(1) #범위안에서 난수 생성

install.packages("RMySQL")
library(RMySQL)

#database까지 연동
#con에 dbConnect 객체 넣어줌
con<-dbConnect(MySQL(),user="root",
               password="1234",host="127.0.0.1",
               dbname="rprogramming")
#con(rprogramming db)에서 접근가능한 table 리
dbListTables(con)

#Query에 알맞은 결과값을 dataframe 자료구조로 가져옴
df<-dbGetQuery(con, "select * from rtest2")
df

dbGetQuery(con, "select DISTINCT name as N from rtest2 where score>=5")
dbGetQuery(con, "select DISTINCT name N from rtest2 where score>=5")
dbGetQuery(con, "select * from rprogramming.rtest2 where score<=2")

#시각화 관련 도구
#scatterplot : 산점도
install.packages("mlbench")
library(mlbench)

data(Ozone)
head(Ozone)

#사실 이 작업을 시작하기 전에 xlim과 ylim의 적정값을 미리 찾아놔야 함
#x,y의 min max 찾아서 하기기
xrange<-c(min(Ozone$V8,na.rm = T), max(Ozone$V8,na.rm = T))
yrange<-c(min(Ozone$V9,na.rm = T), max(Ozone$V9,na.rm = T))
plot(Ozone$V8, Ozone$V9,xlab="Temp1",ylab = "Temp2",
     main="Ozone",pch="*",cex=2, col="#ccaa99",
     col.axis="#0000ff",col.lab="#00ff00",
     xlim=xrange, ylim=yrange)

help(par) #plot 사용하는 docs

str(Ozone)

cars # 속도와 제동거리

plot(cars,type="l") #엥 line으로 하니까 잘 안보이는 단점이 있네 : 적절한 그래프를 선택해야함
plot(cars,type="b")
plot(cars,type="o") #추세가 좀 잘 안보이네...?
plot(cars$speed,cars$dist)
boxplot(cars$dist)
boxplot(cars$speed)

#speed로 그룹화 / 각 그룹별 dist평균 출력
#tapply(target,기준(인덱스 vector),FUN)

ds<-tapply(cars$dist,cars$speed,mean) #speed로 묶고, dist의 평균 구해주기
ds
#dplyr library로도 할 수 있다
df1<-cars %>% 
  group_by(speed) %>% 
  summarize(distMean=mean(dist))

plot(ds,xlab="speed",ylab = "dist",type = "o",
     cex=0.5, lty="dashed")

plot(x=df1$speed,y=df1$distMean,xlab="speed",ylab = "dist",type = "o",
     cex=0.5, lty="dashed")

#figure(화면) 위에 graph를 여러개 띄워야 하는 경우도 많다!
par() # reset
myPar<-par(mfrow=c(2,1))
par(mfrow=c(1,1))
par(myPar)
plot(Ozone$V8, Ozone$V9,main = "OZONE2")
plot(Ozone$V8, Ozone$V9,main="OZONE")

#ggplot2 패키지 시각화 : 그냥 plot이랑은 조금 다름! 
#1단계 : 배경(axes-axis,axis)
#2단계 : 그래프
#3단계 : option : 축, 색상...

library(ggplot2)
str(mpg)
mpg<-as.data.frame(ggplot2::mpg) #mpg 초기화
ggplot(data = mpg, aes(x=displ,y=hwy))+ #배경
  geom_point()+ #그래프
  xlim(0,10)+ #세부옵션
  ylim(0,50) #세부옵션

qplot(data=mpg,x=displ,y=hwy) #default is scatter
qplot(data=mpg,x=displ) #default is histogram

#ggplot vs qplot
#ggplot():세부조작
#qplot():간단 데이터 확인

#바 그래프 출력
df<-mpg %>% 
  group_by(drv) %>% 
  summarize(meanHwy=mean(hwy))
df
#tibble은 df의 최신버전 : 거의 유사
ggplot(data=df,aes(x=drv,y=meanHwy)) + geom_col()

#reorder : 앞에거를 뒤의 크기 순으로 정렬해라 : 뒤에거의 반대로할려면 뒤에 -붙이기
ggplot(data=df,aes(x=reorder(drv,-meanHwy),y=meanHwy)) + geom_col()

#빈도 바 그래프
ggplot(data=mpg, aes(x=drv)) + geom_bar()
ggplot(data=mpg, aes(x=cty)) + geom_bar()

#geom_col() : 평균-> 그래프 : x,y 찍은 점을 눈에 잘 들어오게 바 형식으로 보여주는 것 뿐
#geom_bar() : 빈도그래프 : x축 하나만 줘야지 빈도를 쌓아줌

#yahoo.com에서 finance 들어가기

economics
View(economics)
str(economics)

#시간의 흐름에 따른 사원의 실업률을 알아보자
ggplot(data=economics, aes(x=date,y=unemploy)) + geom_line()







