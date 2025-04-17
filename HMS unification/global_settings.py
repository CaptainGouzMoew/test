import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from unidecode import unidecode

class Settings:
    def __init__(self):
        # Working root folder (the only path that should be changed)
        self.root_folder = os.path.dirname(os.path.realpath(__file__))
        self.input_folder = self.root_folder + '/input'
        self.tmp1_folder = self.input_folder + '/tmp1'
        self.tmp2_folder = self.input_folder + '/tmp2'
        self.output_folder = self.root_folder + '/output'
        
        # current year
        self.year_limit = 2024
        
        # last day of current month of data (31-12-current_year) (data cutoff)
        self.month_last = 20241212
        self.month_last_dt = datetime.strptime(str(self.month_last), '%Y%m%d')
        
        # first day of data cutoff
        self.month_first = 20060101
        self.month_first_dt = datetime.strptime(str(self.month_first), '%Y%m%d')

        
#         self.month_first = int(self.month_first_dt.strftime('%Y%m%d'))
#         self.month_first_dt = self.month_last_dt - relativedelta(years=5)
        
        # past time from day limit
        self.one_year_ago_dt = self.month_last_dt - relativedelta(years=1)
        self.five_year_ago_dt = self.month_last_dt - relativedelta(years=5)
        self.six_month_ago_dt = self.month_last_dt - relativedelta(months=6)
        
        self.six_month_ago = int(self.six_month_ago_dt.strftime('%Y%m%d'))

        
        # First day of next month of data (month_last + 1day)
        self.month_to = 20250101
        self.month_to_str = 'month_to_' + str(self.month_to)
        
        
        folders_to_create = [self.input_folder, self.tmp1_folder, self.tmp2_folder, self.output_folder]
        self.create_directories(folders_to_create)
    
    def get_kpi_col(self, df):
        out = []
        for column in df.columns.tolist():
            if column.startswith('kpi'):
                out.append(column)
        return out
        
    def read_file(self, path, ftype='excel', encoding='utf-8'):
        df = None
        if ftype == 'excel':
            df = pd.read_excel(path)
        elif ftype == 'csv':
            df = pd.read_csv(path, encoding=encoding)
        
        if df is not None:
            print(path)
            df.columns = self.clean_columns(df)
            print(df.dtypes)
            return df
        
    def create_directories(self, directory_list):
        for directory in directory_list:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Directory created: {directory}")
            else:
                print(f"Directory found: {directory}")
    
    def clean_phone(self='', phone=''):
        phone = str(phone)
        
        # Remove non letter & number
        phone = re.sub(r"\W|\.0$", "", phone).replace('_', '')

        # Get the number with length 12-11-10-9
        x = re.findall(r"\d{12}|\d{11}|\d{10}|\d{9}", phone)
        if len(x) == 0:
            return ''
        phone = x[0]

        # Replace 84 to 0
        if phone.startswith('84'):
            phone = phone.replace(phone, '0', 1)

        # Add 0 to phone head
        if not phone.startswith('0'):
            phone = '0' + phone

        # Replace phone head
        old_head = ['0169', '0168', '0167', '0166', '0165', '0164', '0163', '0162', '0128', '0123', '0124', '0125', '0127', '0129', '0120', '0121', '0122', '0126', '0128', '0182', '0186', '0188', '0199']
        new_head = ['039', '038', '037', '036', '035', '034', '033', '032', '088', '083', '084', '085', '081', '082', '070', '079', '077', '076', '078', '052', '056', '058', '059']

        for i in range(len(old_head)):
            if phone.startswith(old_head[i]):
                phone = phone.replace(old_head[i], new_head[i], 1)
                break

        ignore_phone_list = ['0000000000', '0000000001', '0000032123', '09999999999', '0']
        if phone in ignore_phone_list:
            return ''
        
        return phone
    
    def replace_special_chars(self, value, replace_char=' '):
        special = r'`~!@#$%^&*()-=_+[]{}\|;:'",<.>/?"
        for v in special:
            value = value.replace(v, replace_char)
        return value

    def replace_space_chars(self, value, replace_char=' '):
        pattern = r'\t+|\n+|\r\n+| +'
        value = re.sub(pattern, replace_char, value)
        return value.strip()

    def replace_abbreviation(self, value):
        abb = {' DL ' : ' ',
                ' TT ' : ' ',
                ' KP ' : ' ',
                'SO ' : ' ',
                ' TL ' : ' ',
                ' HCM' : 'HO CHI MINH',
                ' HN' : 'HA NOI',
                ' QL ' : ' ',
                ' DN ' : ' DA NANG ',
                ' H ' : ' ',
                ' T ' : ' ',
                ' D ' : ' ',
                ' X ' : ' ',
                ' P ' : ' ',
                ' Q ' : ' ',
                ' K ' : ' ',
                ' DAI LO' : ' ',
                ' THI TRAN' : ' ',
                ' KHU PHO' : ' ',
                ' THANH PHO' : ' ',
                ' TINH LO' : ' ',
                ' QUOC LO' : ' ',
                ' HUYEN' : ' ',
                ' TINH' : ' ',
                ' DUONG' : ' ',
                ' XA' : ' ',
                ' PHUONG' : ' ',
                #' QUAN' : ' ',
                ' KHOM' : ' ',
                'VIET NAM' : ' ',
                'SO NHA' : ' ',
                  "'" : ''}
        for v in abb.keys():
            value = value.replace(v, abb[v])
        return value

    def clean_address(self, address):
        if address.upper() == 'NAN' or address.upper() == 'NA' or address.upper == 'NULL':
            address = ''
        address = str(address)
        address = self.replace_special_chars(address)
        address = self.replace_space_chars(address)
        #address = unidecode(address)
        address = address.upper()
        #address = self.replace_abbreviation(address).replace(' ', '')
        return address
    
    def clean_vin(self, vin):
        vin = str(vin)
        vin = vin.upper()
        if vin == 'NAN' or vin == 'NA' or vin == 'NULL':
            vin = ''
        return vin
    
    def clean_columns(self, df):
        columns = [i.lower().strip().replace(' ', '_') for i in df.columns.tolist()]
        return columns
    
    def remove_vietnamese_accent(self, value):
        return unidecode(value)

    def remove_non_letters(self, value):
        pattern = re.compile('[^a-zA-Z] ')
        letters_only = re.sub(pattern, '', value)
        return letters_only

    def remove_parentheses(self, value):
        pattern = re.compile(r'\([^)]*\)')
        cleaned_value = re.sub(pattern, '', value)
        return cleaned_value


    def mark_as_company(self, val):
        check_list = ['cty', 'cong ty', 'congty', 'ct', 'xn', 'xi nghiep', 'ban quan ly', 'ban ql', 'ban tuyen giao', 'ban to chuc', 'tnhh', 'vien bao ve', 'vien hoa sinh', 'vien y hoc', 'tnhh', 'xe chuyen vung', 'trung tam sat hach', 'cuc chinh tri', 'cuc bao ve', 'bo cong an', 'cong thong tin', 'cuc thi hanh', 'cong an ', 'doanh nghiep', 'nha may', 'nha xuat ban', 'nxb', 'chi nhanh', 'co so', 'ngan hang' , 'o to ', 'tap doan', 'dnth', 'buu dien', 'tmcp', 'phong cs', 'co dien', 'hawee', 'hop tac xa', 'vien kiem sat', 'uy ban', 'ubnd']
        val = self.remove_vietnamese_accent(val)
        val = self.remove_non_letters(val)
        for check in check_list:
            if check in val:
                return True
        return False
    
    def remove_duplicate_words(self, input_string):
        words = re.findall(r'\b(\w+)\b', input_string)
        unique_words = []
        for word in words:
            if word not in unique_words:
                unique_words.append(word)
        cleaned_string = ' '.join(unique_words)
        return cleaned_string
    
    def clean_name(self, val):
        val = self.remove_parentheses(val)
        val = re.sub(re.compile(' +'), ' ', val)
        val = val.replace('bán xe', '').replace('ban xe', '').replace('mr.', '').replace('mr ', '')
        val = re.sub(re.compile(r'\d'), '', val)
        val = re.sub(re.compile(r'[^\w\s]'), '', val)
        val = self.remove_duplicate_words(val)
        #val = val.replace(' ', '')
        #val = self.remove_vietnamese_accent(val).strip()
        if val == 'nan' or val == 'null':
            val = ''
        return val.strip()

################### CODE TO ADD CITY ####################################


import re
import difflib
import unicodedata
from unidecode import unidecode

def replace_tp(tp):
    tp = tp.replace('THANH HOÁ', 'THANH HÓA')
    tp = tp.replace('THÀNH PHỐTHANH HÓA', 'THANH HÓA')
    tp = tp.replace('KHÁNH HOÀ', 'KHÁNH HÒA')
    tp = tp.replace('TP.HCM', 'HỒ CHÍ MINH')
    tp = tp.replace('TPHCM', 'HỒ CHÍ MINH')
    tp = tp.replace('TP HCM', 'HỒ CHÍ MINH')
    tp = tp.replace('HCM', 'HỒ CHÍ MINH')
    tp = tp.replace('HỒ CHÍ MINH', 'HỒ CHÍ MINH')
    tp = tp.replace('DAKLAK', 'ĐẮK LẮK')
    tp = tp.replace('ÐẮK LẮK', 'ĐẮK LẮK')
    tp = tp.replace('ÐỒNG NAI', 'ĐỒNG NAI')
    tp = tp.replace('ÐỒNG NAI', 'ĐỒNG NAI')
    tp = tp.replace('ÐÀ NẴNG', 'ĐÀ NẴNG')
    tp = tp.replace('HOÀ BÌNH', 'HÒA BÌNH')
    tp = tp.replace('THỪA THIÊN HUẾ', 'THỪA THIÊN - HUẾ')
    tp = tp.replace('BÌNH ÐỊNH', 'BÌNH ĐỊNH')
    tp = tp.replace('ÐỒNG THÁP', 'ĐỒNG THÁP')
    tp = tp.replace('HN', 'HÀ NỘI')
    tp = tp.replace('HÀ NỘI', 'HÀ NỘI')
    tp = tp.replace('HUẾ', 'THỪA THIÊN - HUẾ')
    tp = tp.replace('APP', '')
    tp = tp.replace('(', '')
    tp = tp.replace(')', '')
    return tp

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵà]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪÀ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡộ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠỘ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    s = re.sub(r"[^a-zA-Z0-9]+", ' ', s)
    return unidecode(s)

def replace_city(df, city_col_in, city_col_out):
    vn_city = (
    "Cà Mau",
    "Bạc Liêu",
    "Sóc Trăng",
    "Hậu Giang",
    "Cần Thơ",
    "Kiên Giang",
    "An Giang",
    "Đồng Tháp",
    "Vĩnh Long",
    "Trà Vinh",
    "Bến Tre",
    "Tiền Giang",
    "Long An",
    "Hồ Chí Minh",
    "Bà Rịa",
    "Vũng Tàu",
    "Bà Rịa - Vũng Tàu",
    "Đồng Nai",
    "Bình Dương",
    "Tây Ninh",
    "Bình Phước",
    "Lâm Đồng",
    "Đắk Nông",
    "Đắk Lắk",
    "Gia Lai",
    "Kon Tum",
    "Bình Thuận",
    "Ninh Thuận",
    "Khánh Hòa",
    "Phú Yên",
    "Bình Định",
    "Quảng Ngãi",
    "Quảng Nam",
    "Đà Nẵng",
    "Huế",
    "Quảng Trị",
    "Quảng Bình",
    "Hà Tĩnh",
    "Nghệ An",
    "Thanh Hóa",
    "Ninh Bình",
    "Nam Định",
    "Hà Nam",
    "Thái Bình",
    "Hưng Yên",
    "Hải Phòng",
    "Hải Dương",
    "Hà Nội",
    "Bắc Ninh",
    "Vĩnh Phúc",
    "Phú Thọ",
    "Bắc Giang",
    "Quảng Ninh",
    "Lạng Sơn",
    "Thái Nguyên",
    "Hòa Bình",
    "Yên Bái",
    "Sơn La",
    "Lai Châu",
    "Điện Biên",
    "Lào Cai",
    "Tuyên Quang",
    "Bắc Kạn",
    "Cao Bằng",
    "Hà Giang",
    )
    city_master_list = vn_city
    address_list = tuple(df[city_col_in])
    thanhpho_list = []
    for add in address_list:
        has_city = ''
        add = add.upper()
        add = re.sub(' +', ' ', add).strip()
        add_og = add
        for thanh_pho in city_master_list:
            add = replace_tp(add)
            if add[-len(thanh_pho):] == thanh_pho.upper():
                has_city = thanh_pho.upper()
                break

##        if has_city == '':
##            for thanh_pho in city_master_list:
##                temp = difflib.SequenceMatcher(None, no_accent_vietnamese(add_og), no_accent_vietnamese(thanh_pho).upper())
##                if temp.ratio() >= 0.9:
##                    has_city = thanh_pho.upper()
##                    break
##                else:
##                    if no_accent_vietnamese(thanh_pho).upper() in no_accent_vietnamese(add_og).upper():
##                        has_city = thanh_pho.upper()
##                        break

        thanhpho_list.append(has_city)
    df[city_col_out] = thanhpho_list

    df[city_col_out] = df[city_col_out].apply(lambda x: x.replace('Bà Rịa - Vũng Tàu'.upper(), 'BRVT'.upper())
                                  .replace('Bà Rịa'.upper(), 'BRVT'.upper())
                                  .replace('Vũng Tàu'.upper(), 'BRVT'.upper()))

    df[city_col_out] = df[city_col_out].apply(lambda x: x.replace( 'BRVT'.upper(), 'Bà Rịa - Vũng Tàu'.upper()))
    return df

###################################### CODE TO CHECK DF ################################################################

import io
class Data_Info:
    def get_info(self,df):
        for col in df.columns:
            x = col.strip()
            x = re.sub(r"\"|\(|\)",r"",x)
            x = re.sub(r"\s",r"_",x)
            df.rename(columns = {col:x},inplace=True)
        buf = io.StringIO()
        df.info(buf=buf)
        s = buf.getvalue()
        lines = [line.split() for line in s.splitlines()[3:-2]]
        df_info = pd.DataFrame(lines)
        df_info = df_info[2:]
        df_info['Non_Null_Count'] = df_info[2].astype(str) + " " + df_info[3]
        def count_value(df,col,typed):
            count_zero_blank = 0
            count_pos = 0
            count_neg = 0

            count_true = 0
            count_false = 0
            
            if typed == "int64" or typed == 'float64':
                for row in df[col]:
                    if row is not np.NaN:
                        if row == 0:
                            count_zero_blank += 1
                        elif row > 0:
                            count_pos += 1
                        elif row < 0:
                            count_neg += 1
            else:
                for row in df[col]:
                    if row is not np.NaN:
                        if type(row) is bool:
                            if row:
                                count_true += 1
                            else:
                                count_false += 1
                        if len(str(row)) < 1:
                            count_zero_blank += 1
            return str(count_zero_blank) + " " + str(count_pos) + " " + str(count_neg)+ " " + str(count_true)+ " " + str(count_false)
        df_info['Check'] = df_info.apply(lambda x: count_value(df,x[1],x[4]),axis = 1)
        df_info[['Zero_or_blank_count', 'Pos_num_count','Neg_num_count', 'True_count', 'False_count']] = df_info['Check'].str.split(' ', expand=True)
        df_info.drop([0,2,3,'Check'],axis=1,inplace=True)
        df_info.rename(columns={1:'Column',4:'Dtype'},inplace=True)
        return df_info
