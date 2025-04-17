import pandas as pd
pd.options.mode.chained_assignment = None
from unidecode import unidecode
import numpy as np
import re
import importlib

# WTF
def clean_address_old_data(x, district, city):
    x = unidecode(x)
    x = x.lower()
    
    #x = clean_city(x)
    #x = re.sub(r'[^a-zA-Z0-9]', '', x)
    x = clean_city(remove_special_characters(x)).replace(' ','')
    x = x.strip()

    clean_district_check = False
    clean_city_check = False
    
    if city != 'other' and x.endswith(city):
        x = x[:-len(city)]
        clean_city_check = True
        if district != 'other' and x.endswith(district):
            x = x[:-len(district)]
            clean_district_check = True

    if clean_city_check:
        arc_city = {'hanoi' : 'hn',  'hagiang' : 'hg', 'caobang' : 'cb', 'backan' : 'bk', 'tuyenquang' : 'tq', 'laocai' : 'lc', 'dienbien' : 'db', 'laichau' : 'lc', 'sonla' : 'sl', 'yenbai' : 'yb', 'hoabinh' : 'hb', 'thainguyen' : 'tn', 'langson' : 'ls', 'quangninh' : 'qn', 'bacgiang' : 'bg', 'phutho' : 'pt', 'vinhphuc' : 'vp', 'bacninh' : 'bn', 'haiduong' : 'hd', 'haiphong' : 'hp', 'hungyen' : 'hy', 'thaibinh' : 'tb', 'hanam' : 'hna', 'namdinh' : 'nd', 'ninhbinh' : 'nb', 'thanhhoa' : 'th', 'nghean' : 'na', 'hatinh' : 'ht', 'quangbinh' : 'qb', 'quangtri' : 'qt', 'thuathienhue' : 'tth', 'danang' : 'dn', 'quangnam' : 'qn', 'quangngai' : 'qn', 'binhdinh' : 'bd', 'phuyen' : 'py', 'khanhhoa' : 'kh', 'ninhthuan' : 'nt', 'binhthuan' : 'bt', 'kontum' : 'kt', 'gialai' : 'gl', 'daklak' : 'dl', 'daknong' : 'dkn', 'lamdong' : 'ld', 'binhphuoc' : 'bp', 'tayninh' : 'tn', 'binhduong' : 'bd', 'dongnai' : 'don', 'hochiminh' : 'hcm', 'longan' : 'la', 'tiengiang' : 'tg', 'bentre' : 'bt', 'travinh' : 'tv', 'vinhlong' : 'vl', 'dongthap' : 'dt', 'angiang' : 'ag', 'kiengiang' : 'kg', 'cantho' : 'ct', 'haugiang' : 'hg', 'soctrang' : 'st', 'baclieu' : 'bl', 'camau' : 'cm', 'bariavungtau' : 'brvt'}
        x = x.replace(arc_city[city], '')
        x = x.replace(city, '')

    if clean_district_check:
        arc_district = {'badinh' : 'bd',  'hoankiem' : 'hk', 'tayho' : 'th', 'longbien' : 'lb', 'caugiay' : 'cg', 'dongda' : 'dd', 'haibatrung' : 'hbt', 'hoangmai' : 'hm', 'thanhxuan' : 'tx', 'socson' : 'ss', 'donganh' : 'da', 'gialam' : 'gl', 'namtuliem' : 'ntl', 'thanhtri' : 'tt', 'bactuliem' : 'btl', 'hagiang' : 'hg', 'dongvan' : 'dv', 'meovac' : 'mv', 'yenminh' : 'ym', 'quanba' : 'qb', 'vixuyen' : 'vx', 'bacme' : 'bm', 'hoangsuphi' : 'hsp', 'xinman' : 'xm', 'bacquang' : 'bq', 'quangbinh' : 'qb', 'caobang' : 'cb', 'baolam' : 'bl', 'baolac' : 'bl', 'haquang' : 'hq', 'trungkhanh' : 'tk', 'halang' : 'hl', 'quanghoa' : 'qh', 'hoaan' : 'ha', 'nguyenbinh' : 'nb', 'thachan' : 'ta', 'backan' : 'bk', 'pacnam' : 'pn', 'babe' : 'bb', 'nganson' : 'ns', 'bachthong' : 'bt', 'chodon' : 'cd', 'chomoi' : 'cm', 'nari' : 'nr', 'tuyenquang' : 'tq', 'lambinh' : 'lb', 'nahang' : 'nh', 'chiemhoa' : 'ch', 'hamyen' : 'hy', 'yenson' : 'ys', 'sonduong' : 'sd', 'laocai' : 'lc', 'batxat' : 'bx', 'muongkhuong' : 'mk', 'simacai' : 'sm', 'bacha' : 'bh', 'baothang' : 'bt', 'baoyen' : 'by', 'sapa' : 'sp', 'vanban' : 'vb', 'dienbienphu' : 'db', 'muonglay' : 'ml', 'muongnhe' : 'mn', 'muongcha' : 'mc', 'tuachua' : 'tc', 'tuangiao' : 'tg', 'dienbien' : 'db', 'dienbiendong' : 'dbd', 'muongang' : 'ma', 'nampo' : 'np', 'laichau' : 'lc', 'tamduong' : 'td', 'muongte' : 'mt', 'sinho' : 'sh', 'phongtho' : 'pt', 'thanuyen' : 'tu', 'tanuyen' : 'tu', 'namnhun' : 'nn', 'sonla' : 'sl', 'quynhnhai' : 'qn', 'thuanchau' : 'tc', 'muongla' : 'ml', 'bacyen' : 'by', 'phuyen' : 'py', 'mocchau' : 'mc', 'yenchau' : 'yc', 'maison' : 'ms', 'songma' : 'sm', 'sopcop' : 'sc', 'vanho' : 'vh', 'yenbai' : 'yb', 'nghialo' : 'nl', 'lucyen' : 'ly', 'vanyen' : 'vy', 'mucangchai' : 'mcc', 'tranyen' : 'ty', 'tramtau' : 'tt', 'vanchan' : 'vc', 'yenbinh' : 'yb', 'hoabinh' : 'hb', 'dabac' : 'db', 'luongson' : 'ls', 'kimboi' : 'kb', 'caophong' : 'cp', 'tanlac' : 'tl', 'maichau' : 'mc', 'lacson' : 'ls', 'yenthuy' : 'yt', 'lacthuy' : 'lt', 'thainguyen' : 'tn', 'songcong' : 'sc', 'dinhhoa' : 'dh', 'phuluong' : 'pl', 'donghy' : 'dh', 'vonhai' : 'vn', 'daitu' : 'dt', 'phoyen' : 'py', 'phubinh' : 'pb', 'langson' : 'ls', 'trangdinh' : 'td', 'binhgia' : 'bg', 'vanlang' : 'vl', 'caoloc' : 'cl', 'vanquan' : 'vq', 'bacson' : 'bs', 'huulung' : 'hl', 'chilang' : 'cl', 'locbinh' : 'lb', 'dinhlap' : 'dl', 'halong' : 'hl', 'mongcai' : 'mc', 'campha' : 'cp', 'uongbi' : 'ub', 'binhlieu' : 'bl', 'tienyen' : 'ty', 'damha' : 'dh', 'haiha' : 'hh', 'bache' : 'bc', 'vandon' : 'vd', 'dongtrieu' : 'dt', 'quangyen' : 'qy', 'coto' : 'ct', 'bacgiang' : 'bg', 'yenthe' : 'yt', 'tanyen' : 'ty', 'langgiang' : 'lg', 'lucnam' : 'ln', 'lucngan' : 'ln', 'sondong' : 'sd', 'yendung' : 'yd', 'vietyen' : 'vy', 'hiephoa' : 'hh', 'viettri' : 'vt', 'phutho' : 'pt', 'doanhung' : 'dh', 'hahoa' : 'hh', 'thanhba' : 'tb', 'phuninh' : 'pn', 'yenlap' : 'yl', 'camkhe' : 'ck', 'tamnong' : 'tn', 'lamthao' : 'lt', 'thanhson' : 'ts', 'thanhthuy' : 'tt', 'tanson' : 'ts', 'vinhyen' : 'vy', 'phucyen' : 'py', 'lapthach' : 'lt', 'tamduong' : 'td', 'tamdao' : 'td', 'binhxuyen' : 'bx', 'melinh' : 'ml', 'yenlac' : 'yl', 'vinhtuong' : 'vt', 'songlo' : 'sl', 'bacninh' : 'bn', 'yenphong' : 'yp', 'quevo' : 'qv', 'tiendu' : 'td', 'tuson' : 'ts', 'thuanthanh' : 'tt', 'giabinh' : 'gb', 'luongtai' : 'lt', 'hadong' : 'hd', 'sontay' : 'st', 'bavi' : 'bv', 'phuctho' : 'pt', 'danphuong' : 'dp', 'hoaiduc' : 'hd', 'quocoai' : 'qo', 'thachthat' : 'tt', 'chuongmy' : 'cm', 'thanhoai' : 'to', 'thuongtin' : 'tt', 'phuxuyen' : 'px', 'unghoa' : 'uh', 'myduc' : 'md', 'haiduong' : 'hd', 'chilinh' : 'cl', 'namsach' : 'ns', 'kinhmon' : 'km', 'kimthanh' : 'kt', 'thanhha' : 'th', 'camgiang' : 'cg', 'binhgiang' : 'bg', 'gialoc' : 'gl', 'tuky' : 'tk', 'ninhgiang' : 'ng', 'thanhmien' : 'tm', 'hongbang' : 'hb', 'ngoquyen' : 'nq', 'lechan' : 'lc', 'haian' : 'ha', 'kienan' : 'ka', 'doson' : 'ds', 'duongkinh' : 'dk', 'thuynguyen' : 'tn', 'anduong' : 'ad', 'anlao' : 'al', 'kienthuy' : 'kt', 'tienlang' : 'tl', 'vinhbao' : 'vb', 'cathai' : 'ch', 'hungyen' : 'hy', 'vanlam' : 'vl', 'vangiang' : 'vg', 'yenmy' : 'ym', 'myhao' : 'mh', 'anthi' : 'at', 'khoaichau' : 'kc', 'kimdong' : 'kd', 'tienlu' : 'tl', 'phucu' : 'pc', 'thaibinh' : 'tb', 'quynhphu' : 'qp', 'hungha' : 'hh', 'donghung' : 'dh', 'thaithuy' : 'tt', 'tienhai' : 'th', 'kienxuong' : 'kx', 'vuthu' : 'vt', 'phuly' : 'pl', 'duytien' : 'dt', 'kimbang' : 'kb', 'thanhliem' : 'tl', 'binhluc' : 'bl', 'lynhan' : 'ln', 'namdinh' : 'nd', 'myloc' : 'ml', 'vuban' : 'vb', 'yyen' : 'yy', 'nghiahung' : 'nh', 'namtruc' : 'nt', 'trucninh' : 'tn', 'xuantruong' : 'xt', 'giaothuy' : 'gt', 'haihau' : 'hh', 'ninhbinh' : 'nb', 'tamdiep' : 'td', 'nhoquan' : 'nq', 'giavien' : 'gv', 'hoalu' : 'hl', 'yenkhanh' : 'yk', 'kimson' : 'ks', 'yenmo' : 'ym', 'thanhhoa' : 'th', 'bimson' : 'bs', 'samson' : 'ss', 'muonglat' : 'ml', 'quanhoa' : 'qh', 'bathuoc' : 'bt', 'quanson' : 'qs', 'langchanh' : 'lc', 'ngoclac' : 'nl', 'camthuy' : 'ct', 'thachthanh' : 'tt', 'hatrung' : 'ht', 'vinhloc' : 'vl', 'yendinh' : 'yd', 'thoxuan' : 'tx', 'thuongxuan' : 'tx', 'trieuson' : 'ts', 'thieuhoa' : 'th', 'hoanghoa' : 'hh', 'hauloc' : 'hl', 'ngason' : 'ns', 'nhuxuan' : 'nx', 'nhuthanh' : 'nt', 'nongcong' : 'nc', 'dongson' : 'ds', 'quangxuong' : 'qx', 'nghison' : 'ns', 'vinh' : 'vv', 'cualo' : 'cl', 'thaihoa' : 'th', 'quephong' : 'qp', 'quychau' : 'qc', 'kyson' : 'ks', 'tuongduong' : 'td', 'nghiadan' : 'nd', 'quyhop' : 'qh', 'quynhluu' : 'ql', 'concuong' : 'cc', 'tanky' : 'tk', 'anhson' : 'as', 'dienchau' : 'dc', 'yenthanh' : 'yt', 'doluong' : 'dl', 'thanhchuong' : 'tc', 'nghiloc' : 'nl', 'namdan' : 'nd', 'hungnguyen' : 'hn', 'hoangmai' : 'hm', 'hatinh' : 'ht', 'honglinh' : 'hl', 'huongson' : 'hs', 'ductho' : 'dt', 'vuquang' : 'vq', 'nghixuan' : 'nx', 'canloc' : 'cl', 'huongkhe' : 'hk', 'thachha' : 'th', 'camxuyen' : 'cx', 'kyanh' : 'ka', 'locha' : 'lh', 'kyanh' : 'ka', 'donghoi' : 'dh', 'minhhoa' : 'mh', 'tuyenhoa' : 'th', 'quangtrach' : 'qt', 'botrach' : 'bt', 'quangninh' : 'qn', 'lethuy' : 'lt', 'badon' : 'bd', 'dongha' : 'dh', 'quangtri' : 'qt', 'vinhlinh' : 'vl', 'huonghoa' : 'hh', 'giolinh' : 'gl', 'dakrong' : 'dk', 'camlo' : 'cl', 'trieuphong' : 'tp', 'hailang' : 'hl', 'hue' : 'hh', 'phongdien' : 'pd', 'quangdien' : 'qd', 'phuvang' : 'pv', 'huongthuy' : 'ht', 'huongtra' : 'ht', 'aluoi' : 'al', 'phuloc' : 'pl', 'namdong' : 'nd', 'lienchieu' : 'lc', 'thanhkhe' : 'tk', 'haichau' : 'hc', 'sontra' : 'st', 'nguhanhson' : 'nhs', 'camle' : 'cl', 'hoavang' : 'hv', 'tamky' : 'tk', 'hoian' : 'ha', 'taygiang' : 'tg', 'donggiang' : 'dg', 'dailoc' : 'dl', 'dienban' : 'db', 'duyxuyen' : 'dx', 'queson' : 'qs', 'namgiang' : 'ng', 'phuocson' : 'ps', 'hiepduc' : 'hd', 'thangbinh' : 'tb', 'tienphuoc' : 'tp', 'bactramy' : 'bt', 'namtramy' : 'nt', 'nuithanh' : 'nt', 'phuninh' : 'pn', 'nongson' : 'ns', 'quangngai' : 'qn', 'binhson' : 'bs', 'trabong' : 'tb', 'sontinh' : 'st', 'tunghia' : 'tn', 'sonha' : 'sh', 'sontay' : 'st', 'minhlong' : 'ml', 'nghiahanh' : 'nh', 'moduc' : 'md', 'ducpho' : 'dp', 'bato' : 'bt', 'quynhon' : 'qn', 'anlao' : 'al', 'hoainhon' : 'hn', 'hoaian' : 'ha', 'phumy' : 'pm', 'vinhthanh' : 'vt', 'tayson' : 'ts', 'phucat' : 'pc', 'annhon' : 'an', 'tuyphuoc' : 'tp', 'vancanh' : 'vc', 'tuyhoa' : 'th', 'songcau' : 'sc', 'dongxuan' : 'dx', 'tuyan' : 'ta', 'sonhoa' : 'sh', 'songhinh' : 'sh', 'tayhoa' : 'th', 'phuhoa' : 'ph', 'donghoa' : 'dh', 'nhatrang' : 'nt', 'camranh' : 'cr', 'camlam' : 'cl', 'vanninh' : 'vn', 'ninhhoa' : 'nh', 'khanhvinh' : 'kv', 'dienkhanh' : 'dk', 'khanhson' : 'ks', 'truongsa' : 'ts', 'phanrang-thapcham' : 'pr', 'bacai' : 'ba', 'ninhson' : 'ns', 'ninhhai' : 'nh', 'ninhphuoc' : 'np', 'thuanbac' : 'tb', 'thuannam' : 'tn', 'phanthiet' : 'pt', 'lagi' : 'lg', 'tuyphong' : 'tp', 'bacbinh' : 'bb', 'hamthuanbac' : 'htb', 'hamthuannam' : 'htn', 'tanhlinh' : 'tl', 'duclinh' : 'dl', 'hamtan' : 'ht', 'phuqui' : 'pq', 'kontum' : 'kt', 'dakglei' : 'dg', 'ngochoi' : 'nh', 'dakto' : 'dt', 'konplong' : 'kp', 'konray' : 'kr', 'dakha' : 'dh', 'sathay' : 'st', 'tumorong' : 'tmr', 'iahdrai' : 'ih', 'pleiku' : 'pp', 'ankhe' : 'ak', 'ayunpa' : 'ap', 'kbang' : 'kk', 'dakdoa' : 'dd', 'chupah' : 'cp', 'iagrai' : 'ig', 'mangyang' : 'my', 'kongchro' : 'kc', 'ducco' : 'dc', 'chuprong' : 'cp', 'chuse' : 'cs', 'dakpo' : 'dp', 'iapa' : 'ip', 'krongpa' : 'kp', 'phuthien' : 'pt', 'chupuh' : 'cp', 'buonmathuot' : 'bmt', 'buonho' : 'bh', 'eahleo' : 'eh', 'easup' : 'es', 'buondon' : 'bd', 'cumgar' : 'cm', 'krongbuk' : 'kb', 'krongnang' : 'kn', 'eakar' : 'ek', 'mdrak' : 'mm', 'krongbong' : 'kb', 'krongpac' : 'kp', 'krongana' : 'ka', 'lak' : 'll', 'cukuin' : 'ck', 'gianghia' : 'gn', 'dakglong' : 'dg', 'cujut' : 'cj', 'dakmil' : 'dm', 'krongno' : 'kn', 'daksong' : 'ds', 'dakrlap' : 'dr', 'tuyduc' : 'td', 'dalat' : 'dl', 'baoloc' : 'bl', 'damrong' : 'dr', 'lacduong' : 'ld', 'lamha' : 'lh', 'donduong' : 'dd', 'ductrong' : 'dt', 'dilinh' : 'dl', 'baolam' : 'bl', 'dahuoai' : 'dh', 'dateh' : 'dt', 'cattien' : 'ct', 'phuoclong' : 'pl', 'dongxoai' : 'dx', 'binhlong' : 'bl', 'bugiamap' : 'bg', 'locninh' : 'ln', 'budop' : 'bd', 'honquan' : 'hq', 'dongphu' : 'dp', 'budang' : 'bd', 'chonthanh' : 'ct', 'phurieng' : 'pr', 'tayninh' : 'tn', 'tanbien' : 'tb', 'tanchau' : 'tc', 'duongminhchau' : 'dmc', 'chauthanh' : 'ct', 'hoathanh' : 'ht', 'godau' : 'gd', 'bencau' : 'bc', 'trangbang' : 'tb', 'thudaumot' : 'tdm', 'baubang' : 'bb', 'dautieng' : 'dt', 'bencat' : 'bc', 'phugiao' : 'pg', 'tanuyen' : 'tu', 'dian' : 'da', 'thuanan' : 'ta', 'bactanuyen' : 'btu', 'bienhoa' : 'bh', 'longkhanh' : 'lk', 'tanphu' : 'tp', 'vinhcuu' : 'vc', 'dinhquan' : 'dq', 'trangbom' : 'tb', 'thongnhat' : 'tn', 'cammy' : 'cm', 'longthanh' : 'lt', 'xuanloc' : 'xl', 'nhontrach' : 'nt', 'vungtau' : 'vt', 'baria' : 'br', 'chauduc' : 'cd', 'xuyenmoc' : 'xm', 'longdien' : 'ld', 'datdo' : 'dd', 'phumy' : 'pm', '1' : '1', '12' : '12', 'govap' : 'gv', 'binhthanh' : 'bt', 'tanbinh' : 'tb', 'tanphu' : 'tp', 'phunhuan' : 'pn', 'thuduc' : 'td', '3' : '3', '10' : '10', '11' : '11', '4' : '4', '5' : '5', '6' : '6', '8' : '8', 'binhtan' : 'bt', '7' : '7', 'cuchi' : 'cc', 'hocmon' : 'hm', 'binhchanh' : 'bc', 'nhabe' : 'nb', 'cangio' : 'cg', 'tanan' : 'ta', 'kientuong' : 'kt', 'tanhung' : 'th', 'vinhhung' : 'vh', 'mochoa' : 'mh', 'tanthanh' : 'tt', 'thanhhoa' : 'th', 'duchue' : 'dh', 'duchoa' : 'dh', 'benluc' : 'bl', 'thuthua' : 'tt', 'tantru' : 'tt', 'canduoc' : 'cd', 'cangiuoc' : 'cg', 'chauthanh' : 'ct', 'mytho' : 'mt', 'gocong' : 'gc', 'cailay' : 'cl', 'tanphuoc' : 'tp', 'caibe' : 'cb', 'cailay' : 'cl', 'chauthanh' : 'ct', 'chogao' : 'cg', 'gocongtay' : 'gct', 'gocongdong' : 'gcd', 'tanphudong' : 'tpd', 'bentre' : 'bt', 'chauthanh' : 'ct', 'cholach' : 'cl', 'mocaynam' : 'mcn', 'giongtrom' : 'gt', 'binhdai' : 'bd', 'batri' : 'bt', 'thanhphu' : 'tp', 'mocaybac' : 'mcb', 'travinh' : 'tv', 'canglong' : 'cl', 'cauke' : 'ck', 'tieucan' : 'tc', 'chauthanh' : 'ct', 'caungang' : 'cn', 'tracu' : 'tc', 'duyenhai' : 'dh', 'duyenhai' : 'dh', 'vinhlong' : 'vl', 'longho' : 'lh', 'mangthit' : 'mt', 'vungliem' : 'vl', 'tambinh' : 'tb', 'binhminh' : 'bm', 'traon' : 'to', 'binhtan' : 'bt', 'caolanh' : 'cl', 'sadec' : 'sd', 'hongngu' : 'hn', 'tanhong' : 'th', 'hongngu' : 'hn', 'tamnong' : 'tn', 'thapmuoi' : 'tm', 'caolanh' : 'cl', 'thanhbinh' : 'tb', 'lapvo' : 'lv', 'laivung' : 'lv', 'chauthanh' : 'ct', 'longxuyen' : 'lx', 'chaudoc' : 'cd', 'anphu' : 'ap', 'tanchau' : 'tc', 'phutan' : 'pt', 'chauphu' : 'cp', 'tinhbien' : 'tb', 'triton' : 'tt', 'chauthanh' : 'ct', 'chomoi' : 'cm', 'thoaison' : 'ts', 'rachgia' : 'rg', 'hatien' : 'ht', 'kienluong' : 'kl', 'hondat' : 'hd', 'tanhiep' : 'th', 'chauthanh' : 'ct', 'giongrieng' : 'gr', 'goquao' : 'gq', 'anbien' : 'ab', 'anminh' : 'am', 'vinhthuan' : 'vt', 'phuquoc' : 'pq', 'kienhai' : 'kh', 'uminhthuong' : 'umt', 'giangthanh' : 'gt', 'ninhkieu' : 'nk', 'omon' : 'om', 'binhthuy' : 'bt', 'cairang' : 'cr', 'thotnot' : 'tn', 'vinhthanh' : 'vt', 'codo' : 'cd', 'phongdien' : 'pd', 'thoilai' : 'tl', 'vithanh' : 'vt', 'ngabay' : 'nb', 'chauthanha' : 'cta', 'chauthanh' : 'ctb', 'phunghiep' : 'ph', 'vithuy' : 'vt', 'longmy' : 'lm', 'longmy' : 'lm', 'soctrang' : 'st', 'chauthanh' : 'ct', 'kesach' : 'ks', 'mytu' : 'mt', 'culaodung' : 'cld', 'longphu' : 'lp', 'myxuyen' : 'mx', 'nganam' : 'nn', 'thanhtri' : 'tt', 'vinhchau' : 'vc', 'trande' : 'td', 'baclieu' : 'bl', 'hongdan' : 'hd', 'phuoclong' : 'pl', 'vinhloi' : 'vl', 'giarai' : 'gr', 'donghai' : 'dh', 'hoabinh' : 'hb', 'camau' : 'cm', 'uminh' : 'um', 'thoibinh' : 'tb', 'tranvanthoi' : 'tvt', 'cainuoc' : 'cn', 'damdoi' : 'dd', 'namcan' : 'nc', 'phutan' : 'pt', 'ngochien' : 'nh'}
        x = x.replace(arc_district[district], '')
        x = x.replace(district, '')
        
    return x

def clean_name_old_data(x):
    x = unidecode(x)
    x = x.lower()
    x = re.sub(r'[^a-zA-Z0-9]', '', x)
    x = x.strip()
    return x

def remove_special_characters(text):
    new_text = ''
    for i in unidecode(text):
        if re.search(r'^[A-Za-z0-9\s]+$',i) is None:
            new_text = new_text + ' '
        else:
            new_text = new_text + i
    return new_text


def clean_city(text):
    word_lst = (' dl ',' tt ',' kp ',' tx ',' tp ',' tl ',' ql ',' h ',' t ',' d ',' x ',' p ',' q ',' k ',' vn','dai lo ','thi tran ','thi xa ','khu pho ','thanh pho ','tinh lo ','quoc lo ','huyen ','tinh ','duong ','xa ','phuong ','quan ','khom ','viet nam','thon ','so nha ','sn ')
    result = text.strip()
    if len(result) > 2:
        first = text[:2]
        if first.startswith(('h ', 't ', 'd ', 'x ', 'p ', 'q ', 'k ', 'sn', 'tp')):
            result = text[2:]
    
    if len(result) > 3:
        first = text[:3]
        if first.startswith(('dl ', 'tt ', 'kp ', 'tx ', 'tp ', 'tl ', 'ql ', 'so ')):
            result = text[3:]
    for word in word_lst:
        result = result.replace(word,' ')
    return result

def extract_city_from_address(address,city_list):
    len_city = 0
    city = ''
    for city_name in city_list:
        if re.search(r'%s$' %(city_name),address) is not None:
            if len(city_name) >= len_city:
                len_city = len(city_name)
                city = city_name
    if city == '':
        return 'other'
    return city

def extract_district_from_address(city,address,temp_district):
    if city == 'other':
        return 'other'
    else:
        district_fillter = temp_district[temp_district['city_name'] == city]
        len_district = 0
        district = 'other'
        for i in district_fillter['code_name']:
            if re.search(r'%s$' %(i),address) is not None:
                if len(i) >= len_district:
                    len_district = len(i)
                    district = i
        return district
    
def cleansing_phone(x): # ca
    x = str(x)
    if x[:2] == '84':
        x = '0' + x[2:]
    elif x[:1] != '0':
        x = '0' + x
    return x


def convert_phone(phone,temp_convert_phone):
    phone = str(phone)
    temp_convert_phone = temp_convert_phone.astype(str)
    new_phone = ''
    for i in range(len(temp_convert_phone)):
        len_old_number = len(temp_convert_phone['old_number'][i])
        if phone[:len_old_number] == temp_convert_phone['old_number'][i]:
            new_phone = temp_convert_phone['new_number'][i] + phone[len_old_number:]
    if new_phone == '':
        return phone
    else:
        return new_phone
    
def update_city_cleansing(x,province):
    city = ''
    len_city = 0
    for i in province[province['name_acr'] == x]['code_name']:
        if len (i) >  len_city:
            city = i
            len_city = len(i)
    if city != '':
        return city
    else:
        return x


def cleansing_function(df_old, df_new, province, district, convert_phonenumber):
    
    ################################### CLEAN OLD DATA ######################################################
    df_old['customer_name_original'] = df_old['customer_name']
    df_old['customer_address_original'] = df_old['customer_address']
    
    df_old['customer_name'] = df_old['customer_name'].apply(lambda x: clean_name_old_data(x))
    #print(len(df_old.apply(lambda x: clean_address_old_data(x['customer_address'], x['district'], x['city']), axis=1)))
    #print(len(df_old))
    df_old['customer_address'] = df_old.apply(lambda x: clean_address_old_data(x['customer_address'], x['district'], x['city']), axis=1)

    ################################### CLEAN NEW DATA ######################################################
    hms = df_new[['customer_code', 'customer_name', 'mobile_phone', 'customer_address','vin']]
    hms = hms.rename(columns= {'customer_code' : 'id',
                        'customer_name' : 'name',
                        'mobile_phone' : 'phone',
                        'customer_address' : 'address',
                        'VIN' : 'vin'})
    hms.insert(0, 'unq_id', range(0, len(hms)))
    hms['address_cleansing'] = hms['address'].apply(lambda x: x if x is np.nan else unidecode(x).lower())
    hms['address_cleansing'] = hms['address_cleansing'].apply(lambda x: x if x is np.nan else clean_city(remove_special_characters(x)).replace(' ',''))
    # len_max = province.code_name.str.len().max()

    #tach thanh pho khoi dia chi
    hms['city'] = hms['address_cleansing'].apply(lambda x: 'other' if x is np.nan else extract_city_from_address(x,province['code_name']))
    hms['address_cleansing'] = hms.apply(lambda x: re.sub(r'%s$'%(x['city']),'', x['address_cleansing']) if x['city'] != 'other' else x['address_cleansing'] ,axis=1)

    #map cac quan/huyen voi tinh/thanh pho
    temp_district = district[['code_name','name_acr','province_code']].drop_duplicates()
    temp_district = temp_district[temp_district['name_acr'] != temp_district['code_name']]
    temp_district = temp_district.merge(province[['code_name','code']],left_on='province_code',right_on='code')
    temp_district.rename(columns={'code_name_x' : 'code_name', 'code_name_y' : 'city_name'}, inplace=True)

    #tach quan/huyen khoi dia chi
    hms['district'] = hms.apply(lambda x: extract_district_from_address(x['city'],x['address_cleansing'],temp_district),axis=1)
    hms['address_cleansing'] = hms.apply(lambda x: re.sub(r'%s$'%(x['district']),'', x['address_cleansing']) if (x['city'] != 'other' and x['district'] != 'other') else x['address_cleansing'] ,axis=1)

        
    #tao bang combination theo code goc nhung khong biet de lam gi
    combination = hms[['id','vin','name','address_cleansing','district','city','phone']]
    combination = combination.drop_duplicates()
    combination.sort_values(by=['id'],inplace=True)
    combination.insert(0, 'System_id', range(0, len(combination)))

    combination = combination.rename(columns= {'name' : 'CUSTOMER_NAME',
                                                'phone' : 'MOBILE_PHONE',
                                                'address_cleansing' : 'CUSTOMER_ADDRESS',
                                                'district' : 'DISTRICT',
                                                'city' : 'CITY',
                                                'vin' : 'VIN'})
    
    #tao cac cot cleansing va loai bo ky tu dac biet + dau tieng viet
    lst_col = ["System_id", "VIN", "CUSTOMER_NAME", "CUSTOMER_ADDRESS", "DISTRICT", "CITY", "MOBILE_PHONE"]
    temp_cleansing = combination[lst_col]
    for col in lst_col:
        col_name = re.search(r'phone|vin|name|address|city|district',col, re.IGNORECASE)
        if  col_name is not None:
            col_name = col_name[0].lower() + "_cleansing"
            if re.search(r'phone|vin',col_name,re.IGNORECASE):
                temp_cleansing[col_name] = temp_cleansing[col].apply(lambda x: remove_special_characters(x).replace(' ','') if x is not np.nan else x)
            else:
                temp_cleansing[col_name] = temp_cleansing[col].apply(lambda x: unidecode(x).lower() if x is not np.nan else x)

    #clean phone
    temp_convert_phone = convert_phonenumber[convert_phonenumber['flag'].astype(int) == 1][['old_number','new_number']].reset_index(drop= True)
    temp_cleansing['phone_cleansing'] = temp_cleansing['phone_cleansing'].apply(lambda x: cleansing_phone(x) if re.search(r'^[0-9]',x) is not None else x)
    temp_cleansing['phone_cleansing'] = temp_cleansing['phone_cleansing'].apply(lambda x: convert_phone(x,temp_convert_phone) if x is not np.nan else x)


    #clean city
    temp_cleansing['city_cleansing'] = temp_cleansing['city_cleansing'].apply(lambda x: x[:x.find('(')] if (x.find('(') != -1) and (x is not np.nan) else x)
    temp_cleansing['city_cleansing'] = temp_cleansing['city_cleansing'].apply(lambda x: x.replace('app','') if x is not np.nan else x)


    #clean name va lai clean address,city,district 1 lan nua
    lst_col_2 = ['name_cleansing','address_cleansing','district_cleansing','city_cleansing']
    for col in lst_col_2:
        if col == 'name_cleansing':
            temp_cleansing[col] = temp_cleansing[col].apply(lambda x: remove_special_characters(x).replace(' ','') if x is not np.nan else x)
        else:
            temp_cleansing[col] = temp_cleansing[col].apply(lambda x: clean_city(remove_special_characters(x)).replace(' ','') if x is not np.nan else x)


    temp_cleansing_col = temp_cleansing.columns.tolist()

    #update cot city
    temp_cleansing['city_cleansing'] = temp_cleansing['city_cleansing'].apply(lambda x: update_city_cleansing(x,province) if x is not np.nan else x)

    temp_cleansing = temp_cleansing.merge(province[['code_name','code']],left_on='city_cleansing', right_on='code_name', how='left')
    temp_cleansing = temp_cleansing.merge(district[['name_acr','province_code','code_name']], left_on=['district_cleansing','code'],right_on=['name_acr','province_code'], how='left')

    #update cot district
    temp_cleansing['district_cleansing'] = temp_cleansing.apply(lambda x: x['district_cleansing'] if x['code_name_y'] is np.nan else x['code_name_y'], axis=1)
    temp_cleansing = temp_cleansing[temp_cleansing_col]

    #update cot address voi city
    temp_cleansing = temp_cleansing.merge(province[['code_name','name_acr','code']], left_on = 'city_cleansing', right_on='code_name', how='left')
    temp_cleansing['address_cleansing'] = temp_cleansing.apply(lambda x: x['address_cleansing'].replace(x['name_acr'],'') if x['address_cleansing'] is not np.nan and x['name_acr'] is not np.nan else x['address_cleansing'],axis=1)
    temp_cleansing['address_cleansing'] = temp_cleansing.apply(lambda x: x['address_cleansing'].replace(x['code_name'],'') if x['address_cleansing'] is not np.nan and x['code_name'] is not np.nan else x['address_cleansing'],axis=1)

    #update cot address voi district
    temp_cleansing = temp_cleansing.merge(temp_district[['code_name','name_acr','province_code']], left_on = ['district_cleansing','code'], right_on=['code_name','province_code'], how='left')
    temp_cleansing['address_cleansing'] = temp_cleansing.apply(lambda x: x['address_cleansing'].replace(x['name_acr_y'],'') if x['address_cleansing'] is not np.nan and x['name_acr_y'] is not np.nan else x['address_cleansing'],axis=1)
    temp_cleansing['address_cleansing'] = temp_cleansing.apply(lambda x: x['address_cleansing'].replace(x['code_name_y'],'') if x['address_cleansing'] is not np.nan and x['code_name_y'] is not np.nan else x['address_cleansing'],axis=1)


    temp_cleansing = temp_cleansing[temp_cleansing_col]
    cleansing = temp_cleansing.drop_duplicates()
    cleansing['vin_group'] = cleansing['vin_cleansing'].apply(lambda x: x[3:8] if x is not np.nan else x)
    cleansing['phone_group'] = cleansing['phone_cleansing'].apply(lambda x: x[0:3] if x is not np.nan else x)
    cleansing = cleansing[["vin_group","vin_cleansing","name_cleansing","address_cleansing","district_cleansing","city_cleansing","phone_group","phone_cleansing"]]
    cleansing = cleansing.drop_duplicates()

    return df_old, cleansing
