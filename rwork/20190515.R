library(dplyr)
install.packages("ggplot2")

exam<-read.csv("Data/csv_exam.csv")
exam

exam %>%
  mutate(tot=math+english+science) %>%  #mutate함수 : 변형해서 새로운 파생변수를 만든다
  head


exam %>%
  mutate(tot=math+english+science,
         avg=tot/3) %>%
  head

exam %>%
  mutate(tot=math+english+science,
         avg=tot/3,
         res=ifelse(science>=80,"pass","fail")) %>%
  head

exam %>%
  mutate(tot=math+english+science,
         avg=tot/3) %>%
  arrange(tot) %>% 
  head

#summarize dplyr패키지에서 summary 역할, 
exam %>% summarize(meanMath=mean(math))

table(exam$class)

#반별 수학점수의 평균 및 요약통계치를 알고싶다!
#반별로 그룹을 만들어 줘야 함 : group_by
exam %>% 
  group_by(class) %>% 
  summarize(meanMath=mean(math),
            medianMath=median(math),
            sumMath=sum(math),
            count=n(), #n() : 관측치의 숫자
            sdMath=sd(math),
            minMath=min(math),
            maxMath=max(math))

#근데 이 1차적으로 그룹화를 한 후에 2,3차로 그룹화를 더 할 수도 있다!
str(mpg)
#제조사별, 구동방식별 그룹화
mpg %>% 
  group_by(manufacturer,drv) %>% 
  summarize(meanCty=mean(cty),
            count=n()) %>% 
  head(20)

mpg %>% 
  group_by(manufacturer,drv,class) %>% 
  summarize(meanCty=mean(cty),
            count=n()) %>% 
  head(20)

#자동차 제조사별로 그룹화  
mpg %>% 
  group_by(manufacturer) %>% 
  filter(class=="suv") %>% 
  summarize(meanHwy=mean(hwy),
            meanCty=mean(cty),
            cnt=n()) %>% 
  arrange(desc(meanCty))

#그룹화 할때는 순서도 중요하다
mpg %>% 
  group_by(manufacturer) %>% 
  filter(class=="suv") %>% 
  mutate(avg=(hwy+cty)/2) %>% 
  summarize(meanAvg=mean(avg),
            cnt=n()) %>% 
  arrange(desc(meanAvg))
  
#합치는 것도 중요
mid<-data.frame(sid=c(100,200,300,400,500),
                scoreMid=c(90,90,50,70,100))
final<-data.frame(sid=c(100,200,300,400,500),
                  scoreFinal=c(70,90,50,70,100))
#2개의 df를 1개로 합치기 : join
tot<-left_join(mid,final) #공통된 것으로 자동으로 합치기
tot  

left_join(mid,final,by="sid") #by 뒤 속성으로 조인하겠다
left_join(mid,final,by=c("scoreMid"="scoreFinal")) #by 뒤 속성으로 조인하겠다
left_join(mid,final,by=c("sid"="sid")) #by 뒤 속성으로 조인하겠다

tName<-data.frame(teacher=c("Dave","Cat","Tom","Rose","Jack"),
                  class=c(1,2,3,4,5))
tName
exam

exam_new<-left_join(exam,tName,by="class")
exam_new

#세로방량 합치기 (행 합치기)
mid<-data.frame(sid=c(100,200,300,400,500),
                scoreMid=c(90,90,50,70,100))
final<-data.frame(sid=c(600,700,800,900,1000),
                  scoreFinal=c(70,90,50,70,100))
exam_all<-bind_rows(mid,final)
exam_all

#방량 합치기 (행 합치기)
mid<-data.frame(sid=c(100,200,300,400,500),
                score=c(90,90,50,70,100))
final<-data.frame(sid=c(600,700,800,900,1000),
                  score=c(70,90,50,70,100))
exam_all<-bind_rows(mid,final)
exam_all

#결측치(누락값) 처리
df<-data.frame(sex=c("F","M",NA,"M","F"),
               score=c(50,40,40,30,NA))

df<-data.frame(sex=factor(c("F","M",NA,"M","F")),
               score=c(50,40,40,30,NA))

df
#<NA>는 문자열 타입의 벡터에서 이게 진짜 누락값이라는 뜻(문자열 NA일수도 있기 때문)
is.na(df)
table(is.na(df))
table(is.na(df$sex))

#NA가 포함된 행 제거
dfmiss<-df %>% 
  filter(is.na(score))

#NA가 아닌 행
dfnomiss<-df %>% 
  filter(!is.na(score))

sum(dfnomiss$score) #이제 연산가능

df$id<-c(1:5)

dffull<-df %>% 
  filter(!is.na(score)&!is.na(sex))

dffull

exam$class==1

#na.omit함수를 쓰면 na가 있는 행 다 날려버림
dfnomiss2<-na.omit(df)
dfnomiss2

#연산에서 na.rm=T로 주면 na값 무시하고 연산 실행
mean(df$score, na.rm=T)

#행 및 값 추출
exam[2,]
exam[c(2,3,4,6,7),]
exam[2,"science"]
exam[c(2,3,4,6,7),"science"]<-NA
exam

exam %>%
  summarise(meanSci=mean(science,na.rm = T))

#결측치를 0으로 해놓은 사람들도 있기 때문에 데이터를 잘 들여다 봐야 함
#결측치 대체
#결측치를 math와 eng의평균으로 대체
exam$science<-ifelse(is.na(exam$science),(exam$math+exam$english)/2,exam$science)
#결측치를 평균으로 대체
exam$science<-ifelse(is.na(exam$science),mean(exam$science,na.rm = T),exam$science)

exam

table(is.na(exam$science))

#이상치는 어떻게 처리하는가
#이상치 : 존재할 수 없는 값(학년:-3학년)
#범위를 크게 벗어나는 값(몸무게:250kg)

data<-data.frame(g=c(1,2,3,-3,6),
                 s=c(5,4,3,3,2))
data

table(data$g)
#이상치 -3을 찾은 후, NA로 대체
data$g<-ifelse(data$g==-3,NA,data$g)
data

#s컬럼값이 3보다 작으면 NA처리
data$s<-ifelse(data$s<3,NA,data$s)
data

data %>% 
  filter(!is.na(g)&!is.na(s)) %>% 
  summarise(ms=mean(s))


summary(data)

#성인 몸무게 30kg~150kg
#IQR*1.5 벗어나는 경우, 상하위 0.3% 벗어나는 경우 : 극단치로 봐도 좋다

boxplot(mpg$cty)
summary(mpg$cty)
IQR<-5
new_mpg<-mpg
new_mpg$cty<-ifelse(mpg$cty>19+IQR*1.5,NA,
                ifelse(mpg$cty<14-IQR*1.5,NA,mpg$cty))
boxplot(new_mpg$cty)

#박스플롯의 통계치
boxplot(mpg$hwy)$stats
boxplot.stats(mpg$hwy)

mpg2<-mpg
mpg2$hwy<-ifelse(mpg$hwy<12|mpg$hwy>37,NA,mpg$hwy)
table(is.na(mpg2$hwy))

mpg2
str(mpg2)

#na를 제외한 후, (구동방식)hwy 평균
str(mpg2)
mpg2 %>% 
  group_by(drv) %>% 
  summarize(hMean=mean(hwy,na.rm=T))

#as.factor() as.numeric() : 형변환 할 때 쓰는 함수들
x<-c("a","b","c","c")
str(x)
#나는 이놈이 character가 아니라 factor로 하고싶다!
str(as.character(as.factor(x)))
#level이 범주!

#자료구조 변환(행렬->DF)
#DF에 매트릭스를 집어넣엇 만들 수도 있다
a<-matrix(1:6,ncol=2) #ncol값에 따라 행렬shape결정
class(a)
dfa<-as.data.frame(a)
class(dfa)
b<-data.frame(matrix(1:10,ncol=5))
b

as.factor(c("m","f"))

#흐름제어 코드 if / else

x<-1:5
class(x) #integer
ifelse(x%%2==0,"even number","odd number")

for(i in x){
  print(i)
}
 
i<-0
while(i<10){
  if(i>5){
    break
  }
  i<-i+1
  print(i)
}

#na 처리 함수

x<-data.frame(a=c(1,2,3),
              b=c("a",NA,"c"),
              c=c("a","b",NA))
x
na.omit(x) #na 포함된 행 제외해버리기
na.exclude(x) #상동
na.pass(x)

df<-data.frame(x=1:5,y=seq(2,10,2))
df
df[3,2]<-NA
#residual : 잔차 : 잔여값이 어느정도니? : 이 값들은 실제값과 생성된 모델 사이의 에러
resid(lm(y~x,data=df,na.action = na.omit)) #NA 전체 행을 빼버리기

resid(lm(y~x,data=df,na.action = na.exclude)) #NA값을 무시하기

f<-function(a,b){
  print(a)
  print(b)
}
f(1,2)

head(iris)

View(iris)
str(iris)
summary(iris)

iris3 #똑같은 iris인데 3차원 구조

library(help="datasets")

str(AirPassengers)
Titanic
View(Titanic)
airquality
cars