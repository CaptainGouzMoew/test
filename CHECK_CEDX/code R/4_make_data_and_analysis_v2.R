setwd("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/分析_local/再キックオフ")

#----- ライブラリの読み込み -----------------------------------

library(data.table)
library(tidyverse)
library(openxlsx)
library(readxl)
library(car)

#----- 読み込み ------------------------------------------------

list.files("data/input")

#service
service<-fread("data/tmp/service.csv") %>%
  mutate(DOC_DATE= as.Date(as.character(DOC_DATE), format="%Y%m%d")) %>%
  mutate(DROP_OFF_DATE= as.Date(as.character(DROP_OFF_DATE), format="%Y%m%d")) %>%
  mutate(PICK_UP_DATE= as.Date(as.character(PICK_UP_DATE), format="%Y%m%d")) %>%
  mutate(DOC_year=year(DOC_DATE)) %>%
  mutate(GROSS_VALUE=if_else(GROSS_VALUE<0, 0, as.double(GROSS_VALUE))) %>%
  filter(DOC_year>2015&DOC_year<=2022) %>%
  select(-customer_index, -Cust_group, -V1)

#sales
sale<-fread("data/input/sale_uni_min.csv") %>%
  mutate(MODEL=str_split(MODEL_TEXT_1, " ",simplify=T)[,1]) %>%
  select(-MODEL_TEXT_1) %>%
  mutate(WARRANTY_START_DATE=as.Date(as.character(WARRANTY_START_DATE), format="%Y-%m-%d")) %>%
  mutate(START_year=year(WARRANTY_START_DATE)) %>%
  filter(START_year>2015 & START_year <=2022) %>%
  select(-DEALER_CODE, -customer_index, -Cust_group)

#combine data
cb<- sale %>%
  left_join(service, by="UID") %>%
  mutate(keika=as.integer(ceiling((DOC_DATE-WARRANTY_START_DATE)/365))) %>%
  mutate(keika=if_else(keika==0, 1, as.double(keika))) %>%
  mutate(bad_q=if_else(is.na(JOB_TYPE), 0, if_else(JOB_TYPE==7, 1, 0))) %>%
  filter(keika>0)

rm(sale, service)

### tgt
tgt<-cb %>%
  filter(JOB_TYPE_DESCRIPTION %in% c("Periodic Maintenance")) %>%
  group_by(UID) %>%
  summarise(PM=length(unique(DOC_DATE)),
            keika_max=max(keika)) %>%
  mutate(freq=PM/keika_max) %>%
  filter(freq<11) %>%  
  mutate(PM_num=floor(freq)) %>%
  mutate(PM2ov=if_else(PM_num>=2, 1, 0)) %>%
  select(UID, PM2ov)

cb<- cb %>%
  filter(DOC_year<2022)

#SA_cont
SA_cont<- cb %>%
  select(UID, DOC_DATE, CUSTOMER_ADVISER) %>% unique %>%
  group_by(UID) %>%
  mutate(rank=rank(DOC_DATE)) %>%
  filter(rank>max(rank)-3) %>%
  mutate(n=n()) %>%
  group_by(UID, CUSTOMER_ADVISER) %>%
  summarise(count=n()) %>%
  filter(count>2) %>%
  select(-count) %>%
  mutate(SA_cont=1)

#UID, JOBごとの金額
JOB_m<-cb %>%
  filter(JOB_TYPE_DESCRIPTION %in% c("Body", "Paint", "General Repair", "Periodic Maintenance")) %>%
  group_by(UID, JOB_TYPE_DESCRIPTION) %>%
  summarise(Total_VALUE=sum(GROSS_VALUE, na.rm=T)) %>%
  pivot_wider(names_from=JOB_TYPE_DESCRIPTION, values_from =Total_VALUE) %>%
  mutate_all(~replace(., is.na(.), 0)) %>%
  mutate(BP=Paint+Body) %>% select(-Paint, -Body) %>%
  rename(GR=`General Repair`, PM=`Periodic Maintenance`)

#UID, JOBごとの来場回数
JOB_vnum<-cb %>%
  filter(JOB_TYPE_DESCRIPTION %in% c("Body", "Paint", "General Repair", "Periodic Maintenance")) %>%
  group_by(UID, JOB_TYPE_DESCRIPTION) %>%
  summarise(visit_num=length(unique(DOC_DATE))) %>%
  pivot_wider(names_from=JOB_TYPE_DESCRIPTION, values_from =visit_num) %>%
  mutate_all(~replace(., is.na(.), 0)) %>%
  mutate(BP_vnum=Paint+Body) %>% select(-Paint, -Body) %>%
  rename(GR_vnum=`General Repair`, PM_vnum=`Periodic Maintenance`)

#タイヤ、オイル、バッテリー履歴
TB<-cb %>%
  mutate(TIRE=if_else(str_detect(DESCRIPTION_ONE, pattern="TIRE"),1,0),
         BATTERY=if_else(str_detect(DESCRIPTION_ONE, pattern="BATTERY"),1,0),
         OIL=if_else(str_detect(DESCRIPTION_ONE, pattern="OIL")&
                       str_detect(DESCRIPTION_ONE, pattern="HONDA"),1,0)) %>%
  group_by(UID) %>% summarise(TIRE=sum(TIRE), BATTERY=sum(BATTERY), OIL=sum(OIL))

#PM
PM<-cb %>%
  filter(JOB_TYPE_DESCRIPTION == "Periodic Maintenance") %>%
  group_by(UID) %>%
  summarise(latest_visit_year=max(DOC_year),
            START_year=min(START_year),
            visit_year=length(unique(DOC_year))) %>%
  mutate(visit_rate=visit_year/(2022-START_year)) %>%
  select(-START_year)

#集計
smr <- cb %>%
  group_by(UID) %>%
  summarise(RUN=max(COUNTER_READING),
            Total_VALUE=sum(GROSS_VALUE, na.rm=T)+sum(SALES_PRICE, na.rm=T),
            visit_num=length(unique(DOC_DATE)),
            keika_max=max(keika),
            bad_q=max(bad_q),
            START_year=min(START_year),
            START_date=min(WARRANTY_START_DATE),
            total_buy=max(total_buy)
  )%>%
  mutate(visit_freq_y=visit_num/keika_max) %>%
  left_join(JOB_m, by="UID") %>%
  left_join(JOB_vnum, by="UID") %>%
  mutate(TTL=BP+GR+PM, TTL_uni=TTL/(GR_vnum+BP_vnum+PM_vnum),
         GR_uni=GR/GR_vnum, BP_uni=BP/BP_vnum, PM_uni=PM/PM_vnum,
         GR_freq=GR_vnum/keika_max, BP_freq=BP_vnum/keika_max, PM_freq=PM_vnum/keika_max) %>%
  left_join(TB, by="UID") %>%
  left_join(PM, by="UID") %>%
  left_join(SA_cont, by="UID")

glimpse(smr)

rm(cb, JOB_m, JOB_vnum, TB, PM)

#########################
#  fail
#########################

#Maintanance Pack
mp<-fread("data/tmp/mp.csv") %>%
  group_by(UID) %>%
  summarise(mp_num=n()) %>%
  mutate(mp=1)

list.files("data/tmp2")

#My Honda
MH<-fread("data/tmp2/MH_new_name.csv")

#Chatbot
chat<-fread("data/tmp2/chat_output.csv") 

#Comprain
CR<-fread("data/tmp2/comp_output.csv")
#DCSI
dcsi<-fread("data/tmp2/DCSI_output_ver2.csv") %>%
  group_by(UID) %>% filter(Year==max(Year)) %>%
  summarise(total_satisfaction=mean(total_satisfaction, na.rm=T),
            satisfaction_reminder=mean(satisfaction_reminder, na.rm=T),
            satisfaction_reception=mean(satisfaction_reception, na.rm=T),
            satisfaction_customer_lounge=mean(satisfaction_customer_lounge, na.rm=T),
            satisfaction_delivery=mean(satisfaction_delivery, na.rm=T),
            satisfaction_repair_quality=mean(satisfaction_repair_quality, na.rm=T),
            satisfaction_facility=mean(satisfaction_facility, na.rm=T),
            one_time_repair=mean(one_time_repair, na.rm=T),
            follow_call=mean(follow_call, na.rm=T))
#EW
ew<-fread("data/tmp2/ew_output.csv") %>%
  select(-ew_all_car)
#event_v_promo
eve_v_pro<-fread("data/tmp2/event_v_promo_new_name.csv") %>%
  select(-event_v_promo)
#book
book<-fread("data/tmp2/book_new_name.csv") %>%
  select(-UID_counts_book, -UID有無)

#test_drive
test_drive<-fread("data/tmp2/test_drive_output.csv") 
#estimate_cost
estimate_cost<-fread("data/tmp2/estimate_cost_output.csv") %>%
  rename(estimate_cost=s)
#view_product_color
view_product_color<-fread("data/tmp2/view_product_color_output.csv") %>%
  rename(view_product_color=s)
#view_product_detail_am
view_product_detail<-fread("data/tmp2/view_product_detail_am_output.csv") %>%
  rename(view_product_detail=s)
#view_product_gallery
view_product_gallery<-fread("data/tmp2/view_product_gallery_output.csv") %>%
  rename(view_product_gallery=s)
#view_product_list
view_product_list<-fread("data/tmp2/view_product_list_output.csv") %>%
  rename(view_product_list=s)
#view_promotion_notification
view_promotion_notification<-fread("data/tmp2/view_promotion_notification_output.csv") 
#view_test_drive
view_test_drive<-fread("data/tmp2/view_test_drive_output.csv") 
#sca
sca<-fread("data/tmp2/SCA_output.csv") 
#notif_book_pi
notif_book_pi<-fread("data/tmp2/notif_book_pi_new_name.csv") 
#notif_book_pm
notif_book_pm<-fread("data/tmp2/notif_book_pm_new_name.csv") 
#notif_book_spa
notif_book_spa<-fread("data/tmp2/notif_book_spa_new_name.csv") 
#notif_v_pro
notif_v_pro<-fread("data/tmp2/notif_v_pro_new_name.csv") 
#notif_v_spa
notif_v_spa<-fread("data/tmp2/notif_v_spa_new_name.csv") 
#notif_vpi
notif_vpi<-fread("data/tmp2/notif_vpi_new_name.csv") 
#notif_vpm
notif_vpm<-fread("data/tmp2/notif_vpm_new_name.csv") 

smr<- smr %>% left_join(mp, by="UID") %>%
  left_join(MH, by="UID") %>%
  left_join(chat, by="UID") %>%
  left_join(CR, by="UID") %>%
  left_join(dcsi, by="UID") %>%
  left_join(ew, by="UID") %>%
  left_join(eve_v_pro, by="UID") %>%
  left_join(book, by="UID") %>%
  left_join(test_drive, by="UID") %>%
  left_join(estimate_cost, by="UID") %>%
  left_join(view_product_color, by="UID") %>%
  left_join(view_product_detail, by="UID") %>%
  left_join(view_product_gallery, by="UID") %>%
  left_join(view_product_list, by="UID") %>%
  left_join(view_promotion_notification, by="UID") %>%
  left_join(view_test_drive, by="UID") %>%
  left_join(sca, by="UID") %>%
  left_join(notif_book_pi, by="UID") %>%
  left_join(notif_book_pm, by="UID") %>%
  left_join(notif_book_spa, by="UID") %>%
  left_join(notif_v_pro, by="UID") %>%
  left_join(notif_v_spa, by="UID") %>%
  left_join(notif_vpi, by="UID") %>%
  left_join(notif_vpm, by="UID") %>%
  left_join(tgt, by="UID") %>%
  mutate(visit_rate=if_else(visit_rate>1, 100, visit_rate*100))%>%
  mutate(keika_max=2021-START_year)%>%
  filter(keika_max>0) %>%
  select(-PM_freq, -BP_freq, -GR_freq,-visit_year) #%>%
select(-CUSTOMER_ADVISER, -visit_num,
       -visit_freq_y , -GR_vnum, -PM_vnum, -BP_vnum,
       -TTL_uni, -TTL, -GR_uni, -BP_uni, -PM_uni,-RUN,
       -OIL,-Total_VALUE, -GR,-PM,-BP,-ew_sales,
       -app_mente_SA_select, -app_mente_SA_select,
       -CR_feedback, -satisfaction_mechanic, -mp_num,-bad_q,
       -notif_book_pi, -notif_book_pm, -notif_book_spa,
       -test_drive, -starts_with("satisfaction"), -follow_call, 
       -one_time_repair,
       -coupon_view, -view_product_color, -view_product_gallery,
       -chat_num, -sca_visit_num, -view_product_list,
       -view_promotion_notification, -MH_Active,
       -latest_visit_year, -service_part) 

#mutate(latest_visit=if_else(latest_visit_year>"2020", 1, 0)) 

rm(mp, MH, chat, CR, dcsi, ew, eve_v_pro, book,
   test_drive, estimate_cost, view_product_color, view_product_detail,
   view_product_gallery, view_product_list, view_promotion_notification,
   view_test_drive, sca, notif_book_pi, notif_book_pm, notif_book_spa,
   notif_v_pro, notif_v_spa, notif_vpi, notif_vpm)

UID<-smr %>% filter(keika_max>0) %>% select(UID)

##data_write
#data<- smr %>%
#  filter(keika_max>0) %>%
#  select(-UID) %>%
#  select(-START_date) %>%
#  mutate_all(., as.numeric) %>%
#  mutate_all(., ~replace(., is.na(.), 0)) 
#dd<-cbind(UID, data)
#write.csv(dd,  "data/output/dataset_all.csv",  row.names=F)


#--------
# 分析
#-------
#smr <-fread("data/output/dataset_all.csv")
data<- smr %>%
  filter(keika_max>0) %>%
  select(-UID) %>%
  select(-START_date,-START_year) %>%
  mutate_all(., as.numeric) %>%
  mutate_all(., ~replace(., is.na(.), 0)) 

PM2ov<-data$PM2ov
data<-data %>% select(-PM2ov)
PM2ov %>% table
nrow(data)

# 標準偏回帰係数（β）を求める
sc<-scale(data)
z <-  data.frame(sc) %>% cbind(PM2ov) # 得点を標準化
result <-glm(PM2ov~keika_max + total_buy + TIRE + BATTERY + visit_rate + 
               mp + MH_ID + chat + CR + total_satisfaction + 
               ew_num + coupon_use + SA_select + app_reserve_mean + estimate_cost + 
               view_product_detail + view_test_drive + notif_v_spa + notif_vpi + 
               notif_vpm + SA_cont + visit_rate:keika_max+SA_select:SA_cont,
             z, family=binomial())
model <- step(result)  # 関数stepで最もAICが低くなるモデルを確認
summary(model)  #選ばれたもっとも良いモデルとなる変数を使って回帰分析
