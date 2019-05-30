library(dplyr)
library(KoNLP)
library(rJava)
library(stringr)
library(tm)
library(rvest)
install.packages("rvest")

#samsung galaxy lines VS iphone lines

#url<-"https://kuduz.tistory.com/1041"
#temptxt<-read_html(url)
#temptxt

#words<-html_nodes(temptxt, ".tt_article_useless_p_margin")
#word<-html_text(words)
#word

#iphone과 galaxy는 javascript로 짜여있어서 selenium돌려야 함
#iphonelines<-list()
#galaxylines<-list()

urltemp<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-8GB/product-reviews/B00YD53JRO/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
urltemp<-"https://www.naver.com"
htxt<-read_html(urltemp)
htxt
str(htxt)

htxt$node

html<-html_nodes(htxt, css=".blind")
html_text(html)

html<-html_nodes(htxt, css=".a-section")
#html<-html_nodes(html, '.review-text')
html_text(html)

#review<-html_nodes(htxt,".a-section celwidget")
#review

rm(list=ls())

#iphone은 5C부터 시작
iphone5C<-c()

url<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-8GB/product-reviews/B00YD53JRO/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(num in 1:2){
  urltemp<-paste(url,num,sep = "")
  htxt<-read_html(urltemp)
  html<-html_nodes(htxt, '.a-size-base')
  html<-html_text(html)
  html<-str_replace_all(html,"[[:punct:]]{1,}|\\n","")
  html<-str_replace_all(html,"[[:space:]]{1,}"," ")
  iphone5C<-c(iphone5C,html)
}
write.csv(iphone5C,file="iphone5.csv")
iphone5C

iphone6<-c()
url<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-16GB/product-reviews/B00YD547Q6/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(num in 1:200){
  urltemp<-paste(url,num,sep = "")
  htxt<-read_html(urltemp)
  html<-html_nodes(htxt, '.a-size-base')
  html<-html_nodes(html, '.review-text')
  html<-html_text(html)
  html<-str_replace_all(html,"[[:punct:]]{1,}|\\n","")
  html<-str_replace_all(html,"[[:space:]]{1,}"," ")
  iphone6<-c(iphone6,html)
}

iphone6

iphone6S<-c()

library(tidytext)
library(tidyr)
library(dplyr)
library(KoNLP)
library(rJava)
library(stringr)
library(tm)
library(rvest)

#kaggle 자료 활용
movieSent<-read.csv(file="Data/movieSent/train.tsv",
                    header=T,
                    sep="\t",
                    na.strings = c("NA",""),
                    stringsAsFactors = F)

moviePharse<-movieSent$Phrase

moviePharse


my.df.text<-data_frame(moviePharse)
my.df.text

movieScore<-movieSent$Sentiment

mean(movieScore) # 미리 정해진 값의 평균은 2.063578 : 꽤나 부정적임!

my.df.text.word<-my.df.text %>% 
  unnest_tokens(word,moviePharse)
my.df.text.word

#get_sentiments("bing")
get_sentiments("afinn")

myresult<-inner_join(my.df.text.word,get_sentiments("afinn"))

myresult %>% arrange(score)

myresult<-myresult %>%
  count(word,score) 

mysummarise<-myresult %>% 
  group_by(word) %>% 
  summarise(eachscore=score*n)

mysummarise %>% arrange(desc(eachscore))
mysummarise %>% arrange(eachscore)

sum(mysummarise$eachscore) #47100
mean(mysummarise$eachscore) #34.83728



View(myresult)

#bing 사전

myresult<-inner_join(my.df.text.word,get_sentiments("bing"))

myresult

myresult<-myresult %>%
  count(word,sentiment) 

myresult

mysummarise<-myresult %>% 
  spread(sentiment, n,fill=0) %>% 
  summarise(totNeg=sum(negative),totPos=sum(positive))

mysummarise

#positive한 표현이 67558번, negative한 표현이 61164번 나온다

#nrc 사전

myresult<-inner_join(my.df.text.word,get_sentiments("nrc"))

myresult

myresult<-myresult %>%
  count(word,sentiment) 

myresult

myresult %>% 
  spread(sentiment, n, fill=0)

mysummarise<-myresult %>% 
  spread(sentiment, n, fill=0) %>% 
  summarise(totAng=sum(anger),totAnt=sum(anticipation),
            totDis=sum(disgust),totFear=sum(fear),totJoy=sum(joy),
            totNeg=sum(negative),totPos=sum(positive),totSad=sum(sadness),
            totSur=sum(surprise),totTrust=sum(trust))

mysummarise

#  totAng totAnt totDis totFear totJoy totNeg totPos totSad totSur totTrust
#  21395  33890  17970   26724  33224  51553  79545  24864  20328    38731

#loughran 사전

get_sentiments("loughran")
table(get_sentiments("loughran")$sentiment)

myresult<-inner_join(my.df.text.word,get_sentiments("loughran"))

myresult

myresult<-myresult %>%
  count(word,sentiment) 

myresult

myresult %>% 
  spread(sentiment, n, fill=0)

mysummarise<-myresult %>% 
  spread(sentiment, n, fill=0) %>% 
  summarise(totConstraining=sum(constraining),totLit=sum(litigious),
            totNeg=sum(negative),totPos=sum(positive),totSuperfluous=sum(superfluous),
            totUncertiainty=sum(uncertainty))

mysummarise

#totConstraining totLit totNeg totPos totSuperfluous totUncertiainty
#           1348   1875  21627  16299             34            8569

#Rselenium Crwaling
library(rvest)
library(httr)
library(stringr)
install.packages("RSelenium")
library(RSelenium)

iphonelist<-list()
galaxylist<-list()

iphone5C<-c()

remDr<-remoteDriver(remoteServerAddr="localhost",port=4445L, browserName="chrome")
remDr$open()
remDr$navigate("https://www.amazon.com/Apple-iPhone-GSM-Unlocked-8GB/product-reviews/B00YD53JRO/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1")
url_item<-remDr$getPageSource()[[1]]
url_item

url_item<-read_html(url_item,encoding = "UTF-8")
item<-url_item %>%
  html_nodes(".a-size-base") %>% 
  html_nodes(".review-text") %>% 
  html_text()
item[4]
length(item)
item

iphone5c<-c()
iphone6<-c()
iphone6s<-c()
iphone7<-c()
iphone7p<-c()
iphone8<-c()
iphone8p<-c()
iphonex<-c()
iphonexr<-c()
iphonexs<-c()


url<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-8GB/product-reviews/B00YD53JRO/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:150){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphone5c<-c(iphone5c,review)
}
write.csv(iphone5c,file="iphone5.csv")
iphone5c

#iphone6
url<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-16GB/product-reviews/B00YD547Q6/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:270){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphone6<-c(iphone6,review)
}
write.csv(iphone6,file="iphone6.csv")

#iphone6s
url<-"https://www.amazon.com/Apple-iPhone-6S-Unlocked-64GB/product-reviews/B01CR1AA90/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:160){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphone6s<-c(iphone6s,review)
}
write.csv(iphone6s,file="iphone6s.csv")

#iphone7
url<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-32GB/product-reviews/B01N6YAP98/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:160){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphone7<-c(iphone7,review)
}
write.csv(iphone7,file="iphone7.csv")

#iphone7p
url<-"https://www.amazon.com/Apple-iPhone-Plus-Unlocked-32GB/product-reviews/B01NB1FOM3/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:60){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphone7p<-c(iphone7p,review)
}
write.csv(iphone7p,file="iphone7p.csv")

#iphone8
url<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-64GB/product-reviews/B077583FPX/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:10){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphone8<-c(iphone8,review)
}
write.csv(iphone8,file="iphone8.csv")

#iphone8p
url<-"https://www.amazon.com/Apple-iPhone-Plus-Unlocked-64GB/product-reviews/B0775FLHPN/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:20){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphone8p<-c(iphone8p,review)
}
write.csv(iphone8p,file="iphone8p.csv")

#iphonex
url<-"https://www.amazon.com/Apple-iPhone-GSM-Unlocked-64GB/product-reviews/B07757R58W/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:10){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphonex<-c(iphonex,review)
}

#iphonex 두번째
url<-"https://www.amazon.com/Apple-iPhone-Fully-Unlocked-256GB/product-reviews/B0775451TT/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:15){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  iphonex<-c(iphonex,review)
}

write.csv(iphonex,file="iphonex.csv")

#####################################################삼성 - 아이폰 사차원의 벽#############################################

galaxys6<-c()
galaxys7<-c()
galaxys8<-c()
galaxys8p<-c()
galaxys9p<-c()
galaxys10<-c()
galaxys9<-c()
galaxys10p<-c()

#galaxys6
url<-"https://www.amazon.com/Samsung-SM-G920V-Sapphire-Smartphone-Verizon/product-reviews/B01D0JV7AO/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:100){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys6<-c(galaxys6,review)
}

write.csv(galaxys6,file="galaxys6.csv")

#galaxys7
url<-"https://www.amazon.com/Samsung-Galaxy-Verizon-Wireless-Smartphone/product-reviews/B01F48QLFA/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:100){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys7<-c(galaxys7,review)
}

write.csv(galaxys7,file="galaxys7.csv")

#galaxys8
url<-"https://www.amazon.com/Samsung-Galaxy-Factory-Unlocked-Smartphone/product-reviews/B06Y14T5YW/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:130){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys8<-c(galaxys8,review)
}

write.csv(galaxys8,file="galaxys8.csv")

#galaxys9
url<-"https://www.amazon.com/Samsung-Galaxy-S9-Unlocked-Midnight/product-reviews/B07C65XFBB/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:33){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys9<-c(galaxys9,review)
}

write.csv(galaxys9,file="galaxys9.csv")

#galaxys10
url<-"https://www.amazon.com/Samsung-Galaxy-Factory-Unlocked-Phone/product-reviews/B07N4M412B/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:17){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys10<-c(galaxys10,review)
}

write.csv(galaxys10,file="galaxys10.csv")

#galaxys8p
url<-"https://www.amazon.com/Samsung-Galaxy-Factory-Unlocked-Smartphone/product-reviews/B06Y16RL4W/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:112){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys8p<-c(galaxys8p,review)
}

write.csv(galaxys8p,file="galaxys8p.csv")

#galaxys9p
url<-"https://www.amazon.com/Samsung-Galaxy-Factory-Unlocked-Smartphone/product-reviews/B079JXY4TJ/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:178){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys9p<-c(galaxys9p,review)
}

write.csv(galaxys9p,file="galaxys9p.csv")

#galaxys10p
url<-"https://www.amazon.com/Samsung-SM-G975F-Smartphone-International-No-Warranty/product-reviews/B07NZXBRPS/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for(page in 1:4){
  tempurl<-paste(url,page,sep = "")
  remDr$navigate(tempurl)
  url_item<-remDr$getPageSource()[[1]]
  url_item<-read_html(url_item,encoding = "UTF-8")
  review<-url_item %>%
    html_nodes(".a-size-base") %>% 
    html_nodes(".review-text") %>% 
    html_text()
  galaxys10p<-c(galaxys10p,review)
}

write.csv(galaxys10p,file="galaxys10p.csv")


