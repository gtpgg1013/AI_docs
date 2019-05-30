#1. list 관련 변수 다루기
a<-list(1,2,3)
length(a)

seq(1,10,by = 2) #결과 int벡터 리턴
as.list(seq(1,10)) #결과 list 리턴

e<-as.list(seq(5,10))
e
length(e)
e[[5]] #list에서 참조시에는 [[]] 대괄호 2개 형식 써야 함
e[[5]]<-88
e

a<-c(1,2,3)
e[[5]][1]<-99
e[[5]]<-a
e

#list에서 특정 자료를 삭제할 때는, NULL을 집어 넣어주면 된다!
#그 원소가 사라지고, 인덱스가 당겨짐
c<-as.list(seq(10,14))
c[[3]]<-NULL 
c

#subset: 특정 범위의 자료를 가져올 수 있음
d<-as.list(seq(20))
d[10:15]

a<-c(1,2,3)
#여러개의 벡터를 좌우/상하 합치면(cbind/rbind) -> matrix (동일 타입일 시)
#matrix
matrix(1:6,ncol=3,byrow = TRUE) #byrow주면 row값부터 채우는 순서로
b<-cbind(c(1,2),c(3,4))

#length : vector/matrix 상관 없이 전체 원소 개수
a<-c(1,2,3)
length(a)
length(b)

#dim
dim(a) #vector인 경우는 NULL
dim(b) #행렬의 경우에는 크기 벡터 나옴

#벡터 인덱싱[[]], 서브셋팅[]
a[1:2]
a[1]
a[[1]]

a<-rbind(1:4, 6:9)
a
a[] #전체
a[1,] #첫번째 행
a[,2] #두번째 열
a[2,2:4]
a[1:2,2:3]
#8을 참조하고 싶다면?
a[2,3]
a[[2,3]]
#두개 다 가능하다

a<-1:10
a
a[5]
#특정요소 제외
a[-5]
b<-a[-5]
a[-7:-9]

#조건문 활용할 때 쓸 수 있다다
bl<-c(T,F,T,T)
k<-1:4
k[bl]
k[k%%2==0]
k<-k*10
k

#변수 초기화
rep(NA,10)

#length주면 이 숫자로 등분해서 생성
seq(0,100,length=5)

set.seed(1)
rnorm(10) #가우시안 정규분포 : 걍 정규분포~ : 난수 발생 함수
runif(10) #구간으로 나눈 후 균등히 분포하게 난수 발생시키는 함수

#둘이 같은 의미이다.
matrix(rnorm(10),c(2,5))
matrix(rnorm(10),nrow = 2,ncol = 5)

#proc.time()을 이용한 시간 측정
x<-1:10000
y<-10001:20000
z<-rep(0,10000)
z[1]<-x[1]+y[1]
z[1]
startTime<-proc.time()

for(i in 1:10000){
  z[i]<-x[i]+y[i]
}
proc.time()-startTime
x[i]+y[i]

#element끼리 비교
a<-c(0,1,2,3)
b<-c(4,2,1)
a==b
#모두 같니? : all() : 배열 전체 비교  
all(a==b)

exp(a)
exp(exp(1))

log(a)
log10(a)

x<-1:5
y<-rep(1,length(x))
x+y
#broadcasting : 연산이 되기 위해서 자동 확장됨
#2가 그냥 스칼라값이 아니라, 알아서 2,2,2,2,2로 변형되어서 계산됨!
x+2

x<-50:59
x
#최댓값
max(x)
#max가 있는 곳의 index
which.max(x)
#최솟값
min(x)
#min이 있는 곳의 index
which.min(x)

#matrix의 column별 summension
x<-matrix(c(10,20,10,20),nrow = 2)
sum(x[,1])
colSums(x)

set.seed(123)
df<-data.frame(k1=c("x","x","y","y","x"),
               k2=c("f","s","f","s","f"),
               d1=rnorm(5),
               d2=rnorm(5))
df

library(dplyr)
#k1 기준으로 2개로 나누는 그룹 객체 생성
#group_by 만으로는 아무것도 안일어나기 때문에 보통 summerise와 같이 쓰임
group_by(df,k1)
summarise(group_by(df,k1),myd1Mean=mean(d1),myd2Mean=mean(d2))

#k1,k2 두개 기준으로 그룹 나눔
summarise(group_by(df,k1,k2),myd1Mean=mean(d1),myd2Mean=mean(d2))

#tidyr : 데이터들 깔끔히 정리정돈할 때 쓰는 package
install.packages("tidyr")
library(tidyr)

#pivot table => 내가 원하는 형식으로 데이터 구조 변경 : 데이터 재구조화
#spread()
group_by(df,k1,k2)
summarise(group_by(df,k1,k2),myMean=mean(d1))
#spread를 알고는 있으되, 너무 깊게는 안해도 된다
spread(summarise(group_by(df,k1,k2),myMean=mean(d1)), k1, myMean)
#  k2       x     y
#1 f     -0.216  1.56  
#2 s     -0.230  0.0705

#두 데이터프레임 합성=> join, merge
#bind : 단순 연결
#merge : 두 df의 공통 key를 사용하여 병합
#df1,df2는 k라는 공통 column 기준으로 병합
df1<-data.frame(k=c('b','b','a','c','a','a','b'),
                d1=0:6)
df1
df2<-data.frame(k=c('a','b','d'),d2=0:2)
merge(df1,df2)

merge(df1,df2,all=T)
merge(df1,df2,all.x=T) #x의 k는 전부 나옴
merge(df1,df2,all.y=T) #y의 k는 전부 나옴

#join 연습 코드
#creating dataframe1
pd=data.frame(Name=c("Senthil","Senthil","Sam","Sam"),
              Month=c("Jan","Feb","Jan","Feb"),
              BS = c(141.2,139.3,135.2,160.1),
              BP = c(90,78,80,81))
print(pd)
#creating dataframe2
pd_new=data.frame(Name=c("Senthil","Ramesh","Sam"),Department=c("PSE","Data Analytics","PSE"))
print(pd_new) 

left_join(pd,pd_new,by="Name")
right_join(pd,pd_new,by="Name")
#inner join : 교집합, 두개 다 있는 것만 보여준다
inner_join(pd,pd_new,by="Name")

#감성분석기
#AI를 이용하는 게 아닌, 단순 감성분석사전을 참고하여 결과를 도출하는 프로세스
install.packages("tidytext")
library(tidytext)
#감성분석사전(afinn) 불러오기 -5~5점
get_sentiments("afinn")
str(get_sentiments("afinn"))
summary(get_sentiments("afinn"))

AFFIN<-data.frame(get_sentiments("afinn"))
AFFIN
str(AFFIN)

hist(AFFIN$score,xlim=c(-6,6),col='blue',breaks=20, xlab='score', ylab='freq', main='AFFIN')
AFFIN %>% filter(score==-4)

oplex<-data.frame(get_sentiments("bing"))
table(oplex$sentiment)

emolex<-data.frame(get_sentiments("nrc"))
emolex
table(emolex$sentiment)

#일케하면 anger만 뽑아낼 수 있다
#[]안에 true/false 넣어서 확인 가능
emolex$word[emolex$sentiment=="anger"]

#감성분석 => 긍정 / 부정
#감성분석 주제
#stackoverflow의 댓글 감성분석?
#한글은 안됨
#그러므로 영어로 해보아라...?


library(tm)
library(stringr)
library(dplyr)

my.text.location<-"Data/papers/"
mypaper<-VCorpus(DirSource(my.text.location))
inspect(mypaper)
str(mypaper[[1]])
mypaper[[1]]$content #char 벡터
class(mypaper[[1]]$content)
class(mypaper[[1]][1])

class(unlist(mypaper[[1]][1])) #벡터는 벡터인데 좀 이상함
as.character(mypaper[[1]][1]) #mypaper[[1]]$content랑 똑같음

length(as.character(mypaper[[1]][1])) #원소개수 1
length(unlist(mypaper[[1]][1]))

mytxt<-c(rep(NA,24))
mytxt

#이게 안됨
#for(i in 1:24){
#  mytxt[i]<-mypaper[[i]]$content
#}

#mytxt



for(i in 1:24){
  mytxt[i]<-as.character(mypaper[[i]][1])
}

str(mytxt) #list
mytxt[2]

install.packages("tidytext")
library(tidytext)
library(tidyr)

#data_frame : tidytext형태로 데이터를 구성
my.df.text<-data_frame(paper.id=1:24, doc=mytxt)
my.df.text

#unnest_tokens:문서 단위의 텍스트를 단어로 분해하는 함수
my.df.text.word<-my.df.text %>% 
  unnest_tokens(word, doc)
my.df.text.word

#단어를 얻었으니 sentiment와 join해주자
#get_sentiments랑 같은 형식으로 만들어주려고 data_frame 썼음
get_sentiments("bing")

#디폴트 : by="word"
#fill = 0 주면 NA->0
myresult.sa<-my.df.text.word %>% 
  inner_join(get_sentiments(("bing"))) %>% 
  count(word, paper.id, sentiment) %>% 
  spread(sentiment,n,fill=0)

myresult.sa

myagg<-summarise(group_by(myresult.sa, paper.id),
          pos.sum=sum(positive),
          neg.sum=sum(negative),
          pos.sent=pos.sum-neg.sum)

myagg

#파일 이름 추출
myfilenames<-list.files(path=my.text.location,all.files = TRUE)
myfilenames

#연도만 추출하기
paper.name<-myfilenames[3:26]
as.numeric(str_extract_all(paper.name,"[[:digit:]]{1,}"))
pub.year<-as.numeric(unlist(str_extract_all(paper.name,"[[:digit:]]{1,}")))
#as.numeric 사용해서 숫자로 저장
pub.year

#id, 이름, year 써있는 df 생성
paper.id<-1:24
pub.year.df<-data.frame(paper.id,paper.name,pub.year)
pub.year.df

mydf<-inner_join(myagg,pub.year.df)
library(ggplot2)
ggplot(data=mydf,aes(x=pub.year,y=pos.sent))+geom_col()
ggplot(data=mydf,aes(x=paper.id,y=pos.sent))+geom_col()

myresult.sa %>%
  group_by(paper.id) %>% 
  summarise(sumNeg=sum(negative),sumPos=sum(positive))

#연도별로 점수내보자
myresult.sa

mytbl<-inner_join(myresult.sa,pub.year.df)
myresult.by.year<-mytbl %>%
  group_by(pub.year) %>% 
  summarise(neg.sum=sum(negative),
            pos.sum=sum(positive),
            sum=pos.sum-neg.sum)
ggplot(myresult.by.year,aes(x=pub.year,y=sum))+geom_col()+xlim(c(2005,2018))+ylim(c(-15,15))


























