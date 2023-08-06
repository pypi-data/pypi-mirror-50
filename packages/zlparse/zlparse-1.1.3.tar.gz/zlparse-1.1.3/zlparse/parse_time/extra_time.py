import datetime
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

# from lmf.dbv2 import db_query


list_page_time_ggtime_question = ['guangxi_hezhou_ggzy',
                                  'yunnan_tengchong_ggzy',
                                  'fujian_quanzhou_ggzy',
                                  'fujian_wuyishan_ggzy',
                                  'fujian_shaowu_ggzy',
                                  'fujian_fuqing_ggzy',
                                  'qycg_ec_ccccltd_cn',
                                  'zhejiang_ningbo_zfcg',
                                  'zhejiang_wenzhou_zfcg',
                                  'guangxi_guigang_zfcg',
                                  'shandong_shandongsheng_zfcg',
                                  'guangxi_guigang_ggzy',
                                  'guizhou_guiyang_ggzy',
                                  'sichuan_sichuansheng_ggzy',
                                  'jiangsu_nanjing_ggzy',
                                  'xinjiang_atushi_gcjs',
                                  'xinjiang_bole_gcjs',
                                  'xinjiang_changji_gcjs',
                                  'xinjiang_xinjiangsheng_gcjs',
                                  'xinjiang_kashi_gcjs',
                                  'xinjiang_tacheng_gcjs',
                                  'shandong_shandongsheng_1_ggzy',
                                  'fujian_fujiansheng_ggzy',
                                  'guizhou_guizhousheng_ggzy',
                                  'hubei_wuhan_ggzy',
                                  'sichuan_panzhihua_ggzy',
                                  'zhejiang_taizhou_ggzy',
                                  'jiangsu_wuxi_ggzy',
                                  'liaoning_tieling_ggzy',
                                  'hunan_changsha_gcjs',
                                  'sichuan_neijiang_ggzy',
                                  'guangdong_dongguan_ggzy',
                                  'hubei_wuhan_1_zfcg',
                                  'guangdong_yangjiang_gcjs',
                                  'xinjiang_wulumuqi_zfcg',
                                  'qycg_dfqcgs_dlzb_com',
                                  'anhui_anhuisheng_gcjs',
                                  'jiangsu_danyang_ggzy',
                                  'guangdong_sihui_ggzy',
                                  'liaoning_chaoyang_ggzy',
                                  'zhejiang_zhejiangsheng_gcjs',
                                  'xinjiang_yining_gcjs',
                                  'jiangxi_nanchang_gcjs',
                                  'neimenggu_xilinguolemeng_ggzy',
                                  'zhejiang_tongxiang_ggzy',
                                  'shanxi_xian_ggzy',
                                  'yunnan_lijiang_ggzy',
                                  'yunnan_dali_ggzy',
                                  'yunnan_honghe_ggzy',
                                  'yunnan_lincang_ggzy',
                                  'yunnan_puer_ggzy',
                                  'guangdong_guangdongsheng_zfcg',
                                  'liaoning_shenyang_ggzy',
                                  'sichuan_neijiang_ggzy',
                                  'hubei_huanggang_ggzy',
                                  'guangdong_yunfu_ggzy',
                                  'sichuan_luzhou_ggzy',
                                  'liaoning_huludao_ggzy',
                                  'shanxi1_xinzhou_gcjs',
                                  'jiangxi_dexing_ggzy',
                                  'ningxia_yinchuan_zfcg',
                                  'ningxia_ningxiasheng_zfcg',
                                  'shandong_qingdao_zfcg',
                                  'qycg_www_dlswzb_com',
                                  'ningxia_ningxiasheng_gcjs',
                                  'jiangsu_suzhou_zfcg',
                                  'zhejiang_longquan_ggzy',
                                  'xinjiang_wulumuqi_gcjs',
                                  'qycg_ec_ceec_net_cn',
                                  'neimenggu_bayannaoer_zfcg', ]

list_page_time_ggtime_missing = [
    'jiangxi_jiangxisheng_ggzy',
    'anhui_anhuisheng_1_ggzy',
    'jiangsu_taizhou_zfcg',
    'guangxi_guangxisheng_1_gcjs',
    'qycg_zljt_dlzb_com',
    'qycg_baowu_ouyeelbuy_com',
    'xinjiang_beitun_ggzy',
    'anhui_anhuisheng_ggzy',
    'jiangxi_pingxiang_gcjs',
    'neimenggu_neimenggusheng_zfcg',
    'qycg_bid_fujianbid_com',
    'shandong_dezhou_zfcg',
    'qycg_ecp_cgnpc_com_cn',
    'sichuan_pengzhou_ggzy',
    'fujian_sanming_zfcg',
    'qycg_bidding_ceiec_com_cn',
    'neimenggu_eeduosi_ggzy',
    'guangdong_guangdongsheng_ggzy',
    'jilin_changchun_gcjs',
    'liaoning_dalian_gcjs',
    'sichuan_meishan_ggzy',
    'shanxi_xianyang_ggzy',
    'jiangsu_xuzhou_ggzy',
    'heilongjiang_qqhaer_gcjs',
    'shandong_shandongsheng_gcjs',
    'anhui_anqing_zfcg',
    'hunan_hunansheng_gcjs',
    'jiangxi_pingxiang_zfcg',
    'shanxi_hanzhong_gcjs',
    'sichuan_chengdu_gcjs',
    'shanxi_xian_gcjs',
    'jiangsu_yangzhou_gcjs',
    'jiangsu_zhangjiagang_ggzy',
    'guangxi_baise_gcjs',
]

list_page_time_fbjs = [
    'guangxi_hezhou_ggzy',
    'yunnan_tengchong_ggzy',
    'fujian_quanzhou_ggzy',
    'fujian_wuyishan_ggzy',
    'fujian_shaowu_ggzy',
    'fujian_fuqing_ggzy',
    'qycg_ec_ccccltd_cn',
    'zhejiang_ningbo_zfcg',
    'zhejiang_wenzhou_zfcg',
    'guangxi_guigang_zfcg',
    'shandong_shandongsheng_zfcg',
    'guangxi_guigang_ggzy',
    'guizhou_guiyang_ggzy',
    'sichuan_sichuansheng_ggzy',
    'jiangsu_nanjing_ggzy',
    'xinjiang_atushi_gcjs',
    'xinjiang_bole_gcjs',
    'xinjiang_changji_gcjs',
    'xinjiang_xinjiangsheng_gcjs',
    'xinjiang_kashi_gcjs',
    'xinjiang_tacheng_gcjs',
    'shandong_shandongsheng_1_ggzy',
    'fujian_fujiansheng_ggzy',
    'guizhou_guizhousheng_ggzy',
    'hubei_wuhan_ggzy',
    'sichuan_panzhihua_ggzy',
    'zhejiang_taizhou_ggzy',
    'jiangsu_wuxi_ggzy',
    'liaoning_tieling_ggzy',
]


def ext_from_ggtime(ggstart_time):
    t1 = ggstart_time
    a = re.findall('([1-9][0-9]{3})[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', t1)

    if a != []:
        y = a[0]
        x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
        return x

    a = re.findall('([1-9][0-9]{3})[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2})', t1)
    if a != []:
        y = a[0]
        x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
        return x

    a = re.findall('^([0-2][0-9])[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2})', t1)
    if a != []:
        y = a[0]
        x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
        x = '20' + x
        return x

    a = re.findall('^(20[0-9]{2})--([0-9]{1,2})-([0-9]{1,2})', t1)

    if a != []:
        x = '-'.join([a[0][0], a[0][1] if a[0][1] != '0' else '1', a[0][2] if a[0][2] != '0' else '1'])

        return x

    if ' CST ' in t1:
        try:
            x = time.strptime(t1, '%a %b %d %H:%M:%S CST %Y')
            x = time.strftime('%Y-%m-%d %H:%M:%S', x)
        except:
            x = ''
        if x != '': return x
    a = re.findall('^(20[0-9]{6})', t1)
    if a != []:
        x = '-'.join([a[0][:4], a[0][4:6], a[0][6:8]])
        return x

    return None


def extimefbsj(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:发布时间)[：:](20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt.replace('documentwrite', ''))
    # print(a)
    if a != []:
        return '-'.join(a[0])
    return None


def extime(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:更新时间|发文日期|发布日期|公示日期)[：:](20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt.replace('documentwrite', ''))
    # print(a)
    if a != []:
        return '-'.join(a[0])
    return None


def extime_xxsj(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:信息时间)[：:](20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt.replace('documentwrite', ''))
    # print(a)
    if a != []:
        return '-'.join(a[0])
    return None


def strptime_transfromgg_guangdong_guangdongsheng(page):
    list1 = []
    soup = BeautifulSoup(page, 'lxml')
    soup_input = soup.find_all('input')[-3:]
    for i in soup_input:
        value = i['value']
        list1.append(value)
    if list1 != []:
        return ('-'.join([list1[0], list1[1], list1[2]]))
    return None


def strptime_transfrom_yunan(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = '(?:发布时间|提交时间|公示时间)[：:]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})'

    a = re.findall(p, txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def strptime_transfrom_yue_r_n(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/', '', soup.text.strip())
    p = "(?:信息时间|信息日期|信息发布日期|发稿时间|发布时间|生成日期)[：:]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})[\-\.\\日/](20[0-2][0-9])"
    a = re.findall(p, txt)
    if a != []:
        return (a[0][2] + '-' + a[0][0] + '-' + a[0][1])
    return None


def extime_all(page, ggstart_time, quyu):
    ggstart_time = ext_from_ggtime(ggstart_time if ggstart_time is not None else '')
    if quyu in list_page_time_ggtime_question:
        if quyu in [
            'guangxi_hezhou_ggzy',
            'yunnan_tengchong_ggzy',
            'fujian_quanzhou_ggzy',
            'fujian_wuyishan_ggzy',
            'fujian_shaowu_ggzy',
            'fujian_fuqing_ggzy',
            'qycg_ec_ccccltd_cn',
            'zhejiang_ningbo_zfcg',
            'zhejiang_wenzhou_zfcg',
            'guangxi_guigang_zfcg',
            'shandong_shandongsheng_zfcg',
            'guangxi_guigang_ggzy',
            'guizhou_guiyang_ggzy',
            'sichuan_sichuansheng_ggzy',
            'jiangsu_nanjing_ggzy',
            'xinjiang_atushi_gcjs',
            'xinjiang_bole_gcjs',
            'xinjiang_changji_gcjs',
            'xinjiang_xinjiangsheng_gcjs',
            'xinjiang_kashi_gcjs',
            'xinjiang_tacheng_gcjs',
            'shandong_shandongsheng_1_ggzy',
            'fujian_fujiansheng_ggzy',
            'guizhou_guizhousheng_ggzy',
            'hubei_wuhan_ggzy',
            'sichuan_panzhihua_ggzy',
            'zhejiang_taizhou_ggzy',
            'jiangsu_wuxi_ggzy',
            'liaoning_tieling_ggzy',
        ]:
            res = extimefbsj(page)
        elif quyu in [
            'guangdong_guangdongsheng_zfcg'
        ]:
            res = strptime_transfromgg_guangdong_guangdongsheng(page)
        elif quyu in [
            'sichuan_neijiang_ggzy',
            'guangdong_dongguan_ggzy',
            'hubei_wuhan_1_zfcg',
            'guangdong_yangjiang_gcjs',
            'xinjiang_wulumuqi_zfcg',
            'qycg_dfqcgs_dlzb_com',
            'anhui_anhuisheng_gcjs',
        ]:
            res = extime(page)
        elif quyu in [
            'jiangsu_danyang_ggzy',
            'guangdong_sihui_ggzy',
            'liaoning_chaoyang_ggzy',
            'zhejiang_zhejiangsheng_gcjs',
            'xinjiang_yining_gcjs',
            'jiangxi_nanchang_gcjs',
            'neimenggu_xilinguolemeng_ggzy',
            'zhejiang_tongxiang_ggzy',
            'shanxi_xian_ggzy',
        ]:
            res = extime_xxsj(page)
        elif quyu in [
            'yunnan_lijiang_ggzy',
            'yunnan_dali_ggzy',
            'yunnan_honghe_ggzy',
            'yunnan_lincang_ggzy',
            'yunnan_puer_ggzy',
        ]:
            res = strptime_transfrom_yunan(page)
        elif quyu in [
            'liaoning_shenyang_ggzy'
        ]:
            res = strptime_transfrom_yue_r_n(page)
        else:
            res = None
    elif quyu in list_page_time_ggtime_missing:
        if quyu in [
            'anhui_anhuisheng_1_ggzy',
            'jiangsu_taizhou_zfcg',
            'guangxi_guangxisheng_1_gcjs',
            'qycg_zljt_dlzb_com',
            'qycg_baowu_ouyeelbuy_com',
            'xinjiang_beitun_ggzy',
        ]:
            if ggstart_time is not None:
                res = ggstart_time
            else:
                res = extime(page)
        elif quyu in [
            'anhui_anhuisheng_ggzy',
            'jiangxi_pingxiang_gcjs',
            'neimenggu_neimenggusheng_zfcg',
            'qycg_bid_fujianbid_com',
            'shandong_dezhou_zfcg',
            'qycg_ecp_cgnpc_com_cn',
            'sichuan_pengzhou_ggzy',
            'fujian_sanming_zfcg',
            'qycg_bidding_ceiec_com_cn',
            'neimenggu_eeduosi_ggzy',
            'guangdong_guangdongsheng_ggzy',
            'jilin_changchun_gcjs',
            'liaoning_dalian_gcjs',
        ]:
            if ggstart_time is not None:
                res = ggstart_time
            else:
                res = extimefbsj(page)
        elif quyu in [
            'sichuan_meishan_ggzy',
            'shanxi_xianyang_ggzy',
            'jiangsu_xuzhou_ggzy',
            'heilongjiang_qqhaer_gcjs',
        ]:
            if ggstart_time is not None:
                res = ggstart_time
            else:
                res = extime_xxsj(page)
        else:
            res = ggstart_time
    else:
        res = ggstart_time
    res = ext_from_ggtime(res if res is not None else '')
    if not res: return None
    if pd.to_datetime(res, format='%Y-%m-%d', errors='ignore') <= pd.to_datetime(datetime.datetime.now().strftime('%Y-%m-%d'), format='%Y-%m-%d',
                                                                                 errors='ignore'):
        return res
    else:
        return None


if __name__ == '__main__':
    print(extime_all('', '2019-1-1 00:00:00', 'anhui_anqing_ggzy'))
