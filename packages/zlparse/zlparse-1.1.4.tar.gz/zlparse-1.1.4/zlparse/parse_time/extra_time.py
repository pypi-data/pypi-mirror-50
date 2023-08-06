import json
from zlparse_.zlparse.parse_time.common import *
from zlparse_.zlparse.parse_time.conf import *
from zlparse_.zlparse.parse_time.exec_func_f import exec_func
# exec_func = {
#     'extimefbsj': extimefbsj,
#     'extime_xxsj': extime_xxsj,
#     'strptime_transfrom_yunan': strptime_transfrom_yunan,
#     'strptime_transfrom_yue_r_n': strptime_transfrom_yue_r_n,
#     'extime': extime,
#     'extime_v2': extime_v2,
#     'extimefbsj_v2': extimefbsj_v2,
#     'extime_xxsj_v2': extime_xxsj_v2,
#     'strptime_transfromgg_guangdong_guangdongsheng': strptime_transfromgg_guangdong_guangdongsheng,
# }


def extime_all(page, ggstart_time, quyu,conp=False):
    if conp:
        methed = select(quyu,conp)
    else:
        with open('quyu_time_func.json', encoding='utf-8') as f:
            dict_a = json.load(f)
        methed = dict_a[quyu]

    ggstart_time = ext_from_ggtime(ggstart_time if ggstart_time is not None else '')

    if methed != 'ggstart_time':
        if methed == 'None':
            res = None
        else:
            res = exec_func[methed](ggstart_time, page)
    else:
        res = ggstart_time

    res = ext_from_ggtime(res if res is not None else '')
    if not res: return None
    if pd.to_datetime(res, format='%Y-%m-%d', errors='ignore') <= pd.to_datetime(datetime.datetime.now().strftime('%Y-%m-%d'), format='%Y-%m-%d',errors='ignore'):
        return res
    else:
        return None


if __name__ == '__main__':

    conp = ["postgres", "since2015", "192.168.3.171", "anbang", "parse_project_code"]

    from zlparse_.zlparse.parse_time.conf import file_to_db,update,insert

    # file_to_db(conp)
    # insert('xinjiang_atushi_gcjs111111','xxxxxxxxxxxxxxwerwerx',conp)
    # with open('quyu_time_func.json')