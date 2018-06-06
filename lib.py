import re
def data_type(pn):
    # 判断PH
    if len(pn) == 16 and re.match(r'PH_\d{3}0C\d{3}00G2\d',pn):
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
        elif re.match(r'88\d0C\d{5}G7\d',pn):
            return 'Specific_RBA'
    # 若全不匹配，返回N/A pn，用来识别错误pn
    else:
        return 'N/A pn'

def get_edz(pn):
    # 根据不同DM进行判断返回edz号(Integer)
    if pn is None:
        return None
    if data_type(pn) in ['HI', 'GBN', 'MBS', 'RBA', 'DISC', 'DISC_ASY', 'DISC_RBA']:
        return int(pn[2:4] + pn[5])
    elif data_type(pn) in ['R_RBA', 'R_DISC_ASY', 'R_HI']:
        return int(pn[4:6] + pn[7])
    # 待完善：这里没有考虑Specific_RBA的edz情况，需要新建一个89G70对应edz的数据库表格
    else:
        return None