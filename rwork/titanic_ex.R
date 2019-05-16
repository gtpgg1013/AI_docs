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

table(test$Embarked)

qplot(data=train,x=Age,y=PassengerId,color=Survived)
str(test)
boxplot(test$Fare)$stats
