import re
import numpy as np
import pandas as pd

def impact_list_preprocess(object):
    # 对.xlsx文件进行处理后返回一个pandas.DataFrame类用于上传数据库
    df = pd.read_excel(object)
    column_change = {
        'Change Number': 'change_number',
        'Configuration of Change Authority': 'cfg_of_change_authority',
        'Change Type(before)': 'change_type',
        'Number(before)': 'pn_bef',
        'Edition(before)': 'edition_bef',
        'Quantity(before)': 'quantity_bef',
        'Effectivity(before)': 'effectivity_bef',
        'Number(after)': 'pn_after',
        'Edition(after)': 'edition_aft',
        'Quantity(after)': 'quantity_aft',
        'Effectivity(after)': 'effectivity_aft'
    }
    df.rename(columns=column_change, inplace=True)
    df['edz'] = df['pn_after'].apply(get_edz)
    df.loc[df['edz'].isnull(), ['edz']] = df.loc[df['edz'].isnull(), ['pn_bef']]['pn_bef'].apply(get_edz)
    return df

def data_type(pn):
    if pn is np.nan:
        return 'N/A pn'
    # 判断PH
    elif len(pn) == 16 and re.match(r'PH_\d{3}0C\d{3}00G2\d',pn):
        return 'PH'
    # 判断R模型
    elif re.match(r'R_\d{4}C\d{5}G\d{2}',pn):
        if re.match(r'R_88\d0C\d{3}00G2\d',pn):
            return 'R_HA'
        elif re.match(r'R_88\d[^0]C\d{5}G2\d',pn):
            return 'R_HI'
        elif re.match(r'R_88\d[^0]C\d5000G4\d',pn):
            return 'R_RBA'
        elif re.match(r'R_89\d[^0]C\d{5}G2\d',pn):
            return 'R_DISC_ASY'
    #判断89DM
    elif len(pn) == 15 and re.match(r'89\d[^0]C\d{5}G\d{2}',pn):
        if re.match(r'89\d{2}C\d{5}G7\d',pn):
            return 'DISC'
        elif re.match(r'89\d{2}C\d{5}G2\d',pn):
            return 'DISC_ASY'
        elif re.match(r'89\d{2}C\d{5}G4\d',pn):
            return 'DISC_RBA'
    # 判断88DM
    elif len(pn) == 13 and re.match(r'88\d{2}C\d{5}G\d{2}',pn):
        if re.match(r'88\d0C\d{3}00G2\d',pn):
            return 'HA'
        elif re.match(r'88\d[^0]C\d0000G2\d',pn):
            return 'HI'
        elif re.match(r'88\d[^0]C\d5000G4\d',pn):
            return 'RBA'
        elif re.match(r'88\d[^0]C\d{5}G6\d',pn):
            return 'GBN'
        elif re.match(r'88\d[^0]C\d{5}G7\d',pn):
            return 'MBS'
        elif re.match(r'8800C\d{5}G7\d',pn):
            return 'Specific_RBA'
    # 若全不匹配，返回N/A pn
    else:
        return 'N/A pn'

def get_edz(pn):
    # pn为string类型输入，或者是np.nan
    if pn is np.nan:
        return None
    elif data_type(pn) in ['HI','GBN','MBS','RBA','DISC','DISC_ASY','DISC_RBA']:
        return int(pn[2:4]+pn[5])
    elif data_type(pn) in ['R_RBA','R_DISC_ASY','R_HI']:
        return int(pn[4:6]+pn[7])
    # specific RBA需要对数据库进行查询才能获取
    # elif data_type(pn) in ['Specific_RBA']:
    #     return
    else:
        return None