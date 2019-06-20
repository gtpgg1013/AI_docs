library(dplyr)
library(ggplot2)

mpg

mpg<- as.data.frame(ggplot2::mpg)

str(mpg)

boxplot(mpg$cty~mpg$drv)$stat

table(mpg$drv)
nr_mpg<-n_mpg %>% 
  filter(drv=="r"&cty<=18&cty>=11) %>%
  arrange(desc(cty))

nf_mpg<-n_mpg %>% 
  filter(drv=="f"&cty<=25&cty>=15) %>%
  arrange(desc(cty))

n4_mpg<-n_mpg %>% 
  filter(drv=="4"&cty<=20&cty>=9) %>%
  arrange(desc(cty))

nr_mpg<-n_mpg %>% 
  filter(drv=="r"&cty<=18&cty>=11) %>%
  arrange(desc(cty))

n_mpg<-rbind(nf_mpg,n4_mpg,nr_mpg)  
boxplot(n_mpg$cty~n_mpg$drv)$stat

mpg %>% 
  filter(class=="compact") %>% 
  group_by(manufacturer) %>% 
  summarize(count=n())

######################################복습끝###############################################

library(foreign)
library(readxl)
library(ggplot2)
library(dplyr)
raw_welfare<-read.spss(file="C:/BigdataR/koweps.sav", to.data.frame = T)
welfare<-raw_welfare
welfare

welfare<-rename(welfare, 
                sex=h10_g3, #성별
                birth=h10_g4, #연도
                marriage=h10_g10, #혼인여부
                religion=h10_g11, #종교
                income=p1002_8aq1, #급여
                code_job=h10_eco9, #직종코드
                code_region=h10_reg7 #지역코드
)

#age에 대해 group나눔
welfare$age<-2019-welfare$birth+1
welfare<-welfare %>% 
  mutate(ageg=ifelse(age<30,"young",
                     ifelse(age<=59,"old","superold")))
qplot(welfare$ageg)
table(welfare$ageg)

n_welfare<-welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg) %>% 
  summarize(meanIncome=mean(income))

welfare
str(welfare)

str(n_welfare)
  
ggplot(data=n_welfare,aes(x=ageg,y=meanIncome)) + geom_col()

welfare$sex<-ifelse(welfare$sex==1,"male","female")
#나이순으로 정렬하기기
ggplot(data=n_welfare,aes(x=ageg,y=meanIncome)) + geom_col() + scale_x_discrete(limits=c("young","old","superold"))

#성별 월급 차이 + 연령대별로 차이?
#group_by 함수에 인자를 2개 넣으면 그룹을 다양하게 쪼갤 수 있음
sex_ageg<-welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg,sex) %>% 
  summarise(meanIncome=mean(income)) 
sex_ageg

#aes 속성에서 fill인자를 주면 색깔별로 쪼갤 수 있음
ggplot(data=sex_ageg,aes(x=ageg,y=meanIncome,fill=sex)) + 
  geom_col(position = "dodge",show.legend = T) +
  scale_x_discrete(limits=c("young","old","superold"))


#연속적 나이를 선그래프로 보여주자
sex_ageg2<-welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(age,sex) %>% 
  summarise(meanIncome=mean(income))

#col 속성으로 나눠줄 수 있다
ggplot(data=sex_ageg2,aes(x=age,y=meanIncome,col=sex)) + 
  geom_line() +
  scale_x_discrete(limits=c("young","old","superold"))

#어떤 직업이 가장 많은 급여를 받을 것인가...?
welfare$code_job
table(welfare$code_job)

list_job<-read_xlsx("Data/Koweps_Codebook.xlsx",sheet=2)
list_job
View(list_job)
dim(list_job)

#list_job과 welfare를 code_job을 기준으로 연결 (join)
#기준 : id
#여러 그룹을 복합적으로 한 그림으로 보고 싶으면 : x,y,fill 속성을 사용해서 나타내라
welfare<-left_join(welfare,list_job,id="code_job")
welfare %>% 
  filter(!is.na(code_job)) %>% 
  select(code_job,job)

#직업별 평균 급여 출력
job_income<-welfare %>%
  filter(!is.na(income)&!is.na(job)) %>% 
  group_by(job,sex) %>% 
  summarize(meanIncome=mean(income))

top_10<-welfare %>%
  filter(!is.na(income)&!is.na(job)) %>% 
  group_by(job,sex) %>% 
  summarize(meanIncome=mean(income)) %>% 
  head(50)

top_10

ggplot(data=top_10,aes(x=job,y=meanIncome,fill=sex)) +
  coord_flip()+
  geom_col(position = "dodge")

top_10$job
#reorder(정렬대상변수, 연속형변수) : 정렬대상변수가 꼭 factor이어야 함
ggplot(data=top_10,aes(x=reorder(job,meanIncome),y=meanIncome,fill=sex)) +
  coord_flip()+
  geom_col()

df<-welfare %>% 
  filter(sex=="female")

table(df$job)

ggplot(data=top_10,aes(x=reorder(job,-meanIncome),y=meanIncome,fill=sex)) +
  coord_flip()+
  geom_col()

#하위 10개 직업 추출
down_10<-welfare %>% 
  filter(!is.na(income)&!is.na(job)) %>% 
  group_by(job,sex) %>% 
  summarize(meanIncome=mean(income)) %>% 
  tail(40)

down_10 %>% 
  tail(10)

ggplot(data=down_10,aes(x=reorder(job,meanIncome),y=meanIncome,fill=sex))+
  coord_flip()+
  geom_col(position="stack")

#급여 많이 받는 남성 직업 -> 상위 10개 추출
#남성 직업 -> 빈도 10개

welfare

job_male<-welfare %>% 
  filter(!is.na(job)&sex=="male") %>% 
  group_by(job) %>% 
  summarise(count=n()) %>% 
  arrange(desc(count)) %>% 
  head(10)

job_female<-welfare %>% 
  filter(!is.na(job)&sex=="female") %>% 
  group_by(job) %>% 
  summarise(count=n()) %>% 
  arrange(desc(count)) %>% 
  head(10)

job_female

#크기순으로 분류하고프면 reorder함수 사용
ggplot(data=job_male,aes(x=reorder(job,count),y=count))+
  geom_col()+
  coord_flip()

ggplot(data=job_female,aes(x=reorder(job,count),y=count))+
  geom_col()+
  coord_flip()

welfare$religion

class(welfare$religion)
table(welfare$religion)
welfare$religion<-ifelse(welfare$religion==1,"yes","no")

welfare$marriage
table(welfare$marriage)

#종교 유무에 따라 이혼율? : 기혼, 이혼 빼고는 전부 NA 줌
welfare$group_marriage<-ifelse(welfare$marriage==1,"marriage",
                               ifelse(welfare$marriage==3,"divorced",NA))

table(is.na(welfare$group_marriage))
qplot(welfare$group_marriage)

welfare %>% 
  filter(!is.na(group_marriage)) %>% 
  group_by(religion,group_marriage) %>% 
  summarise(n=n()) %>% 
  mutate(tot_group=sum(n)) %>% 
  mutate(pct=round(n/tot_group*100,1))

#round함수 : 반올림하는 거

welfare$code_region

#join하려고 df만들어주기
list_region<-data.frame(code_region=c(1:7),
           region=c("서울",
                    "수도권",
                    "부산,경남,울산",
                    "대구/경북",
                    "대전/충남",
                    "강원/충북",
                    "광주/전남/전북/제주도"))
list_region

welfare<-left_join(welfare,list_region,by="code_region")

welfare %>% 
  select(code_region,region)

#지역별 연령대 표
region_ageg<-welfare %>% 
  group_by(region,ageg) %>% 
  summarise(n=n()) %>% 
  mutate(tot_group=sum(n)) %>% 
  mutate(pct=round((n/tot_group)*100,2))

#색상으로 구분해야함
#보통 x,y 둘중하나가 연속적 값이고 fill속성은 이산적인게 좋다
ggplot(data=region_ageg,aes(x=region,y=pct,fill=ageg)) +
  geom_col() +
  coord_flip()

#노년층만 보고싶을 때
region_ageg_superold<-region_ageg %>% 
  filter(ageg=="superold") %>% 
  arrange(pct)

region_ageg_superold #노년층 퍼센트만 확인

ggplot(data=region_ageg_superold,aes(x=region,y=pct,fill=ageg)) +
  geom_col() +
  coord_flip()

region_ageg

#전체 n과 그에 따른 퍼센테이지를 보고싶으면 이렇게 할 수 있다
ggplot(data=region_ageg,aes(x=reorder(region,n),y=n,fill=ageg)) + geom_col(position = "stack")
ggplot(data=region_ageg,aes(x=reorder(region,n),y=ageg,fill=n)) +
  geom_col(position = "stack") +
  coord_flip()

#각 권역별 연령대별 비율
welfare %>% 
  group_by(code_region,ageg)

str(welfare)
View(welfare)
summary(welfare)

#새로운 패키지
install.packages("ggiraphExtra")
library(ggiraphExtra)
str(USArrests)

head(USArrests)
library(tibble)
#행 index에 있는 데이터(원래 못씀)를 데이터화 시키고 싶다!
crime<-rownames_to_column(USArrests,var="state")
#일케 써주면 행 index로 들어가있던 미 50개주 이름이 state라는 column에 데이터화됨
crime

crime$state<-tolower(crime$state)

install.packages("maps")
library(maps)
#map_data는 각각의 주 단위로 위/경도 확인할 수 있음
state_map<-map_data("state")
state_map
str(state_map)

install.packages("mapproj")
library(mapproj)
ggChoropleth(data=crime,
             aes(fill=Murder,
                 map_id=state),
             map=state_map)

str(crime)

plot(iris$Sepal.Width,iris$Sepal.Length,cex=1.5, pch=".", xlab="width",ylab="length",main = "IRIS")
x<-seq(0,2*pi,0.1)
x
y<-sin(x)
plot(x,y,col="#00ff33")
lines(x,y)

cars
plot(cars,xlim=c(0,25))
#y=b*x+a
abline(a=5,b=3.5,col="#efaa99") # 선 만들어주는 함수

plot(cars,xlim=c(0,30))
#y=b*x+a
abline(a=-5,b=3.5,col="#efaa99") # 선 만들어주는 함수
# v,h 두 직선이 만나는 지점 : 평균 : 이걸 지나야 좋은 선형 회귀
abline(h=mean(cars$dist))
abline(v=mean(cars$speed))

plot(4:6,4:6) #(4,4) (5,5) (6,6)에 점 생성
#text(5,5,"x")
#adj인자를 통해 위치의 어디 부분에 텍스트를 적을 지 결정할 수 있음
text(5,5,"00",adj=c(0,0))
text(5,5,"00",adj=c(1,0))
text(5,5,"00",adj=c(0,1))
text(5,5,"00",adj=c(1,1))

#각 점에다 라벨링! 
plot(cars,cex=.5)
text(cars$speed,cars$dist,pos=3)

plot(cars,cex=4.5)
identify(cars$speed,cars$dist)

plot(iris$Sepal.Width,iris$Sepal.Length,pch=20,xlab="width",ylab="length",xlim=c(0,5),ylim=c(0,10))
points(iris$Petal.Width,iris$Petal.Length,pch="+",col="#ff0000")
legend("topright",legend=c("Sepal","Petal"),pch=c(20,43),col=c("black","red"),bg = "gray")












