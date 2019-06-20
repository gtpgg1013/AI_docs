library(dplyr)
library(ggplot2)

mpg
# [기초 알고리즘]
# Q1 
tmpmpg <- mpg
tmpmpg$totyb <- tmpmpg$cty + tmpmpg$hwy

# Q2
tmpmpg$avgyb <- (tmpmpg$totyb)/2
tmpmpg$avgyb
tmpmpg$totyb

# Q3 
tmpmpg %>% 
  arrange(avgyb) %>% 
  head(3)

str(tmpmpg)

# [Microsoft R 서버를 활용한 빅데이터 분석]
# Q1
tmpmpg %>%
  group_by(class) %>% 
  summarise(meanCty=mean(avgyb))

# Q2
tmpmpg %>%
  group_by(class) %>% 
  summarise(meanCty=mean(avgyb)) %>% 
  arrange(desc(meanCty))

# Q3
tmpmpg %>% 
  group_by(manufacturer) %>% 
  summarise(meanHwy=mean(hwy)) %>% 
  arrange(desc(meanHwy)) %>% 
  head(3)

# Q4
tmpmpg %>% 
  group_by(manufacturer) %>% 
  count(class='compact') %>% 
  arrange(desc(n))









