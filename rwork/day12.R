install.packages("rvest")
library(rvest)

#url 가져오고
url<-"https://movie.daum.net/moviedb/grade?movieId=111292&type=netizen&page=1"
htxt<-read_html(url)
str(htxt)
#
review<-html_nodes(htxt, ".desc_review")
review
review<-html_text(review)
review



cnt<-html_nodes(htxt, ".txt_menu")
cnt
cnt<-html_text(cnt)
cnt

# 233/10+1 =>24  는 과제임

paste("1","2",sep="")

allReviews<-c()
url_default<-"https://movie.daum.net/moviedb/grade?movieId=111292&type=netizen&page="
for(page in 1:24){
  url<-paste(url_default,page,sep="")  
  htmlTxt<-read_html(url)
  review<-html_nodes(htmlTxt,".desc_review")
  reviews<-html_text(review)
  allReviews<-c(allReviews,reviews)
  print(page)
}
allReviews

install.packages("stringr")
library(stringr)

allReviews<-str_replace_all(allReviews,"[[:punct:]]{1,}","")
allReviews<-str_replace_all(allReviews,"[[:space:]]{1,}"," ")
allReviews

mywords<-unlist(extractNoun(allReviews))
mywords

write.table(allReviews,"review.txt")

allReviews<-c()
url_default<-"https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword=161967&target=before&page="
for(page in 1:40){
  url<-paste(url_default,page,sep="", encoding="euc_kr")  
  htmlTxt<-read_html(url)
  review<-html_nodes(htmlTxt,".list_netizen")
  review<-html_nodes(review,".title")
  #review<-html_nodes(htmlTxt,".title")
  reviews<-html_text(review)
  allReviews<-c(allReviews,reviews)
  #print(review) 
}
allReviews
write.table(allReviews,"review2.txt")

#포털사이트에서 특정 단어를 검색한 후,
#지식인의 글을 추출






allReviews<-c()
url_default<-"https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword=161967&target=before&page="
for(page in 1:40){
  url<-paste(url_default,page,sep="")  
  #print(url)
  htmlTxt<-read_html(url,encoding = "cp949")
  review<-html_nodes(htmlTxt,".list_netizen")
  review<-html_nodes(review,".title")
  # #review<-html_nodes(htmlTxt,".title")
  reviews<-html_text(review)
  allReviews<-c(allReviews,reviews)
  #print(reviews) 
}
allReviews
write.table(allReviews,"review2.txt")




install.packages("rJava")
install.packages("KoNLP")

url<-"https://namu.wiki/w/%EA%B8%B0%EC%83%9D%EC%B6%A9"
htmlTxt<-read_html(url)
content<-html_nodes(htmlTxt,".wiki-heading-content")
content
content<-html_text(content)
#html_nodes(htmlTxt,"a")
class(content)
library(KoNLP)
useSejongDic()
unlist(extractNoun(content))#1894개

text<-sapply(content, extractNoun,USE.NAMES = F)
text<-unlist(text) #1894개
text<-Filter(function(x){nchar(x)>=2},text)
text #1497개

text<-gsub("\\d+","",text)
data<-table(text)
class(table(text))
write.csv(data, "기생충.csv")
data
head(sort(data,decreasing = TRUE), 30)

#트위터 크롤링
install.packages(c("twitteR","ROAuth", "base64enc"))
library("twitteR")
library("ROAuth")
library("base64enc")

# 트위터 계정 발급키 입력
consumerKey <- ""
consumerSecret <- ""
accessToken <- ""
accessTokenSecret <- ""

# oauth 인증 파일 저장
setup_twitter_oauth(consumerKey, consumerSecret, accessToken, accessTokenSecret)
# 콘솔 창에 1(yes) 선택

#키워드 저장
keyword <-enc2utf8("기생충")

# 크롤링할 트위터 수(n=1000)와 언어(lang="ko") 
data<- searchTwitter(keyword, n=1000, lang="ko")
length(data)
data





