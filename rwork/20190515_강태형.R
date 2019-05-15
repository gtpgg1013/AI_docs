library(ggplot2)
library(dplyr)

#Q1
#1
nmpg<-mpg
nmpg<-nmpg %>% mutate(sumy=cty+hwy)
#2
nmpg<-nmpg %>% mutate(avgy=sumy/2)
#3
nmpg %>% arrange(desc(sumy)) %>% head(3)
#4
mpg %>% 
  mutate(sumy=cty+hwy) %>% 
  mutate(avgy=sumy/2) %>% 
  arrange(desc(avgy)) %>% 
  head(3)

#5
mpg %>% 
  group_by(class) %>% 
  summarize(meanCty=mean(cty))

#6
mpg %>% 
  group_by(class) %>% 
  summarize(meanCty=mean(cty)) %>% 
  arrange(desc(meanCty))

#7
mpg
mpg %>% 
  group_by(manufacturer) %>% 
  summarize(meanHwy=mean(hwy)) %>% 
  arrange(desc(meanHwy)) %>% 
  head(3)

#8
mpg %>% 
  group_by(manufacturer) %>%
  filter(class=="compact") %>% 
  summarize(count=n()) %>% 
  arrange(desc(count))

#Q2
#1
midwest
str(midwest)
df1<-midwest %>%
  mutate(kidsPerAdult=(1-(popadults/poptotal))*100)

midwest$kidsPerAdult<-df1$kidsPerAdult
midwest$kidsPerAdult

#2
midwest %>% 
  group_by(county) %>% 
  arrange(desc(kidsPerAdult)) %>% 
  head(5)

table(midwest$county)

#3
df1<-midwest %>% 
  mutate(kidRank=ifelse(kidsPerAdult>=40,"large",
                        ifelse(kidsPerAdult>=30,"middle","small")))
midwest$kidRank<-df1$kidRank
table(midwest$kidRank)

#4
df1<-midwest %>% 
  mutate(asianPerTotal=(popasian/poptotal)*100)
midwest$asianPerTotal<-df1$asianPerTotal

midwest %>% 
  select(state,county,asianPerTotal) %>% 
  arrange(asianPerTotal) %>%
  tail(10)

#Q3
mpg<-as.data.frame(ggplot2::mpg)
mpg[c(65,124,131,153,212),"hwy"]<-NA

#1
table(is.na(mpg$drv))
table(is.na(mpg$hwy))

#2
str(mpg)
mpg %>%
  filter(!is.na(hwy)) %>% 
  group_by(drv) %>% 
  summarize(meanHwy=mean(hwy))

#Q4
mpg<-as.data.frame(ggplot2::mpg)
mpg[c(10,14,58,93),"drv"] <- "k"
mpg[c(29,43,129,203),"cty"]<-c(3,4,39,42)

#1
table(mpg$drv)
df1<-mpg %>% 
  filter(drv %in% c(4,"f","r"))
table(df1$drv)
mpg<-df1

#2
boxplot(mpg$cty)$stats
mpg<-mpg %>% 
  filter(mpg$cty<=26&mpg$cty>=9)
boxplot(mpg$cty)$stats

#3
str(mpg)
mpg %>% 
  group_by(drv) %>% 
  summarize(meanCty=mean(cty))
