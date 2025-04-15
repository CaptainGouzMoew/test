library(data.table)
library(tidyverse)
library(openxlsx)
library(readxl)

#----------------------

file_0 <- ("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/4. 2016年以降データ")
file_1 <- ("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/4. 2016年以降データ/1. 221208データ/1_install_active_did_dcsi")
file_2 <- ("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/4. 2016年以降データ/1. 221208データ/2_install_active_not_did_dcsi")
file_3 <- ("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/4. 2016年以降データ/1. 221208データ/3_install_inactive_not_did_dcsi")
file_4 <- ("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/4. 2016年以降データ/1. 221208データ/4_not_install_did_dcsi")
file_5 <- ("D:/UserArea/J0116191/OneDrive - Honda/2_CF本部/4. 2016年以降データ/1. 221208データ/5_not_install_not_did_dcsi")

#service
service_1<-fread(paste(file_1, "/install_active_did_dcsi_service.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=1)
service_2<-fread(paste(file_2, "/install_active_not_did_dcsi_service.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=2)
service_3<-fread(paste(file_3, "/install_inactive_not_did_dcsi_service.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=3)
service_4<-fread(paste(file_4, "/not_install_did_dcsi_service.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=4)
service_5<-fread(paste(file_5, "/not_install_not_did_dcsi_service.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=5)
service<-bind_rows(service_1, service_2, service_3, service_4, service_5) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(service, "data/tmp/service.csv",row.names=F)
rm(service_1, service_2, service_3, service_4, service_5)

#sale
sale_1<-fread(paste(file_1, "/install_active_did_dcsi_sale.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=1)
sale_2<-fread(paste(file_2, "/install_active_not_did_dcsi_sale.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=2)
sale_3<-fread(paste(file_3, "/install_inactive_not_did_dcsi_sale.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=3)
sale_4<-fread(paste(file_4, "/not_install_did_dcsi_sale.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=4)
sale_5<-fread(paste(file_5, "/not_install_not_did_dcsi_sale.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=5)
sale<-bind_rows(sale_1, sale_2,sale_3, sale_4, sale_5) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(sale, "data/tmp/sale.csv",row.names=F)
rm(sale_1, sale_2,sale_3, sale_4, sale_5)

#MyHonda
MH_1<-fread(paste(file_1, "/install_active_did_dcsi_myhonda.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=1)
MH_2<-fread(paste(file_2, "/install_active_not_did_dcsi_myhonda.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=2)
MH_3<-fread(paste(file_3, "/install_inactive_not_did_dcsi_myhonda.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=3)
MH<-bind_rows(MH_1, MH_2, MH_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(MH, "data/tmp/MH.csv",row.names=F)
rm(MH_1, MH_2, MH_3)

#DCSI
DCSI_1<-fread(paste(file_1, "/install_active_did_dcsi_dcsi.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=1)
DCSI_4<-fread(paste(file_4, "/not_install_did_dcsi_dcsi.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=4)
DCSI<-bind_rows(DCSI_1, DCSI_4) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(DCSI, "data/tmp/DCSI.csv",row.names=F)
rm(DCSI_1, DCSI_4)

#complain
comp_1<-fread(paste(file_1, "/install_active_did_dcsi_complain.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=1)
comp_2<-fread(paste(file_2, "/install_active_not_did_dcsi_complain.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=2)
comp_3<-fread(paste(file_3, "/install_inactive_not_did_dcsi_complain.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=3)
comp_4<-fread(paste(file_4, "/not_install_did_dcsi_complain.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=4)
comp_5<-fread(paste(file_5, "/not_install_not_did_dcsi_complain.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=5)
comp<-bind_rows(comp_1, comp_2, comp_3, comp_4, comp_5) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(comp, "data/tmp/comp.csv",row.names=F)
rm(comp_1, comp_2, comp_3, comp_4, comp_5)

#ew:延長保証（Extended Warranty）
###price内に","が入っている場合があるので置換して除く
###Chrとdoubleの場合があるのでintに統一
ew_1<-fread(paste(file_1, "/install_active_did_dcsi_ew.csv", sep=""), encoding="UTF-8") %>%
  mutate(`Price (HVN)`=as.integer(str_replace_all(`Price (HVN)`, ",",""))) %>% mutate(Cust_group=1)
ew_2<-fread(paste(file_2, "/install_active_not_did_dcsi_ew.csv", sep=""), encoding="UTF-8") %>%
  mutate(`Price (HVN)`=as.integer(str_replace_all(`Price (HVN)`, ",",""))) %>% mutate(Cust_group=2)
ew_3<-fread(paste(file_3, "/install_inactive_not_did_dcsi_ew.csv", sep=""), encoding="UTF-8") %>%
  mutate(`Price (HVN)`=as.integer(str_replace_all(`Price (HVN)`, ",",""))) %>% mutate(Cust_group=3)
ew_4<-fread(paste(file_4, "/not_install_did_dcsi_ew.csv", sep=""), encoding="UTF-8") %>%
  mutate(`Price (HVN)`=as.integer(str_replace_all(`Price (HVN)`, ",",""))) %>% mutate(Cust_group=4)
ew_5<-fread(paste(file_5, "/not_install_not_did_dcsi_ew.csv", sep=""), encoding="UTF-8") %>%
  mutate(`Price (HVN)`=as.integer(str_replace_all(`Price (HVN)`, ",",""))) %>% mutate(Cust_group=5)
ew<-bind_rows(ew_1, ew_2,ew_3, ew_4, ew_5) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(ew, "data/tmp/ew.csv",row.names=F)
rm(ew_1, ew_2, ew_3, ew_4, ew_5)

#mp:メンテナンスパック

mp_1<-fread(paste(file_1, "/install_active_did_dcsi_mp.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=1)
mp_2<-fread(paste(file_2, "/install_active_not_did_dcsi_mp.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=2)
mp_3<-fread(paste(file_3, "/install_inactive_not_did_dcsi_mp.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=3)
mp_4<-fread(paste(file_4, "/not_install_did_dcsi_mp.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=4)
mp_5<-fread(paste(file_5, "/not_install_not_did_dcsi_mp.csv", sep=""), encoding="UTF-8") %>% mutate(Cust_group=5)

#ベトナム語の列名を変更
cname<-c("V1", "Month", "DLR", "Count", "DLR.1",
         "Model","Ngay ban_tang PM package","Ngay dang ky Warranty Date",
         "Km","New Car","Servicecar","2Cap","4Cap","Khac",
         "Lan 1","Lan 2","Lan 3","Lan 4","Lan 5","Lan 6",
         "Khac.1", "Gia ban", "Ghi chu","customer_index","Cust_group")
colnames(mp_1)<-cname
colnames(mp_2)<-cname
colnames(mp_3)<-cname
colnames(mp_4)<-cname
colnames(mp_5)<-cname

###Chrとdouble/intの場合があるのでChrに統一
list<-c("New Car","Servicecar","2Cap","4Cap","Khac")
mp_1<-mp_1 %>% mutate_at(vars(`Count`,`New Car`,`Servicecar`,`2Cap`,`4Cap`,`Khac`),
                         ~if_else(is.na(.), "", as.character(.)))
mp_2<-mp_2 %>% mutate_at(vars(`Count`,`New Car`,`Servicecar`,`2Cap`,`4Cap`,`Khac`),
                         ~if_else(is.na(.), "", as.character(.)))
mp_3<-mp_3 %>% mutate_at(vars(`Count`,`New Car`,`Servicecar`,`2Cap`,`4Cap`,`Khac`),
                         ~if_else(is.na(.), "", as.character(.)))
mp_4<-mp_4 %>% mutate_at(vars(`Count`,`New Car`,`Servicecar`,`2Cap`,`4Cap`,`Khac`),
                         ~if_else(is.na(.), "", as.character(.)))
mp_5<-mp_5 %>% mutate_at(vars(`Count`,`New Car`,`Servicecar`,`2Cap`,`4Cap`,`Khac`),
                         ~if_else(is.na(.), "", as.character(.)))
mp<-bind_rows(mp_1, mp_2, mp_3, mp_4, mp_5) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(mp, "data/tmp/mp.csv",row.names=F)
rm(mp_1, mp_2, mp_3, mp_4, mp_5)

#booking
book_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_booking_service.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=1)
book_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_booking_service.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=2)
book_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_booking_service.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=3)
book<-bind_rows(book_1, book_2, book_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(book, "data/tmp/book.csv",row.names=F)
rm(book_1, book_2, book_3)


#event:view_promotion_notification
event_V_promo_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=1)
event_V_promo_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=2)
event_V_promo_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=3)
event_V_promo<-bind_rows(event_V_promo_1, event_V_promo_2, event_V_promo_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(event_V_promo, "data/tmp/event_v_promo.csv",row.names=F)
rm(event_V_promo_1, event_V_promo_2, event_V_promo_3)

#event:use_promotion
use_promotion_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="use_promotion")) %>% mutate(Cust_group=1)
use_promotion_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="use_promotion")) %>% mutate(Cust_group=2)
use_promotion_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="use_promotion")) %>% mutate(Cust_group=3)
use_promotion<- use_promotion_1 %>%#bind_rows(use_promotion_1, use_promotion_2, use_promotion_3) %>%
  mutate(UID=paste(Cust_group, customer_index=cusstomer_index, sep="_")) %>%
  select(UID, event_date, promotion_id)
write.csv(use_promotion, "data/tmp/use_promotion.csv",row.names=F)
rm(use_promotion_1, use_promotion_2, use_promotion_3)


#event:test_drive
test_drive_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="test_drive")) %>% mutate(Cust_group=1)
test_drive_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="test_drive")) %>% mutate(Cust_group=2)
test_drive_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="test_drive")) %>% mutate(Cust_group=3)
test_drive<- bind_rows(test_drive_1, test_drive_2, test_drive_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(test_drive, "data/tmp/test_drive.csv",row.names=F)
rm(test_drive_1, test_drive_2, test_drive_3)

#event:view_test_drive
view_test_drive_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_test_drive")) %>% mutate(Cust_group=1)
view_test_drive_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_test_drive")) %>% mutate(Cust_group=2)
view_test_drive_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_test_drive")) %>% mutate(Cust_group=3)
view_test_drive<- bind_rows(view_test_drive_1, view_test_drive_2, view_test_drive_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(view_test_drive, "data/tmp/view_test_drive.csv",row.names=F)
rm(view_test_drive_1, view_test_drive_2, view_test_drive_3)

#event:compare_product_am
compare_product_am_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="compare_product_am")) %>% mutate(Cust_group=1)
compare_product_am_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="compare_product_am")) %>% mutate(Cust_group=2)
compare_product_am_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="compare_product_am")) %>% mutate(Cust_group=3)
compare_product_am<- bind_rows(compare_product_am_1, compare_product_am_2, compare_product_am_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(compare_product_am, "data/tmp/compare_product_am.csv",row.names=F)
rm(compare_product_am_1, compare_product_am_2, compare_product_am_3)

#event:estimate_cost
estimate_cost_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="estimate_cost")) %>% mutate(Cust_group=1)
estimate_cost_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="estimate_cost")) %>% mutate(Cust_group=2)
estimate_cost_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="estimate_cost")) %>% mutate(Cust_group=3)
estimate_cost<- bind_rows(estimate_cost_1, estimate_cost_2, estimate_cost_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(estimate_cost, "data/tmp/estimate_cost.csv",row.names=F)
rm(estimate_cost_1, estimate_cost_2, estimate_cost_3)

#event:view_product_color
view_product_color_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_color")) %>% mutate(Cust_group=1)
view_product_color_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_color")) %>% mutate(Cust_group=2)
view_product_color_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_color")) %>% mutate(Cust_group=3)
view_product_color<- bind_rows(view_product_color_1, view_product_color_2, view_product_color_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(view_product_color, "data/tmp/view_product_color.csv",row.names=F)
rm(view_product_color_1, view_product_color_2, view_product_color_3)

#event:view_product_detail_am
view_product_detail_am_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_detail_am")) %>% mutate(Cust_group=1)
view_product_detail_am_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_detail_am")) %>% mutate(Cust_group=2)
view_product_detail_am_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_detail_am")) %>% mutate(Cust_group=3)
view_product_detail_am<- bind_rows(view_product_detail_am_1, view_product_detail_am_2, view_product_detail_am_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(view_product_detail_am, "data/tmp/view_product_detail_am.csv",row.names=F)
rm(view_product_detail_am_1, view_product_detail_am_2, view_product_detail_am_3)

#event:view_product_gallery
view_product_gallery_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_gallery")) %>% mutate(Cust_group=1)
view_product_gallery_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_gallery")) %>% mutate(Cust_group=2)
view_product_gallery_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_gallery")) %>% mutate(Cust_group=3)
view_product_gallery<- bind_rows(view_product_gallery_1, view_product_gallery_2, view_product_gallery_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(view_product_gallery, "data/tmp/view_product_gallery.csv",row.names=F)
rm(view_product_gallery_1, view_product_gallery_2, view_product_gallery_3)

#event:view_product_list
view_product_list_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_list")) %>% mutate(Cust_group=1)
view_product_list_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_list")) %>% mutate(Cust_group=2)
view_product_list_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_product_list")) %>% mutate(Cust_group=3)
view_product_list<- bind_rows(view_product_list_1, view_product_list_2, view_product_list_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(view_product_list, "data/tmp/view_product_list.csv",row.names=F)
rm(view_product_list_1, view_product_list_2, view_product_list_3)

#event:view_promotion_notification
view_promotion_notification_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=1)
view_promotion_notification_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=2)
view_promotion_notification_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=3)
view_promotion_notification<- bind_rows(view_promotion_notification_1, view_promotion_notification_2, view_promotion_notification_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(view_promotion_notification, "data/tmp/view_promotion_notification.csv",row.names=F)
rm(view_promotion_notification_1, view_promotion_notification_2, view_promotion_notification_3)

#notification:view_promotion_notification
notif_v_pro_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=1)
notif_v_pro_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=2)
notif_v_pro_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_event_tracking.xlsx", sep=""), sheet="view_promotion_notification")) %>% mutate(Cust_group=3) 
notif_v_pro<-bind_rows(notif_v_pro_1, notif_v_pro_2, notif_v_pro_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(notif_v_pro, "data/tmp/notif_v_pro.csv",row.names=F)
rm(notif_v_pro_1, notif_v_pro_2, notif_v_pro_3)


#notification:view_pi_remind_notification 
notif_vpi_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_pi_remind_notification")) %>% mutate(Cust_group=1)
notif_vpi_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_pi_remind_notification")) %>% mutate(Cust_group=2)
notif_vpi_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_pi_remind_notification")) %>% mutate(Cust_group=3)
notif_vpi<-bind_rows(notif_vpi_1, notif_vpi_2, notif_vpi_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(notif_vpi, "data/tmp/notif_vpi.csv",row.names=F)
rm(notif_vpi_1, notif_vpi_2, notif_vpi_3)

#notification:view_pm_remind_notification
notif_vpm_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_pm_remind_notification")) %>% mutate(Cust_group=1)
notif_vpm_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_pm_remind_notification")) %>% mutate(Cust_group=2)
notif_vpm_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_pm_remind_notification")) %>% mutate(Cust_group=3)
notif_vpm<-bind_rows(notif_vpm_1, notif_vpm_2, notif_vpm_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(notif_vpm, "data/tmp/notif_vpm.csv",row.names=F)
rm(notif_vpm_1, notif_vpm_2, notif_vpm_3)

#notification:booking_pi_remind_notification
notif_book_pi_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_pi_remind_notification")) %>% mutate(Cust_group=1)
notif_book_pi_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_pi_remind_notification")) %>% mutate(Cust_group=2)
notif_book_pi_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_pi_remind_notification")) %>% mutate(Cust_group=3) %>% select(-vin)
notif_book_pi<-bind_rows(notif_book_pi_1, notif_book_pi_2) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(notif_book_pi, "data/tmp/notif_book_pi.csv",row.names=F)
rm(notif_book_pi_1, notif_book_pi_2, notif_book_pi_3)

#notification:booking_pi_remind_notification
notif_book_pm_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_pm_service")) %>% mutate(Cust_group=1)
notif_book_pm_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_pm_service")) %>% mutate(Cust_group=2)
notif_book_pm_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_pm_service")) %>% mutate(Cust_group=3) 
notif_book_pm<-bind_rows(notif_book_pm_1, notif_book_pm_2) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(notif_book_pm, "data/tmp/notif_book_pm.csv",row.names=F)
rm(notif_book_pm_1, notif_book_pm_2, notif_book_pm_3)


#notification:booking_sparepart
notif_book_spa_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_sparepart")) %>% mutate(Cust_group=1)
notif_book_spa_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_sparepart")) %>% mutate(Cust_group=2) %>% select(-vin)
notif_book_spa_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="booking_sparepart")) %>% mutate(Cust_group=3) 
notif_book_spa<-bind_rows(notif_book_spa_1, notif_book_spa_2, notif_book_spa_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(notif_book_spa, "data/tmp/notif_book_spa.csv",row.names=F)
rm(notif_book_spa_1, notif_book_spa_2, notif_book_spa_3)


#notification:view_sparepart_notification
notif_v_spa_1<-data.frame(read.xlsx(paste(file_1, "/install_active_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_sparepart_notification")) %>% mutate(Cust_group=1)%>% select(-uid)
notif_v_spa_2<-data.frame(read.xlsx(paste(file_2, "/install_active_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_sparepart_notification")) %>% mutate(Cust_group=2)%>% select(-uid)
notif_v_spa_3<-data.frame(read.xlsx(paste(file_3, "/install_inactive_not_did_dcsi_notification_tracking.xlsx", sep=""), sheet="view_sparepart_notification")) %>% mutate(Cust_group=3) 
notif_v_spa<-bind_rows(notif_v_spa_1, notif_v_spa_2, notif_v_spa_3) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(notif_v_spa, "data/tmp/notif_v_spa.csv",row.names=F)
rm(notif_v_spa_1, notif_v_spa_2, notif_v_spa_3)


#SCA
SCA_1<-data.frame(read.xlsx(paste(file_0, "/4. 230202データ/data_sca/data_sca/install_active_did_dcsi_sca2.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=1)
SCA_2<-data.frame(read.xlsx(paste(file_0, "/4. 230202データ/data_sca/data_sca/install_active_not_did_dcsi_sca2.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=2)
SCA_3<-data.frame(read.xlsx(paste(file_0, "/4. 230202データ/data_sca/data_sca/install_inactive_not_did_dcsi_sca2.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=3)
SCA_4<-data.frame(read.xlsx(paste(file_0, "/4. 230202データ/data_sca/data_sca/not_install_did_dcsi_sca2.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=4)
SCA_5<-data.frame(read.xlsx(paste(file_0, "/4. 230202データ/data_sca/data_sca/not_install_not_did_dcsi_sca2.xlsx", sep=""), sheet="Sheet1")) %>% mutate(Cust_group=5)
SCA<-bind_rows(SCA_1, SCA_2, SCA_3, SCA_4, SCA_5) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(SCA, "data/tmp/SCA.csv",row.names=F)
rm(SCA_1, SCA_2, SCA_3, SCA_4, SCA_5)


#チャットボット
chat_1_20<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_active_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2020")) %>% mutate(year="2020", Cust_group=1)
chat_1_21<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_active_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2021")) %>% mutate(year="2021", Cust_group=1)
chat_1_22<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_active_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2022")) %>% mutate(year="2022", Cust_group=1)
chat_2_20<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_active_not_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2020")) %>% mutate(year="2020", Cust_group=2)
chat_2_21<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_active_not_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2021")) %>% mutate(year="2021", Cust_group=2)
chat_2_22<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_active_not_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2022")) %>% mutate(year="2022", Cust_group=2)
chat_3_20<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_inactive_not_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2020")) %>% mutate(year="2020", Cust_group=3)
chat_3_21<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_inactive_not_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2021")) %>% mutate(year="2021", Cust_group=3)
chat_3_22<-data.frame(read.xlsx(paste(file_0, "/3. 230110データ(チャットボット)/install_inactive_not_did_dcsi_chatbot (Eng).xlsx", sep=""), sheet=" CB 2022")) %>% mutate(year="2022", Cust_group=3)
chat<-bind_rows(chat_1_20, chat_1_21, chat_1_22, chat_2_20, chat_2_21, chat_2_22, chat_3_20, chat_3_21, chat_3_22) %>%
  mutate(UID=paste(Cust_group, customer_index, sep="_"))
write.csv(chat, "data/tmp/chat.csv",row.names=F)
rm(chat_1_20, chat_1_21, chat_1_22, chat_2_20, chat_2_21, chat_2_22, chat_3_20, chat_3_21, chat_3_22)
