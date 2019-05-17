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

ggplot(data=df4,aes(x=group,y=meanIncome))+geom_col()

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

#job별 월급차이
df2<-welfare %>% 
  group_by(code_job) %>% 
  summarise(meanIncome=mean(income, na.rm = T))
qplot(data=df2,x=code_job,y=meanIncome)
ggplot(data=df2,aes(x=code_job,y=meanIncome)) + geom_col()