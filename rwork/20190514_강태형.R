#연습문제 
#mpg
#1. mpg 데이터는 11개 변수로 구성되어 있습니다.
#이 중 일부만 추출해서 분석에 활용하려고 합니다.
#mpg 데이터에서 class(자동차 종류), cty(도시 연비) 변수를 추출해
#새로운 데이터를 만드세요. 새로 만든 데이터의 일부를 출력해서 
#두 변수로만 구성되어 있는지 확인하세요.

nmpg<-mpg %>% select(class,cty) 
nmpg %>% head

#2
suv_nmpg<-nmpg %>% filter(class=="suv")
str(suv_nmpg$cty)
mean(suv_nmpg$cty)
compact_nmpg<-nmpg %>% filter(class=="compact")
mean(compact_nmpg$cty)

#3
audi_car<-mpg %>% filter(manufacturer=="audi") %>% arrange(desc(hwy)) %>% head(5)
audi_car

#4 : midwest
midwest
str(midwest)
n_midwest<-as.data.frame(midwest)
n_midwest

#5
library(dplyr)
n_midwest<-rename(n_midwest,"total"="poptotal")
n_midwest<-rename(n_midwest,"asian"="popasian")

n_midwest

#6
n_midwest$AsianPerTotal<-(n_midwest$asian/n_midwest$total)*100
hist(n_midwest$AsianPerTotal)
n_midwest$AsianPerTotal

#7
mean_APT<-mean(n_midwest$AsianPerTotal)
mean_APT
n_midwest$asianCheck<-ifelse(n_midwest$AsianPerTotal>mean_APT,"large","small")
n_midwest

#8
table(n_midwest$asianCheck)
qplot(n_midwest$asianCheck)