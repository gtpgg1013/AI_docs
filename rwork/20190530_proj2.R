library(rJava)
library(KoNLP)
library(rvest)
library(dplyr)
library(stringr)
library(tm)
library(tidytext)
library(tidyr)


galaxyReviews<-VCorpus(DirSource("Data/galaxy/"))
galaxyReviews
str(galaxyReviews)
#galaxyReviews[[1]]$content
#galaxyReviews<-tm_map(galaxyReviews,removeNumbers)
#galaxyReviews<-tm_map(galaxyReviews,removePunctuation)
galaxyReviews<-tm_map(galaxyReviews,content_transformer(tolower))

#head(galaxyReviews[[1]][4])

mytempfunct<-function(myobject, oldexp, newexp){
  tm_map(myobject,
         content_transformer(function(x,pattern) gsub(pattern, newexp,x)), 
         oldexp)
}

galaxyReviews<-mytempfunct(galaxyReviews,"[[:digit:]]{1,}","")
galaxyReviews<-mytempfunct(galaxyReviews,"[[:punct:]]{1,}"," ")
galaxyReviews<-mytempfunct(galaxyReviews,"[[:space:]]{1,}"," ")

#불용어제거
galaxyReviews<-tm_map(galaxyReviews,removeWords,words=stopwords("SMART"))

#여기까지 갤럭시 숫자 없애고, 특문 없앰, 소문자화 시킴

mygalaxy<-c(rep(NA,8))

#galaxyReviews[[1]][1]

for(i in 1:8){
  mygalaxy[i]<-as.character(galaxyReviews[[i]][1])
}
my.df.text<-data_frame(galaxy.id=1:8, doc=mygalaxy)
my.df.text.word<-my.df.text %>% 
  unnest_tokens(word,doc)

my.df.text.word

#get_sentiments("bing")

#bing
mygalaxy.result<-my.df.text.word %>% 
  inner_join(get_sentiments("bing")) %>% 
  count(word,galaxy.id,sentiment) %>% 
  spread(sentiment,n,fill=0)
  
mygalaxy.result %>% arrange(desc(negative))
mygalaxy.result %>% arrange(desc(positive))

#afinn
get_sentiments("afinn")

mygalaxy.result<-my.df.text.word %>% 
  inner_join(get_sentiments("afinn")) %>% 
  count(word,galaxy.id,score)

mygalaxy.result

galaxy.scoreby.id<-mygalaxy.result %>%
  group_by(galaxy.id) %>% 
  summarise(score=mean(score*n))

galaxy.scoreby.id$galaxy.id<-c("1_galaxys6","2_galaxys7","3_galaxys8","4_galaxys8p","5_galaxys9","6_galaxys9p","7_galaxys10","8_galaxys10p")
galaxy.scoreby.id

library(ggplot2)
ggplot(data=galaxy.scoreby.id,aes(x=galaxy.id,y=score)) + geom_col()


#galaxyReviews<-lapply(galaxyReviews,function(x){
#  str_replace_all(x,"[[:digit:]]{1,}|[[:punct:]]{1,}","")
#})

#galaxyReviews<-lapply(galaxyReviews,function(x){
#  str_replace_all(x,"[[:space:]]{1,}"," ")
#})

#galaxyReviews<-lapply(galaxyReviews,tolower)


head(unlist(galaxyReviews))

iphoneReviews<-VCorpus(DirSource("Data/iphone/"))
iphoneReviews
str(iphoneReviews)
iphoneReviews<-tm_map(iphoneReviews,content_transformer(tolower))

mytempfunct<-function(myobject, oldexp, newexp){
  tm_map(myobject,
         content_transformer(function(x,pattern) gsub(pattern, newexp,x)), 
         oldexp)
}

iphoneReviews<-mytempfunct(iphoneReviews,"[[:digit:]]{1,}","")
iphoneReviews<-mytempfunct(iphoneReviews,"[[:punct:]]{1,}"," ")
iphoneReviews<-mytempfunct(iphoneReviews,"[[:space:]]{1,}"," ")

#불용어제거
iphoneReviews<-tm_map(iphoneReviews,removeWords,words=stopwords("SMART"))

myiphone<-c(rep(NA,8))

for(i in 1:8){
  myiphone[i]<-as.character(iphoneReviews[[i]][1])
}
str(myiphone[3])
length(myiphone[3])
my.df.text2<-data_frame(iphone.id=1:8, doc=myiphone)
my.df.text.word2<-my.df.text2 %>% 
  unnest_tokens(word,doc)

my.df.text.word2
table(my.df.text.word2$iphone.id)

get_sentiments("bing")

#bing
myiphone.result<-my.df.text.word2 %>% 
  inner_join(get_sentiments("bing")) %>% 
  count(word,iphone.id,sentiment) %>% 
  spread(sentiment,n,fill=0)

my.df.text.word2 %>% 
  inner_join(get_sentiments("bing")) %>% 
  count(word,iphone.id,sentiment)

myiphone.result %>% arrange(desc(negative))
myiphone.result %>% arrange(desc(positive))

#afinn
get_sentiments("afinn")

myiphone.result<-my.df.text.word2 %>% 
  inner_join(get_sentiments("afinn")) %>% 
  count(word,iphone.id,score)

myiphone.result

iphone.scoreby.id<-myiphone.result %>%
  group_by(iphone.id) %>% 
  summarise(score=mean(score*n))

iphone.scoreby.id$iphone.id<-c("iphone5","iphone6","iphone6s","iphone7","iphone7p","iphone8","iphone8p","iphonex")
iphone.scoreby.id

library(ggplot2)
ggplot(data=iphone.scoreby.id,aes(x=iphone.id,y=score)) + geom_col()

iphone.scoreby.id$group<-c(rep("iphone",8))
galaxy.scoreby.id$group<-c(rep("galaxy",8))

iphone.scoreby.id$galaxy.id<-c(rep(NA,8))
galaxy.scoreby.id$iphone.id<-c(rep(NA,8))
iphone.scoreby.id$generation<-c(6,6.5,7,7.5,8,8.5,9,10)
galaxy.scoreby.id$generation<-c(6,6.5,7,7.5,8,8.5,9,10)

iphone.scoreby.id$id<-iphone.scoreby.id$iphone.id
galaxy.scoreby.id$id<-galaxy.scoreby.id$galaxy.id

compare.iphone.galaxy<-rbind(iphone.scoreby.id,galaxy.scoreby.id)

compare.iphone.galaxy


ggplot(data=compare.iphone.galaxy,aes(x=id,y=score,color=group)) + geom_point()
ggplot(data=compare.iphone.galaxy,aes(x=generation,y=score,color=group)) + geom_line(size=2) +
  ylim(c(0,15))

# 이 수치는 좀 별로인 거 같은데..?
#compare.iphone.galaxy<-compare.iphone.galaxy %>% 
#  group_by(group) %>% 
#  summarise(score=mean(score))

#compare.iphone.galaxy

#각 라인마다 가장 많이 나온 단어
#galaxy
my.df.text.word
my.df.text.word$word

g1<-my.df.text.word %>% 
  filter(galaxy.id==1) %>% 
  count(word)

g1 %>% arrange(desc(n))

g2<-my.df.text.word %>% 
  filter(galaxy.id==2) %>% 
  count(word)

g2 %>% arrange(desc(n))

#nrc 사전 분류에 따른 단어 제품군 별 얼마나 나왔는지 
listg<-list()

table(my.df.text.word$galaxy.id)

for(i in 1:8){
  listg[[i]]<-my.df.text.word %>% 
    filter(galaxy.id==i) %>% 
    count(word) %>%
    arrange(desc(n))
}

listg2<-list()

for(i in 1:8){
  listg2[[i]]<-inner_join(as.data.frame(listg[[i]]),get_sentiments("nrc"))
}

df.galaxy<-data.frame()
for(i in 1:8){
  df.galaxy<-rbind(df.galaxy,listg2[[i]] %>% 
                   spread(sentiment,n,fill=0) %>% 
                   summarise(totAng=sum(anger),totAnt=sum(anticipation),
                             totDis=sum(disgust),totFear=sum(fear),totJoy=sum(joy),
                             totNeg=sum(negative),totPos=sum(positive),totSad=sum(sadness),
                             totSur=sum(surprise),totTrust=sum(trust)))
}
df.galaxy.nrc<-data.frame(df.galaxy,row.names=c("1_galaxys6","2_galaxys7","3_galaxys8","4_galaxys8p","5_galaxys9","6_galaxys9p","7_galaxys10","8_galaxys10p"))
df.galaxy.nrc

df.galaxy.per.nrc<-data.frame()

for(i in 1:8){
  df.galaxy.per.nrc<-rbind(df.galaxy.per.nrc,listg2[[i]] %>% 
                             spread(sentiment,n,fill=0) %>% 
                             summarise(totAng=sum(anger),totAnt=sum(anticipation),
                                       totDis=sum(disgust),totFear=sum(fear),totJoy=sum(joy),
                                       totNeg=sum(negative),totPos=sum(positive),totSad=sum(sadness),
                                       totSur=sum(surprise),totTrust=sum(trust)) %>% 
                             mutate(total=totAng+totAnt+totDis+totFear+totJoy+totNeg+totPos+totSad+totSur+totTrust) %>% 
                             summarise(Anger=totAng/total*100,Anticipation=totAnt/total*100,
                                       Disgust=totDis/total*100,Fear=totFear/total*100,Joy=totJoy/total*100,
                                       Negative=totNeg/total*100,Positive=totPos/total*100,Sadness=totSad/total*100,
                                       Surprise=totSur/total*100,Trust=totTrust/total*100))
}

library(dplyr)

df.galaxy.per.nrc<-data.frame(df.galaxy.per.nrc,row.names=c("1_galaxys6","2_galaxys7","3_galaxys8","4_galaxys8p","5_galaxys9","6_galaxys9p","7_galaxys10","8_galaxys10p"))
df.galaxy.per.nrc$galaxy.id<-c("1_galaxys6","2_galaxys7","3_galaxys8","4_galaxys8p","5_galaxys9","6_galaxys9p","7_galaxys10","8_galaxys10p")
df.galaxy.per.nrc

spread(df.galaxy.per.nrc,galaxy.id,Anger)

library(ggplot2)

ggplot(data=df.galaxy.per.nrc) + geom_line()

#iphone
listi<-list()
for(i in 1:8){
  listi[[i]]<-my.df.text.word2 %>% 
    filter(iphone.id==i) %>% 
    count(word) %>%
    arrange(desc(n))
}

#nrc 사전 분류에 따라서 얼마나 나왔는지

listi2<-list()

for(i in 1:8){
  listi2[[i]]<-inner_join(as.data.frame(listi[[i]]),get_sentiments("nrc"))
}

df.iphone<-data.frame()
for(i in 1:8){
  df.iphone<-rbind(df.iphone,listi2[[i]] %>% 
                     spread(sentiment,n,fill=0) %>% 
                     summarise(totAng=sum(anger),totAnt=sum(anticipation),
                               totDis=sum(disgust),totFear=sum(fear),totJoy=sum(joy),
                               totNeg=sum(negative),totPos=sum(positive),totSad=sum(sadness),
                               totSur=sum(surprise),totTrust=sum(trust)))
}
df.iphone.nrc<-data.frame(df.iphone,row.names=c("iphone5","iphone6","iphone6s","iphone7","iphone7p","iphone8","iphone8p","iphonex"))
df.iphone.nrc

listi2[[1]] %>% 
  spread(sentiment,n,fill=0) %>% 
  summarise(totAng=sum(anger),totAnt=sum(anticipation),
            totDis=sum(disgust),totFear=sum(fear),totJoy=sum(joy),
            totNeg=sum(negative),totPos=sum(positive),totSad=sum(sadness),
            totSur=sum(surprise),totTrust=sum(trust)) %>% 
  mutate(total=totAng+totAnt+totDis+totFear+totJoy+totNeg+totPos+totSad+totSur+totTrust) %>% 
  summarise(Anger=totAng/total*100,Anticipation=totAnt/total*100,
            Disgust=totDis/total*100,Fear=totFear/total*100,Joy=totJoy/total*100,
            Negative=totNeg/total*100,Positive=totPos/total*100,Sadness=totSad/total*100,
            Surprise=totSur/total*100,Trust=totTrust/total*100)

df.iphone.per.nrc<-data.frame()
for(i in 1:8){
  df.iphone.per.nrc<-rbind(df.iphone.per.nrc,listi2[[i]] %>% 
                              spread(sentiment,n,fill=0) %>% 
                              summarise(totAng=sum(anger),totAnt=sum(anticipation),
                                        totDis=sum(disgust),totFear=sum(fear),totJoy=sum(joy),
                                        totNeg=sum(negative),totPos=sum(positive),totSad=sum(sadness),
                                        totSur=sum(surprise),totTrust=sum(trust)) %>% 
                              mutate(total=totAng+totAnt+totDis+totFear+totJoy+totNeg+totPos+totSad+totSur+totTrust) %>% 
                              summarise(Anger=totAng/total*100,Anticipation=totAnt/total*100,
                                        Disgust=totDis/total*100,Fear=totFear/total*100,Joy=totJoy/total*100,
                                        Negative=totNeg/total*100,Positive=totPos/total*100,Sadness=totSad/total*100,
                                        Surprise=totSur/total*100,Trust=totTrust/total*100))
}

df.iphone.per.nrc<-data.frame(df.iphone.mean.nrc,row.names=c("iphone5","iphone6","iphone6s","iphone7","iphone7p","iphone8","iphone8p","iphonex"))
df.iphone.per.nrc %>%
  spread(Anger,Anticipation,Disgust,Fear,Joy,Negative,Positive,Sadness,Surprise,Trust)

spread(Anger,Anticipation,Disgust,Fear,Joy,Negative,Positive,Sadness,Surprise,Trust)

df.iphone.per.nrc


library(tidytext)
library(tidyr)

get_sentiments("nrc")
str(get_sentiments("nrc"))
table(get_sentiments("nrc")$sentiment)

