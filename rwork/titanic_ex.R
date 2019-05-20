library(dplyr)
library(readxl)
library(ggplot2)
gender_submission<-read.csv("Data/titanic/gender_submission.csv")
gender_submission %>% head()
test<-read.csv("Data/titanic/test.csv")
train<-read.csv("Data/titanic/train.csv")
head(train)
head(test)
str(test)
str(train)
View(test)
View(train)

test$Cabin
table(train$Pclass)
table(is.na(train$Pclass))

train$Survived<-ifelse(train$Survived==1,"Survived","Failed")

train$Survived

train

#pclass별 생존자 비율 : 1이 survived
Pclass_train<-train %>% 
  group_by(Pclass,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

Pclass_train

ggplot(data=Pclass_train,aes(x=Pclass,y=pct,fill=Survived))+
  geom_col(position='stack')

#성별별 생존자 비율
Sex_train<-train %>% 
  group_by(Sex,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

Sex_train

ggplot(data=Sex_train,aes(x=Sex,y=pct,fill=Survived))+
  geom_col()+
  coord_flip()

#sibsp별 생존자 비율 : parch랑 관련있지 않을까?
SibSp_train<-train %>% 
  group_by(SibSp,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

SibSp_train

ggplot(data=SibSp_train,aes(x=SibSp,y=pct,fill=Survived))+
  geom_col()+
  coord_flip()

str(train)
#Parch별 생존자 비율 : 가족 수가 높으면
Parch_train<-train %>% 
  group_by(Parch,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

Parch_train

ggplot(data=Parch_train,aes(x=Parch,y=pct,fill=Survived))+
  geom_col()+
  coord_flip()

#Embarked 별 생존자 비율 : 어디에서 출발했니?
table(is.na(train$Embarked))
table(train$Embarked)
Embarked_train<-train %>% 
  group_by(Embarked,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

Embarked_train

ggplot(data=Embarked_train,aes(x=Embarked,y=pct,fill=Survived))+
  geom_col()+
  coord_flip()

#Fare 별 생존자 비율 :이건 완전 주먹구구식
table(is.na(train$Fare))
table(train$Fare)
Fare_train<-train %>% 
  group_by(Fare,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

Fare_train

ggplot(data=Fare_train,aes(x=Fare,y=pct,col=Survived))+
  geom_point()

max(train$Fare)
#Fare 별 생존자 비율 : 그룹핑
Fare_train<-train %>% 
  mutate(Fareg=ifelse(Fare<=100,"A",
                      ifelse(Fare<=200,"B",
                             ifelse(Fare<=300,"C",
                                    ifelse(Fare<=400,"D","E"))))) %>% 
  group_by(Fareg,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

Fare_train

ggplot(data=Fare_train,aes(x=Fareg,y=pct,fill=Survived))+
  geom_col()

library(stringr)

train_df<-read.csv("Data/titanic/train.csv",stringsAsFactors = F)
str(train_df)
list_Nameg<-list()
#이름이랑 관련해서 Survived랑 관련있는지 확인하자
for(i in c(1:891)){
  words<-str_remove_all(train_df$Name[i],"\\W")
  words<-strsplit(words,split=" ")
  list_Nameg[i]<-words
}
list_Nameg
train_df$Nameg<-ifelse(grep(train_df$Name,"Miss"),"Miss","else")
train_df$Nameg
Name_train<-train %>% 
  mutate(Nameg=ifelse(grep("Miss"),"Miss",
                      ifelse(Fare<=200,"B",
                             ifelse(Fare<=300,"C",
                                    ifelse(Fare<=400,"D","E"))))) %>% 
  group_by(Fareg,Survived) %>% 
  summarise(count=n()) %>% 
  mutate(tot=sum(count)) %>% 
  mutate(pct=round(count/tot*100,1))

Fare_train

ggplot(data=Fare_train,aes(x=Fareg,y=pct,fill=Survived))+
  geom_col()

qplot(data=train,x=Age,y=PassengerId,color=Survived)
str(test)
boxplot(test$Fare)$stats

