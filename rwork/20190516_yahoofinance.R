library(ggplot2)
library(dplyr)

#multicampus �ð迭
df<-read.csv("Data/multicampus.csv",stringsAsFactors = F)
df
str(df)
df$Date<-as.Date(df$Date)

par()
myPar<-par(mfrow=c(2,2))
par(myPar)
ggplot(data=df,aes(x=Date,y=High)) + geom_line() + ylim(0,100000)
ggplot(data=df,aes(x=Date,y=Open)) + geom_line() + ylim(0,100000)
ggplot(data=df,aes(x=Date,y=Low)) + geom_line() + ylim(0,100000)
ggplot(data=df,aes(x=Date,y=Close)) + geom_line() + ylim(0,100000)
