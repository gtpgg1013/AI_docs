library(tm)
library(KoNLP)
library(rJava)
library(stringr)
library(RWeka)

mytextlocation<-"Data/논문"
mypaper<-VCorpus(DirSource(mytextlocation))
mypaper

#코퍼스 안 통째로 처리 : tm_map
mycorpus<-tm_map(mypaper,removeNumbers)
mycorpus<-tm_map(mypaper,removePunctuation)
mytemp<-lapply(mypaper,function(x){
  str_replace_all(x,"[[:digit:]]{1,}|[[:punct:]]{1,}|[[:lower:]]{1,}","")
})

mypaper[[1]]$content
mytemp[[1]]

#이렇게 하면 list로 리턴!
myNounFun<-function(mytext){
  myNounList<-paste(extractNoun(mytext), collapse = " ")
  return(myNounList)
}

myNounListRes<-myNounFun(mytemp[[1]])
myNounListRes

myNounCorpus<-mycorpus

for(i in 1:length(mytemp)){
  myNounCorpus[[i]]$content<-myNounFun(mycorpus[[i]]$content)
}

myNounCorpus[[1]]$content

#그리구 이 myNounCorpus로 n-gram 사용
biandtrigramTokenizer<-function(x){
  NGramTokenizer(x,Weka_control(min=2,max=3))
}
ngram.tdm<-TermDocumentMatrix(myNounCorpus,control = list(tokenize=biandtrigramTokenizer))
sort(inspect(ngram.tdm),decreasing = TRUE)
str(ngram.tdm)
sort(ngram.tdm$dimnames$Terms,decreasing = TRUE)
ngram.tdm$dimnames$Docs






