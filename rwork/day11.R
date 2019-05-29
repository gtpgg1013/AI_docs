#creating dataframe1
pd=data.frame(Name=c("Senthil","Senthil","Sam","Sam"),
              Month=c("Jan","Feb","Jan","Feb"),
              BS = c(141.2,139.3,135.2,160.1),
              BP = c(90,78,80,81))
#creating dataframe2
pd_new=data.frame(Name=c("Senthil","Ramesh","Sam"),
                  Department=c("PSE","Data Analytics","PSE"))
left_join(pd,pd_new, by="Name")
right_join(pd,pd_new, by="Name")

inner_join(pd,pd_new, by="Name")

#1. 리스트 관련 변수 다루기
a<-list(1,2,3)
length(a)

class(seq(5,10))
b<-as.list(seq(5,10))
b

e<-as.list(seq(5,10))

e[[5]]

e[[length(e)-1]]<-99
e

c<-as.list(seq(10,14))
c[[3]]<-NULL #리스트에서 특정 자료 삭제시->NULL 을 집어 넣어주면 됨
c

#subset:특정 범위의 자료를 가져올 수 있음
d<-as.list(seq(20))
d[10:15]

a<-c(1,2,3)
#여러개의 벡터를 좌우로 합치면(cbind, rbind) 행렬
#matrix

matrix(1:6,ncol=3,byrow=TRUE)

cbind(c(1,2),c(3,4))
b<-rbind(c(1,2),c(3,4))

#length:벡터이든 행렬이든 상관없이 전체 원소 개수
a<-c(1,2,3)
length(a)
length(b)
#dim:벡터의 경우에는 NULL, 행렬의 경우에는 크기 벡터
dim(a)
dim(b)

#벡터 인덱싱:[[]], 서브셋팅:[]
a[1:2]
a[1]
a[[1]]

a<-rbind(1:4, 6:9)
a
#8을 참조하여 출력
a[] #전체
a[1,]#첫번째 행
a[,2]#두번째 열
a[2,2:4]
a[1:2,2:3]
a[2,3]
a[[2,3]]

a<-1:10
a
b<-a[-5]
b

c<-a[-7:-9]
c

bl<-c(T,F,T,T)
k<-1:4
k[bl]
k[k%%2==0]

k<-k*10
k

#변수 초기화
rep(NA,10)

seq(0,100, length=5)

set.seed(1)
rnorm(10)#가우시안 정규분포
runif(10)#구간으로 나눈 후 균등하게 분포
matrix(rnorm(10),c(2,5))

x<-1:10000
y<-10001:20000
startTime<-proc.time()
z<-rep(0,10000)
# z[1]<-x[1]+y[1]
# z[1]
for(i in 1:10000){
  z[i]<-x[i]+y[i]
}
proc.time()-startTime

a<-c(0,1,2,3)
b<-c(4,2,1)
a==b #요소끼리 비교
all(a==b) #all:배열 전체 비교

exp(a)
a<-c(0,1,2,3)
log(a)
log10(a)

x<-1:5
y<-rep(1,length(x))
x+y
x+2#broadcasting 2 => 2 2 2 2 2 

x<-50:59
which.max(x)

x<-matrix(c(10,20,10,20),nrow=2)
sum(x[,1])
colSums(x)

library(dplyr)
set.seed(123)
df<-data.frame(k1=c("x","x","y","y","x"),
               k2=c("f","s","f","s","f"),
               d1=rnorm(5),
               d2=rnorm(5))
summarise(group_by(df, k1), myMean=mean(d1))

df

summarise(group_by(df, k1,k2), myMean=mean(d1))

library(tidyr)   #데이터 정리/정돈 패캐지

summarise(group_by(df, k1,k2), myMean=mean(d1))

spread(summarise(group_by(df, k1,k2), myMean=mean(d1)), k2, myMean)

#  k1    k2    myMean
# 1 x     f      0.635
# 2 x     s      0.461
# 3 y     f     -1.27 
# 4 y     s     -0.687

#   k1       f      s
# 1 x      0.635  0.461
# 2 y     -1.27  -0.687





#두 데이터프레임 합성=>join, merge
#bind:단순 연결

#merge:두 df의 공통 key를 사용하여 병합
df1<-data.frame(k=c('b','b','a','c','a','a','b'),
                d1=0:6)
df1
df2<-data.frame(k=c('a','b','d'),d2=0:2)
df2
merge(df1,df2)

merge(df1,df2, all=T)
merge(df1,df2, all.x=T)
merge(df1,df2, all.y=T)



install.packages("tidytext")
library(tidytext)

get_sentiments("nrc")


summary(get_sentiments("afinn"))

AFINN<-data.frame(get_sentiments("afinn"))
hist(AFINN$score, xlim=c(-6,6),col='blue', breaks=20)

get_sentiments("bing")


oplex<-data.frame(get_sentiments("bing"))
table(oplex$sentiment)


emolex<-data.frame(get_sentiments("nrc"))
table(emolex$sentiment)


emolex$word[emolex$sentiment=="anger"]
#감성분석 => 긍정 / 부정
#주제
#한글은 안됨

library(tm)
library(stringr)
library(dplyr)

my.text.location<-"papers/"
mypaper<-VCorpus(DirSource(my.text.location))
inspect(mypaper)

# mypaper[[1]]
# str(mypaper[[1]])
# class(mypaper[[1]]$content)
# mypaper[[1]]$content #문자벡터
# class(mypaper[[1]][1]) #list
# class(unlist(mypaper[[1]][1]))
# as.character(mypaper[[1]][1])#mypaper[[1]]$content

length(as.character(mypaper[[1]][1]))#1
length(unlist(mypaper[[1]][1]))#1

mytxt<-c(rep(NA,24))
mytxt

for(i in 1:24){
  mytxt[i]<-as.character(mypaper[[i]][1])
}
mytxt[24]

install.packages("tidytext")
library(tidytext)
my.df.text<-data_frame(paper.id=1:24, doc=mytxt)
my.df.text
#data_frame:tidytext형태로 데이터를 구성

my.df.text.word<-my.df.text %>% 
  unnest_tokens(word, doc)
#unnest_tokens:문서 단위의 텍스트를 단어로 분해  
library(tidyr)
library(tidytext)
myresult.sa<-my.df.text.word %>% 
  inner_join(get_sentiments("bing")) %>% 
  count(word, paper.id, sentiment) %>% 
  spread(sentiment,n,fill=0)
myresult.sa

myagg<-summarise(group_by(myresult.sa, paper.id),
          pos.sum=sum(positive),
          neg.sum=sum(negative),
          pos.sent=pos.sum-neg.sum)
myagg          

myfilenames<-list.files(path=my.text.location,
                        all.files = TRUE)
paper.name<-myfilenames[3:26]
#pub.year<-as.numeric(unlist(str_extract_all(paper.name, "[[:digit:]]{4}")))
pub.year<-as.numeric(str_extract_all(paper.name, "[[:digit:]]{4}"))
pub.year
#as.numeric(unlist(str_extract_all(paper.name, "[[:digit:]]{4}")))

paper.id<-1:24
pub.year.df<-data.frame(paper.id, paper.name, pub.year)
pub.year.df



베이지안
RNN-S2S,W2V
CNN
GAN








