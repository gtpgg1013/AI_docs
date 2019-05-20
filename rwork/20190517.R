library(ggplot2)
library(dplyr)

#x축은 범주형, y축은 자료형으로 범주끼리 이상치를 찾아내기 쉽다
ggplot(data=mpg, aes(x=drv,y=cty))+geom_boxplot()

boxplot(mpg$cty~mpg$drv)$stat

table(mpg$drv)
n_mpg<-mpg
nf_mpg<-n_mpg %>% 
  filter(drv=="f"&cty<=25&cty>=15) %>%
  arrange(desc(cty))

n4_mpg<-n_mpg %>% 
  filter(drv=="4"&cty<=20&cty>=9) %>%
  arrange(desc(cty))

nr_mpg<-n_mpg %>% 
  filter(drv=="r"&cty<=18&cty>=11) %>%
  arrange(desc(cty))

n_mpg<-rbind(nf_mpg,n4_mpg,nr_mpg)  
boxplot(n_mpg$cty~n_mpg$drv)$stat

#일케하면 섞어서 볼 수 있음
n_mpg[sample(NROW(n_mpg),NROW(n_mpg)),]

#텍스트마이닝(mining)
#의미, 주제, 감성 : 문단 / 문장 / 단어에 대해
#베이즈 이론 -> 베이지안 필터기, RNN(시간의 흐름에 따라)

#분석절차
#1.형태소 분석
#2.품사 단어 추출
#3.빈도표 작성
#4.시각화
#머신러닝
#5.알고리즘 선택
#6.모델
#7.모델->분류/예측/카테고리화

#음성생성,텍스트생성,챗봇
#햄/스팸

#자연어 처리 가즈아!
#말뭉치(CORPUS) : 분석 대상 문서들의 집합
#말뭉치 > 문서 > 단락 > 문장 > 단어 > 형태소
#"말뭉치를 만든다" / "create CORPUS"

#R에서 사용하는 텍스트마이닝 라이브러리 : java로 되어 있음 : java다운요

install.packages("rJava")
install.packages("KoNLP")

library(KoNLP)
library(dplyr)
library(rJava)
library(stringr)

useNIADic()

txt<-readLines("Data/hiphop.txt")
txt
txt<-str_replace_all(txt,"\\W"," ")
#영문 전처리를 할 때는 don't 같은 경우는 do not 등으로 변형을 시킨 후 특수문자 삭제를 해야함
#he, him, his 결국 한 사람을 가리키는 것이기 때문에 하나로 바꿔줘야 함
#같은 의미를 갖는 동사들 또한 해야 함

#명사추출
res<-extractNoun(txt)
res
extractNoun("멀티캠퍼스 13층에서 수업을 즐겁게 듣는 중 입니다. 점심메뉴는 노랑통닭입니다.")
nouns<-extractNoun(txt)
str(nouns)
nouns

#table함수를 제대로 쓰려면 list 하나당 결과값이 있어야 하는데 그게 아님
#그래서 unlist로 벡터화해야 함
unlist(nouns)
wordcount<-table(unlist(nouns))
class(wordcount)
wordcount
str(wordcount)

df<-as.data.frame(wordcount,stringsAsFactors = F) #word가 factor형이라서 오류났었음
df %>% arrange(desc(Var1))
str(df)

df<-rename(df,word=Var1,freq=Freq)
head(df)

nchar("hello")
nchar(1)

df<-filter(df,nchar(word)>=3)

df %>%
  filter(nchar(word)>=2) %>% 
  arrange(desc(freq)) %>% 
  head(10)

install.packages("wordcloud")
library(wordcloud)

#파레트 생성
pal<-brewer.pal(8,"Dark2")

wordcloud(df$word,df$freq)
wordcloud(words=df$word,freq=df$freq,min.freq = 4,max.words = 100,colors = pal,scale = c(4,1),random.order = F)

bol4<-readLines("Data/bol4.txt")
list(bol4)
bol4

strsplit(bol4[1],split=" ")

mywords<-list()
for(i in 1:216){
  mywords[i]<-strsplit(bol4[i],split=" ")
}

mywords

words_bol4<-unlist(mywords)
table(words_bol4)

df<-as.data.frame(table(words_bol4),stringsAsFactors = F)
df %>%
  arrange(desc(Freq)) %>% 
  filter(nchar(words_bol4)>=3) %>% 
  head(8)

#########################################################################################################

letters
LETTERS

install.packages("stringr")
library(stringr)

tolower("EYE TO EYE")
toupper("eye to eye")

nchar('korea') #단어구성 문자 수 셀때
nchar('머한민국')

#단어단위로 문장 분해
mysentence<-"Leaning R is so interesting"
#strsplit : 단어분해 : list로 반환
mystr<-strsplit(mysentence,split=" ")

mystr[[1]][1]
class(strsplit(mystr[[1]][1],split=""))
mystr

for(i in 1:5){
  print(strsplit(mystr[[1]][i],split=""))
}

myletters<-list()

for(i in 1:5){
  myletters[i]<-strsplit(mystr[[1]][i],split="")
}
myletters

paste("a","b",sep="",collapse = ";")

mywords<-list()

myletters[[1]]

class(myletters[[1]])

for(i in 1:5){
  mywords[[i]]<-paste(myletters[[i]], collapse = "")
}
mywords

paste(mywords,collapse =" ")

rwiki<-"R is a programming language and free software environment for statistical computing and graphics supported by the R Foundation for Statistical Computing.[6] The R language is widely used among statisticians and data miners for developing statistical software[7] and data analysis.[8] Polls, data mining surveys, and studies of scholarly literature databases show substantial increases in popularity in recent years.[9]. as of May 2019, R ranks 21st in the TIOBE index, a measure of popularity of programming languages.[10]

A GNU package,[11] source code for the R software environment is written primarily in C, Fortran and R itself,[12] and is freely available under the GNU General Public License. Pre-compiled binary versions are provided for various operating systems. Although R has a command line interface, there are several graphical user interfaces, such as RStudio, an integrated development environment.[13][14]"

rwiki_para<-strsplit(rwiki,split="\n")
rwiki_para #class : list 

#문단 -> 문장
rwiki_sent<-strsplit(rwiki_para[[1]],split="\\.") # .(콜론)을 구분기호로 쓰고싶으면 \\. 해야함 (이미 예약어)
#대괄호도 다 날려야 함

#문장->단어 분리
rwiki_sent[[1]][1]
strsplit(rwiki_sent[[1]][1], split=" ")
test="R is a programming language and free software environment for statistical computing and graphics supported by the R Foundation for Statistical Computing"

str_replace_all(test,"a","X")

fruits <- c("one apple", "two pears", "three bananas")
str_replace(fruits, "[aeiou]", "-")
str_replace_all(fruits, "[aeiou]",toupper)
#정규표현식의 \W는 \\W로 사용해줘야 함
str_replace_all("ang! gui! mo! tti!","\\W"," ho! ") 


#요 흐름대로 하면 어렵지 않게 단어들을 추출해 낼 수 있다
text<-read.csv("Data/twitter.csv",header=T,fileEncoding = "UTF-8")
text
str(text)
text<-rename(text,no=번호,id=계정이름,date=작성일,tw=내용)
str(text)

text$tw<-str_replace_all(text$tw,"\\W"," ")
head(text$tw)

nouns<-extractNoun(text$tw) #list형식으로 명사들 뽑아내고
nouns

words<-unlist(nouns) #list 형식을 vector로 전환!
words
df<-as.data.frame(table(words),stringsAsFactors = F) #vector->table(빈도수)->df(factor없이)
str(df)
top20<-df %>%
  filter(nchar(words)>=2) %>% 
  arrange(Freq) %>% 
  tail(20)

dfword<-filter(df, nchar(words)>=2)
dfword


top20

order<-arrange(top20,desc(Freq))$word
top20<-arrange(top20,desc(Freq))
ggplot(data=top20,aes(x=words,y=Freq))+
  geom_col()+
  ylim(0,2500)+
  geom_text(aes(label=Freq), hjust=-0.3)+
  scale_x_discrete(limit=order)+
  coord_flip()

str(df)
str(top20)
top20$words
pal<-brewer.pal(8,"Dark2")
wordcloud(words=top20$words,
          freq = top20$Freq,
          colors=pal,
          min.freq = 200,
          max.words = 50)

wordcloud(words=df$words,
          freq = df$Freq,
          colors=pal,
          min.freq = 50,
          max.words = 200,
          random.color = T,
          random.order = F)

#spss파일 읽기 : 인구조사자료
install.packages("foreign")
library(foreign)
library(readxl)
raw_welfare<-read.spss("Data/Koweps.sav",to.data.frame = T)
welfare<-raw_welfare
class(raw_welfare)
str(raw_welfare)

View(welfare)
summary(welfare)

#우리가 추출해야할 것
welfare<-rename(welfare, 
       sex=h10_g3, #성별
       birth=h10_g4, #연도
       marriage=h10_g10, #혼인여부
       religion=h10_g11, #종교
       income=p1002_8aq1, #급여
       code_job=h10_eco9, #직종코드
       code_region=h10_reg7 #지역코드
       )
str(welfare)

#성별에 따라 월급이 차이가 있을까?
class(welfare$sex)
table(is.na(welfare$sex))


qplot(welfare$sex)
class(welfare$income)
summary(welfare$income)

qplot(welfare$income) + xlim(0,1000)

df<-welfare %>% 
  group_by(sex) %>% 
  summarise(meanIncome=mean(income, na.rm = T))

df

df2<-welfare %>% 
  group_by(code_job) %>% 
  summarise(meanIncome=mean(income, na.rm = T))

df2
#성별별 월급차이
qplot(data=df,x=sex,y=meanIncome)
ggplot(data=df,aes(x=sex,y=meanIncome)) + geom_col()

#job별 월급차이
qplot(data=df2,x=code_job,y=meanIncome)
ggplot(data=df2,aes(x=code_job,y=meanIncome)) + geom_col()

str(df2$code_job)
# welfare$sex<-ifelse(welfare$sex==0,NA,welfare$sex)
welfare$sex

#0, 9999 : 이상치 값에 대한 결측처리
x<-ifelse(welfare$income %in% c(0,9999),NA,welfare$income)
table(is.na(x))

#몇 살때 최고급여?
#항상 하기 전에 na가 있나없나 확인해야함!
table(is.na(welfare$income))

df3<-welfare %>% 
  filter(!is.na(income)) %>% 
  filter(!is.na(age)) %>% 
  group_by(age) %>% 
  summarise(meanIncome=mean(income,na.rm = T))

df3

#만일 연도가 9999(미응답) : 이라면 NA처리 해주고프다
ifelse(welfare$birth==9999,NA,welfare$birth)

#나이에 따른 평균 급여
summary(welfare$birth)
table(is.na(welfare$birth))
str(df3)
ggplot(data=df3,aes(x=birth,y=meanIncome))+geom_line()

welfare$age<-2019-welfare$birth+1

ggplot(data=df3,aes(x=age,y=meanIncome))+
  geom_line()+
  theme_bw()+
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_line(color = "grey60", linetype = "dashed"))

qplot(welfare$age)

#연령대별 1~20 / 21~40 ... 연령대별 평균 임금 확인
welfare$group<-ifelse(welfare$age<=20&welfare$age>=0,"child",
                      ifelse(welfare$age<=40,"youth",
                             ifelse(welfare$age<=60,"littleold",
                                    ifelse(welfare$age<=80,"quiteold","superold"))))
welfare$group
df4<-welfare %>% 
  group_by(group) %>% 
  summarize(meanIncome=mean(income,na.rm = T))

welfare$income<-ifelse(is.na(income),0,welfare$income)

welfare$income
table(welfare$group)

df5<-welfare %>% 
  filter(group=="child")

df5$income
ggplot(data=df4,aes(x=group,y=meanIncome))+geom_col()
