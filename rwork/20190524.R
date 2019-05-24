#말뭉치(corpus) 텍스트 전처리
#수집->시각화&전처리->분석->시각화->알고리즘->모델작성->모델평가->유지보수

mytext<-c("software environment",
  "software  environment",
  "software\tenvironment")

mytext
library(stringr)
str_split(mytext, ' ')
strsplit(mytext, " ")

#apply 복습 (x, FUN) : x에 대해서 FUN 함수를 적용하겠다
sapply(str_split(mytext, ' '), length) #length : 단어가 몇개인지 셈
sapply(str_split(mytext, ' '), str_length) #str_length : 각 문자열의 길이
class(sapply(str_split(mytext, ' '), length)) #결과는 vector로 나온다
class(sapply(str_split(mytext, ' '), str_length))
lapply(str_split(mytext, ' '), length)
class(lapply(str_split(mytext, ' '), length)) #결과는 list로 나온다

#공백 처리 과정 : 우리는 공백 하나뿐만 아니라 여러개 있어도 단어를 분류하고 싶다
mytext
#idea : 공백 여러개를 한개로 일괄 치환
#'hi               hello' -> 'hi hello' : 정규표현식 쓰자
mytext.nowhitespace<-str_replace_all(mytext,"[[:space:]]{1,}" ," ") #공백 1개 이상
mytext.nowhitespace
class(mytext.nowhitespace)

sapply(str_split(mytext.nowhitespace, ' '), length)
sapply(str_split(mytext.nowhitespace, ' '), str_length)
class(sapply(str_split(mytext.nowhitespace, ' '), str_length))


#sapply(입력 ; 리스트, 출력 ; 벡터)
#lapply(입력 : 리스트, 출력 : 리스트)
sapply()

#대소문자 통일
mytext<- "The 45th President of the United States,
Donald Trump, states that he knows how to play trump with the former presidnet"

str_split(mytext,' ')
str_extract_all(mytext, boundary("word")) #"character", "line_break", "sentence", "word"
myword<-unlist(str_extract_all(mytext, boundary("word")))
myword

#고유명사들 치환 후
myword<-str_replace(myword, "Trump", "Trump_unique_")
myword<-str_replace(myword, "States", "States_unique_")
myword

#모든 단어 소문자로 쓰기
table(tolower(myword))
#단어별 출현빈도횟수 확인가능

mytext<-c("He is one of statisticians agreeing that R is the No. 1 statistical software.","He is one of statisticians agreeing that R is the No. one statistical software.")
str_split(mytext," ")
unlist(str_split(mytext," "))

#No. 1 같은놈 지우고싶네
#이렇게 하면 숫자+space는 space로 치환
mytext2<-str_replace_all(mytext,"[[:digit:]]{1,}[[:space:]]{1,}","")
mytext2
mytext2<-str_split(mytext2," ")
mytext2
str_c(mytext2[[1]],collapse = " ") # 하나로 묶어주는 함수
str_c(mytext2[[2]],collapse = " ") # 하나로 묶어주는 함수

unlist(mytext2)

#mytext에서 숫자는 모두 _nubmer_로 일괄 치환

# mytext<-unlist(str_split(mytext," "))
mytext3<-unlist(str_extract_all(mytext,boundary("word")))
mytext3

mytext3<-str_replace_all(mytext,"[[:digit:]]{1,}","__number__")
mytext3

#문장 맨 뒤 .과 et al.은 다른것!
mytext<-"Baek et al. (2014) argued that the state of default-setting is critical for people to protect their own personal privacy on the Internet."
str_split(mytext,"\\. ") #\\.뒤에 공백 주자


mytext2<-str_replace_all(mytext,"-"," ")
mytext2 #-으로 이어진 단어는 의미가 없자너

#성씨 다음에 et al.이 오고, 이어서 (연도) 형식 => "__reference__"로 일괄 치환하고자 함
#Baek et al. (2014) -> __reference__
mytext2<-str_replace_all(mytext2,"[[:upper:]]{1}[[:alpha:]]{1,}[[:space:]]{1}(et al\\.)[[:space:]]{1}\\([[:digit:]]{4}\\)",
                         "__reference__")
mytext2

#.을 제거, .뒤에 공백이 0개 이상인 경우
mytext3<-str_replace_all(mytext,"\\.[[:space::]]{0,}","")
mytext3

#불용어 직접 등록 => 불용어 제거
mystopwords<-"(\\ba )|(\\ban )|(\\bthe )" #\\b 쓰면 그 뒤의 단어로 시작되는 것들
mystopwords<-"a | an |^the " #\\b 쓰면 그 뒤의 단어로 시작되는 것들
mytext<-c("She is an actor", "She is the actor")

mytext
mytext<-str_replace_all(mytext,mystopwords,"")

mytext

#불용어 패키지
install.packages("tm")
library(tm)
stopwords("en") #불용어 해당되는 목록
stopwords("SMART") #긴 불용어 목록

#어근동일화 처리...
#시제 고려 -> 동일화
#~s, ~es => 동일화

#가고, 가다, 간, 가니, ... => 동일화

mytextfunc<-function(text){
  mytext<-str_replace_all(text,"(\\bam )|(\\bare )|(\\bis )|(\\bwas )|(\\bwere )|(\\bbe )","be ")
  return(mytext)
}

text<-c("I am a boy. You are a boy. He might be a boy.")

text

mytext.stem<-mytextfunc(text)
mytext.stem

table(str_split(text," "))
table(str_split(mytext.stem," "))

 
#국립국어원 : 
#한글 유의어사용 - 유료..?

#mapCanvas

#n-gram: 2(bi)-gram, 3(tri)-gram (2단어씩 묶기 / 세 단어씩 묶기)
#n번 연이어 등장하는 단어들의 연결
#단어단위로만 쪼개면 문장의 의미를 이해하기 어려울 수 있다
#45th President : 이걸 쪼개면 각 단어는 의미가 없어짐

mytext<- "The 45th President of the United States,
Donald Trump, states that he knows how to play trump with the former presidnet"
#n-gram + 베이즈 이론(조건부 확률) => 문맥 파악 : 확률적으로 접근 : 앞단어를 봤을 때 뒤의 단어가 나올 확률
#자동완성기능
#방탄 : 소년단(0.5) / 복(0.1) / ... : 결국 확률이다
#이걸로 스팸메일 고르는 것도 만들 수 있음

mytext<-"The United States comprises fifty states. In the United States, each state has its own laws. However, federal law overrides state law in the United States."
str_extract_all(mytext,boundary("sentence"))
myword<-unlist(str_extract_all(mytext,boundary("word")))
myword
table(myword) #근데 이거 대소문자/ s, es 전처리작업 해줘야 함
length(table(myword)) #서로 다른 단어들의 개수
sum(table(myword)) #수치들의 합

mytext.2gram<-str_replace_all(mytext,"\\bUnited States","United_States")
#str_replace_all(mytext,"\\bUnited States","United_States")
myword2<-unlist(str_extract_all(mytext.2gram, boundary("word")))
length(table(myword2))

#의미를 이해할 때는 3gram이 가장 적절한 편
#gram앞의 숫자가 너무 커지면 같은 단어뭉치가 없다

#결국 나중에 가면 P("states"|"united") : 등등의 확률 구할 것임 : 조건부 확률

#연습
#1. 2단어씩 연결하여 출력
mywords<-unlist(str_extract_all(mytext,boundary("word")))
length(table(mywords))
length(mywords)
for(i in 1:25){
  word<-mywords[i]
  print(word)
}

#2. 
library(tm)
my.text.location<-"Data/papers/"
#txt 파일 전체 읽은 다음 말뭉치 만들어야 함
mypaper<-VCorpus(DirSource(my.text.location)) #휘발성 말뭉치 만듬 : 소스는 Dirsource 함수로 주면 됨!
mypaper # documents 24 : file이 24개 있다는 뜻
summary(mypaper)
class(mypaper)
mypaper[[1]]$content #뜻하는게 무엇인가? : 문서번호!
mypaper[[2]]$meta
mypaper[[2]]$content

#메타데이터 수정
meta(mypaper[[2]], tag='author')<-"김저자"

#단어_특수문자(#%$!@...)_ 단어

#알파벳+숫자 두개 다 쓸수 있는 alnum / 특수문자 punct
myfunc<-function(x) {
  str_extract_all(x,"[[:alnum:]]{1,}[[:punct:]]{1,}[[:alnum:]]{1,}")
}

mypuncts<-lapply(mypaper, myfunc)
mypuncts
as.data.frame(table(unlist(mypuncts))) %>% arrange(desc(Freq))
library(dplyr)

#수치로 된 자료를 추출
mydigitfunc<-function(x){
  str_extract_all(x,"[[:digit:]]{1,}")
}

#이렇게 추출을 해보면 숫자 자료가 의미가 있는지 없는지 파악할 수 있음
mydigits<-lapply(mypaper,mydigitfunc)
as.data.frame(table(unlist(mydigits))) %>% arrange(desc(Freq))

#신문기사 등에서 숫자가 앞뒤 문맥을 봐야 의미가 있나 없나 정확히 판단 가능

#대문자로 시작하는 단어 추출
myupperfunc<-function(x){
  str_extract_all(x,"[[:upper:]]{1}[[:alnum:]]{1,}")
}

myuppers<-lapply(mypaper,myupperfunc)
myuppers

#이런 모든걸 해주는 함수 : tm_map()
mycorpus<-tm_map(mypaper, removeNumbers) #패키지가 tm인거 쓰면 됨
tm_map(mypaper, removePunctuation)

mycorpus[[1]]$content
removePunctuation("hlelsfldnl22---,,,,sfdlsnhd@$!$")

install.packages("SnowballC")
library(SnowballC)

#어근을 얻을수 있는 패키지
wordStem(c("learn","learns","learning","learned"))
wordStem(c("runed"))

#stemDocument 보면 어근추출 알고리즘 내용 볼 수 있음
#어근추출
cleaned<-tm_map(mypaper,stemDocument)
cleaned[[1]]$content

myfunc<-function(x){
  str_extract_all(x,"[[:alnum:]]{1,}")
}

mywords<-lapply(mypaper,myfunc)

unlist(mywords)
mywords

#문자열 전처리 코드 : 치환!
mycorpus<-tm_map(mypaper, removeNumbers) #패키지가 tm인거 쓰면 됨

# myobj(대상) / 뭐할것인지 / oldexp(기준으로) : 이건 그냥 공식처럼 쓰는게 낫다
mytempfunc<-function(myobject,oldexp,newexp){
  newobject<-tm_map(myobject,
                    content_transformer(function(x,pattern) gsub(pattern,newexp,x)),
                    oldexp)
  print(newobject)
}

mycorpus <- mytempfunc(mycorpus,"-collar","collar")
mycorpus <- mytempfunc(mycorpus,"\\b((c|C)o-)","co")
mycorpus <- mytempfunc(mycorpus,"\\b((c|C)ross-)","cross")
mycorpus <- mytempfunc(mycorpus,"e\\.g\\.","for example")
mycorpus <- mytempfunc(mycorpus,"i\\.e\\.","that is")
mycorpus <- mytempfunc(mycorpus,"\\'s","")
mycorpus <- mytempfunc(mycorpus,"s’","s")
mycorpus <- mytempfunc(mycorpus,"ICD-","ICD")
mycorpus <- mytempfunc(mycorpus,"\\b((i|I)nter-)","inter")
mycorpus <- mytempfunc(mycorpus,"K-pop","Kpop")
mycorpus <- mytempfunc(mycorpus,"\\b((m|M)eta-)","meta")
mycorpus <- mytempfunc(mycorpus,"\\b((o|O)pt-)","opt")
mycorpus <- mytempfunc(mycorpus,"\\b((p|P)ost-)","post")
mycorpus <- mytempfunc(mycorpus,"-end","end")
mycorpus <- mytempfunc(mycorpus,"\\b((w|W)ithin-)","within")
mycorpus <- mytempfunc(mycorpus,"=","is equal to")
mycorpus <- mytempfunc(mycorpus,"and/or","and or")
mycorpus <- mytempfunc(mycorpus,"his/her","his her")
mycorpus <- mytempfunc(mycorpus,"-"," ")

#필요없는 공란을 없애줌
mycorpust<-tm_map(mycorpus,stripWhitespace)
mycorpust[[1]]$content

#만약 tolower(일반 벡터에 쓰이는 함수)를 corpus객체에 쓰고싶으면 content_transformer함수로 변환필요
mycorpust<-tm_map(mycorpus,content_transformer(tolower))
mycorpust[[1]]$content

#불용어 사전 적용 -> 삭제
mycorpust<-tm_map(mycorpus,removeWords,words=stopwords("SMART"))
mycorpust
mycorpust[[1]]$content

#어근 동일화
mycorpust<-tm_map(mycorpus, stemDocument,language="en")
mycorpust[[1]]$content

#TF/IDF
#TF : 각 문서에서 등장 횟수
#IDF : 전체 문서군에서 등장 횟수의 inverse(역수)

#문서*단어 행렬
#DTM : row:D / col:T
dtm.e<-DocumentTermMatrix(mycorpus)
dtm.e

#단어*문서 행렬
#TDM
TermDocumentMatrix(mycorpus)

inspect(dtm.e[1:3,50:60])

#문제 1,2 Titanic에서 호칭 추출해서 factor로 분류 + 시각화
train<-read.csv("Data/titanic/train.csv")
View(train)
train$Name
namelist

myaliasfunc<-function(x){
  str_extract_all(x,"[[:alpha:]]{1,}\\.")
}

a
a<-as.factor(unlist(myaliasfunc(train$Name)))

table(a)
df<-data.frame(table(a))
df<-df %>% arrange(desc(Freq)) %>% head(5)

df<-rename(df,alias=a,freq=Freq)

library(ggplot2)

ggplot(data=df,aes(x=alias,y=freq)) + geom_col() +coord_flip()

#문제 3

library(tm)
my.text.location2<-"Data/nyt/"

mynyt<-VCorpus(DirSource(my.text.location2))

mynyt

tm_map(mynyt, removeNumbers)
tm_map(mynyt, removePunctuation)
tm_map(mynyt, removeWords, word=stopwords("SMART"))
tm_map(mynyt, removeWords, word=stopwords("en"))
tm_map(mynyt, stemDocument, language="english")
tm_map(mynyt, stripWhitespace
tm_map(mynyt, content_transformer(tolower))








