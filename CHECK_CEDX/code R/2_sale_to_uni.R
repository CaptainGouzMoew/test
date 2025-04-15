setwd("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/分析/再キックオフ")


#----- ライブラリの読み込み -----------------------------------

library(data.table)
library(tidyverse)
library(openxlsx)
library(readxl)

#----- 読み込み ------------------------------------------------

#list.files("tmp")

#販売
sale<-fread("data/tmp/sale.csv")

#PARTNER_CATEGORY=1 個人のみにする
#過去の購入回数を取得
#顧客ごと１レコードにする
sales<-sale %>%
  mutate(WARRANTY_START_DATE=as.Date(as.character(WARRANTY_START_DATE), format="%Y%m%d")) %>%
  mutate(DATEOFBIRTH=as.Date(as.character(DATEOFBIRTH), format="%Y%m%d")) %>%
  mutate(age=2022-year(DATEOFBIRTH)) %>%
  filter(PARTNER_CATEGORY==1)%>%
  group_by(UID) %>%
  mutate(total_buy=n()) %>%
  filter(WARRANTY_START_DATE==min(WARRANTY_START_DATE))%>%
  ungroup() %>%
  select(-V1) %>%  unique %>%
  group_by(UID) %>%
  mutate(last_buy_num=n(), no=row_number()) %>%
  mutate(START_year=year(WARRANTY_START_DATE)) 

sales$age %>% table() %>% barplot()

sales_uni<-sales %>%
  filter(no==1)


#書き出し
write.csv(sales, "data/input/sale_uni_min.csv", row.names=FALSE)
