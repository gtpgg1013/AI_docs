#n-gram µµÃâ
install.packages("RWeka")
library(RWeka)

#NGramTokenizer : ngram ÅäÅ« »ı¼º ÇÔ¼ö
#Weka_control : ngramÀÇ ÃÖ¼Ò, ÃÖ´ë°ª ¼³Á¤

mytext<-c("The United States comprises fifty states.", "In the United States, each state has its own laws.","However, federal law overrides state law in the United States.")
mytext

library(tm)
#¸»¹¶Ä¡ »ı¼º
mytemp<-VCorpus(VectorSource(mytext))
#´Ü¾î¹®¼­Çà·Ä
ngram.tdm<-TermDocumentMatrix(mytemp)
ngram.tdm
#inspect ÇÔ¼ö·Î tm °ü·Ã °´Ã¼µéÀ» display
inspect(ngram.tdm)

#bi or tri
bigramTokenizer<-function(x){
  NGramTokenizer(x, Weka_control(min=2,max=3))
}

#controlÀÌ¶ó´Â 
ngram.tdm<-TermDocumentMatrix(mytemp, control=list(tokenize=bigramTokenizer))
inspect(ngram.tdm)
str(ngram.tdm)
ngram.tdm$dimnames$Terms
ngram.tdm$dimnames$Docs

ngram.tdm[,]

library(dplyr)

#matixµµ È°¿ë°¡´É
#1:Çà´ÜÀ§ ¿¬»ê(´Ü¾î) : ÀüÃ¼ ¹®¼­¿¡¼­ ÇØ´ç ´Ü¾î°¡ ¸î¹ø µîÀå?
#col³¢¸® sortingÇÏ·Á¸é sortÇÔ¼ö ÀÌ¿ë / row³¢¸® sorting ÇÏ·Á¸é %>% arrange ÀÌ¿ë
bigramlist<-apply(ngram.tdm[,], 1, sum)
str(bigramlist)
sort(bigramlist, decreasing =TRUE)

#2:¿­´ÜÀ§ ¿¬»ê(¹®¼­)
apply(ngram.tdm[,], 2, sum)

#myCorpus¿¡µµ À§ ÀÛ¾÷À» ¼öÇà
#ÃÖ»óÀ§ 10°³ÀÇ bigram / trigram ¼öÇà

#ÇÑ±¹¾î Ã³¸®
install.packages("KoNLP")
library(KoNLP)
library(stringr)
library(rJava)

txt<-"¸ÖÆ¼Ä·ÆÛ½º¿¡ ºñ ¿À´Â ³¯¿¡ ¿À´Â °ÍÀº ±×¸® ½±Áö ¾Ê´Ù"
useSejongDic()
extractNoun(txt)

mytextlocation<-"Data/³í¹®/"
#ÆÄÀÏµé ÀüºÎ °¡Á®¿Í¼­ ÄÚÆÛ½º »ı¼º
mypaper<-VCorpus(DirSource(mytextlocation))
mykorean<-mypaper[[19]]$content

#¿µ¹®ÀÚ, °ıÈ£, È¬µû¿ÈÇ¥ µî Æ¯¼ö¹®ÀÚ Á¦°Å
mytext<-str_replace_all(mykorean,"[[:lower:]]","")
mykorean<-str_replace_all(mykorean,"[a-zA-Z]|[[:punct:]]{1,}","") #ÀÏÄÉÇÏ¸é ÇÑ²¨¹ø¿¡ ³¯¸®±â °¡´É
str_replace_all(mytext,"(\\()","")
str_replace_all(mytext,"(\\))","")
str_replace_all(mytext,",","")
#´Ü¾îº° Â¥¸£±â±â
str_extract_all(mykorean,"[[:space:]]*[°¡-ÆR]+[[:space:]]*")

noun.mytext<-extractNoun(mykorean)
table(noun.mytext)

#¼ıÀÚÇ¥Çö ÃßÃâ
mydigits<-lapply(mypaper, function(x) {
  str_extract_all(x,"[[:digit:]]{1,}")
})

mydigits
sort(table(unlist(mydigits)),decreasing = TRUE)

#ÄÚÆÛ½º ¾È¿¡ ÀÖ´Â ¸ğµç°Íµé¿¡ ´ëÇØ ÀÏ°ıÀûÀ¸·Î Ã³¸®ÇÏ°í ½ÍÀº °Ô ÀÖ´Ù : tm_map
mycorpus<-tm_map(mypaper, removeNumbers)

inspect(mycorpus[[3]])

lapply(mycorpus, function(x) {
  str_extract_all(x,"[[:digit:]]{1,}")
})

mytemp<-lapply(mypaper, function(x) {
  str_replace_all(x,"[[:digit:]]{1,}|[[:punct:]]*","")
})

mytemp[[1]]

mypaper[[4]]$content

#Æ¯¼ö¹®ÀÚ¸¦ ±âÁØÀ¸·Î ÁÂ ¿ì¿¡ ¾î¶² ¹®ÀÚµéÀÌ ¿Ô´ÂÁö?
mypuncts<-lapply(mypaper, function(x){
  str_extract_all(x,"\\b[[:alpha:]]{1,}[[:punct:]]{1,}[[:alpha:]]{1,}\\b")
})

sort(table(unlist(mypuncts)),decreasing = TRUE)

#oldexp¸¦ newexp·Î ¹Ù²Ù°Ú´Ù
#x=myobject
mytempfunct<-function(myobject, oldexp, newexp){
  tm_map(myobject,
         content_transformer(function(x,pattern) gsub(pattern, newexp,x)), 
         oldexp)
}

mycorpus<-mytempfunct(mycorpus, "[[:lower:]]","")
mycorpus<-mytempfunct(mycorpus, "[[:upper:]]","")
mycorpus<-mytempfunct(mycorpus, "\\(","")
mycorpus<-mytempfunct(mycorpus, "\\)","")
mycorpus<-mytempfunct(mycorpus, "\\,","")
mycorpus<-mytempfunct(mycorpus, "_","")
mycorpus<-mytempfunct(mycorpus, "-","")
mycorpus<-mytempfunct(mycorpus, "\\.","")
mycorpus<-mytempfunct(mycorpus, "\\?","")
mycorpus<-mytempfunct(mycorpus, "/,","")
mycorpus<-mytempfunct(mycorpus, "¡®","")
mycorpus<-mytempfunct(mycorpus, "¡¯","")
mycorpus<-mytempfunct(mycorpus, "¡¤","")
mycorpus<-tm_map(mycorpus,stripWhitespace)
inspect(mycorpus[[1]])

#ÀÏÄÉÇÏ¸é ¸í»çµé¸¸ µü ½ºÆäÀÌ½º·Î ±¸ºĞÇØ¼­ ÇÑ ¹®ÀåÀ¸·Î È®ÀÎÇÒ ¼ö ÀÖ´Ù
myNounFun<-function(mytext) {
  myNounList<-paste(extractNoun(mytext), collapse = " ")
  return(myNounList)
}

mycorpus[[1]]

myNounFun(mycorpus[[1]]$content)
myNounListRes<-myNounFun(mycorpus[[2]]$content)

myNounListRes

myNounCorpus<-mycorpus

#ÀüÃ¼ ´Ù ¹Ù²ãÁÖ°í
length(mycorpus)
for(i in 1:length(mycorpus)){
  myNounCorpus[[i]]$content<-myNounFun(mycorpus[[i]]$content)
}
myNounCorpus

corplist<-lapply(myNounCorpus,function(x) str_extract_all(x,boundary("word")))

unlist(corplist)
sort(table(unlist(corplist)), decreasing = TRUE)

#¾î ±Ùµ¥ Ä¿¹Â´Ï- ´Ü¾îµéÀº ÀüºÎ´Ù Ä¿¹Â´ÏÄÉÀÌ¼ÇÀ¸·Î ¹Ù²Ù°í½Í´Ù?
#Ä¿¹Â´Ï[[:alpha:]]{1,}

length(myNounCorpus)
imsi<-myNounCorpus
for(i in 1:length(myNounCorpus)){
  myNounCorpus[[i]]$content<-
    str_replace_all(imsi[[i]]$content,
                    "Ä¿¹Â´Ï[[:alpha:]]{1,}",
                    "Ä¿¹Â´ÏÄÉÀÌ¼Ç")
}

#¶È°°Àº ÀÇ¹Ì °¡Áø ´Ü¾îµéµµ ÇÕÃÄÁÖ±â!
for(i in 1:length(myNounCorpus)){
  myNounCorpus[[i]]$content<-
    str_replace_all(imsi[[i]]$content,
                    "À§Å°¸®Å©½º[[:alpha:]]{1,}",
                    "À§Å°¸®Å©½º")
}

dtm.k<-DocumentTermMatrix(myNounCorpus)
dtm.k

colnames(dtm.k)

#±â¼úÅë°è

word.freq<-apply(dtm.k[,],2,sum)
word.freq
apply(dtm.k[,],1,sum)

head(sort(word.freq, decreasing = TRUE))
sort.word.freq<-sort(word.freq, decreasing = TRUE)
sort.word.freq[1:20]
length(word.freq)

#cum ½Ã¸®Áî : ´©Àû°ª
cumsum.word.freq<-cumsum(sort.word.freq)
cumsum.word.freq

length(cumsum.word.freq)
#´©ÀûÇÕ/ÀüÃ¼´©ÀûÇÕ
prop.word.freq<-cumsum.word.freq/cumsum.word.freq[length(cumsum.word.freq)]
prop.word.freq[1:20]

plot(1:length(word.freq),prop.word.freq)
plot(1:length(word.freq),prop.word.freq, type='l')

library("wordcloud")
library(RColorBrewer)
mypal<-brewer.pal(8,"Paired")
wordcloud(names(word.freq),freq=word.freq, min.freq = 3, max.words = 200, col=mypal, random.order = FALSE, scale=c(4,0.2))

#¹Ì±¹ twitter ÇĞ»ıµé ´ëÈ­·Î±× : k-means Å¬·¯½ºÅÍ¸µ
teens<-read.csv("Data/sns.csv")
str(teens)

#¾î ±Ùµ¥ ¼ºº°¿¡ NA°¡ ÀÖ³×?
#¼ºº°À» Å¸°Ù(y)À¸·Î Àâ°í, ³ª¸ÓÁö¸¦ x·Î ÇÑ ´ÙÀ½ »ó°ü°è¼ö¸¦ ±¸ÇÏ¸é
#¾î¶² ¿ä¼Ò°¡ Å¸°Ù¿¡ °¡Àå Å« ¿µÇâÀ» ³¢Ä¡´Â Áö ¾Ë ¼ö ÀÖ´Ù

table(teens$gender)
#NAµµ º¸¿©Áà
table(teens$gender, useNA = "ifany")
#µ¥ÀÌÅÍ´Â ÃÖ´ëÇÑ »ì¸®´Â °Ô ÁÁ´Ù
#teens$age¸¦ º¸¸é ¹º°¡ ÀÌ»óÄ¡°¡ ¸¹´Ù?
summary(teens$age)
boxplot(teens$age)
head(sort(teens$age, decreasing = TRUE))

#teens ³ªÀÌ ÀÌ»óÄ¡ NAÃ³¸®
teens$age<-ifelse(teens$age>13 & teens$age<20,teens$age,NA)

#teens$female<-ifelse(teens$gender=="F",1,0)
#ÀÌ·¸°Ô ÇÏ¸é NAµµ Æ÷ÇÔ°¡´É
teens$female<-ifelse(teens$gender=="F" & !is.na(teens$gender),1,0)
table(teens$female)
teens$nogender<-ifelse(is.na(teens$gender),1,0)
table(teens$nogender)

mean(teens$age)
mean(teens$age, na.rm = TRUE)

table(teens$gradyear)

#¼­¸Ó¸® ÇÔ¼ö (µ¥ÀÌÅÍ, y~x, ÇÔ¼ö) #data.frame
df<-aggregate(data=teens,age~gradyear,mean,na.rm=TRUE)
df %>% filter(gradyear==2006)

class(aggregate(data=teens,age~gradyear,mean,na.rm=TRUE)) #data.frame

#ave(ÇÔ¼ö¸¦ Àû¿ëÇÒ µ¥ÀÌÅÍ, ±âÁØ, ÇÔ¼ö) #vector : À§ÀÇ ÇÔ¼öº¸´Ù ¹Ù·Î °¡Á®´Ù¾²±â Á» ÆíÇÔ
ave_age<-ave(teens$age, teens$gradyear, FUN=function(x) mean(x,na.rm = TRUE))

#º¤ÅÍ·Î Ãâ·Â
class(ave_age)
teens$age<-ifelse(is.na(teens$age),ave_age,teens$age)
summary(teens$age)

str(teens)
teens[,5:40]
interests<-teens[5:40]

#Æ¯Á¤ ÃàÀÇ °ª ¶§¹®¿¡ ÀüÃ¼ °ªÀÌ ¿Ö°îµÉ ¼ö ÀÖ´Ù.
#Áï, À¯Å¬¸®µå ÇÕÀÌ ÇÑ Ãà¶§¹®¿¡ Ä¿Á®¹ö·Á¼­ ºñ½ÁÇÔ¿¡µµ ºÒ±¸ÇÏ°í Å¬·¯½ºÅÍ¸µÀÌ ÀÌ»óÇÏ°Ô µÉ ¼ö ÀÖ´Ù.
#Á¤±ÔÈ­ / re-scaling

#Ç¥ÁØÈ­
interests_z<-as.data.frame(lapply(interests, scale))
interests_z

#ÀÌÁ¦ ±×·³ °Å¸®°è»ê ÇÏ¸é µÊ!
#5°³ÀÇ centroid ±âÁØÀ¸·Î clustering

#Á¤±ÔÈ­ : 0~1·Î ¼³Á¤

#Å¬·¯½ºÅÍ¸µ ÇÏÀÚ!
#½Ãµå ÁÖ°í
set.seed(2345)
#kmeans ÇÔ¼ö È°¿ë
teen_clusters<-kmeans(interests_z,centers=5)
teen_clusters
str(teen_clusters)

teen_clusters$size
teen_clusters$cluster
teen_clusters$centers


str(teen_clusters)
table(teen_clusters$cluster)

#°¢ Å¬·¯½ºÅÍÀÇ ³ªÀÌ Æò±Õ°ª Ãâ·Â
teen_clusters

df_teen_cluster<-as.data.frame(teen_clusters)

teens$cluster<-teen_clusters$cluster

str(teens)

#dplyr ÆĞÅ°Áö
teens %>%
  group_by(cluster) %>% 
  summarise(meanAge=mean(age))

#aggregate ÇÔ¼ö
aggregate(data=teens,age~cluster,mean)
aggregate(data=teens,female~cluster,mean)
aggregate(data=teens,friends~cluster,mean)

#ave ÇÔ¼ö
ave_age<-ave(x=teens$age, y=teens$cluster, FUN=function(x) mean(x,na.rm = TRUE))
ave_age

#±Ùµ¥ °á±¹ ÀÌ Å¬·¯½ºÅÍ·Î gender NA°ªÀ» Ã¤¿ì·Á°í Çß´ø °Í ¾Æ´Ñ°¡...?
#¾Æ! ±×°Ô ¾Æ´Ï¶ó gender NA°ªÀº KNNÀ¸·Î Ã¤¿î´ç (ML)

















