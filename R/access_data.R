#! /usr/bin/Rscript --vanilla 


library(RPostgreSQL)
library(RSQLite)
library(ggplot2)
library(lubridate)
library(plyr)

   
db <- dbConnect(SQLite(), dbname="google_trends_db")

df.raw <- dbGetQuery(db, "select * from search_volume") 

df <- df.raw

df$time_period <- as.Date(df$time_period_start)

qplot(time_period, data = df)

df$term <- as.factor(df$term)

ggplot(data = subset(df, group_id == 4),
       aes(x = time_period, y = volume, colour = term)) + geom_line(aes(group = term)) 

+ geom_line(aes(group = term)) +
    facet_wrap(~group_id, ncol = 3)


ggplot(data = subset(df, group_id == 3), aes(x = period, y = volume, colour = term)) +
    geom_line(aes(group = term))


#############
# Access Data
#############




## dbGetQuery(db, "drop table if exists Survey")
## dbWriteTable(db, name = "Survey", value = df.survey, row.names = FALSE)
