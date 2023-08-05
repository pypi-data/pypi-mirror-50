import datetime
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
from lmf.dbv2 import db_query

not_ggzy_list_page_time = ['anhui_huainan_gcjs',
                           'anhui_xuancheng_gcjs',
                           'guangxi_beihai_gcjs',
                           'guangxi_qinzhou_gcjs',
                           'guangxi_guangxisheng_gcjs',
                           'hebei_shijiazhuang_gcjs',
                           'hebei_tangshan_gcjs',
                           'henan_pingdingshan_gcjs',
                           'henan_zhengzhou_gcjs',
                           'hunan_loudi_gcjs',
                           'jiangsu_changzhou_gcjs',
                           'jiangsu_nanjing_gcjs',
                           'shandong_dongying_gcjs',
                           'shandong_rizhao_gcjs',
                           'shandong_zaozhuang_gcjs',
                           'shanxi_ankang_gcjs',
                           'shanxi_xianyang_gcjs',
                           'shanxi_yanan_gcjs',
                           'sichuan_zigong_gcjs',
                           'xinjiang_hami_gcjs',
                           'zhejiang_huzhou_gcjs',
                           'zhejiang_jinhua_gcjs',
                           'zhejiang_zhoushan_gcjs',
                           'anhui_anhuisheng_zfcg',
                           'fujian_fuzhou_zfcg',
                           'fujian_longyan_zfcg',
                           'fujian_ningde_zfcg',
                           'fujian_putian_zfcg',
                           'fujian_quanzhou_zfcg',
                           'fujian_sanming_zfcg',
                           'fujian_xiamen_zfcg',
                           'fujian_zhangzhou_zfcg',
                           'gansu_jinchang_zfcg',
                           'gansu_gansusheng_zfcg',
                           'guangxi_guilin_zfcg',
                           'guangxi_liuzhou_zfcg',
                           'guangxi_nanning_zfcg',
                           'guangxi_guangxisheng_zfcg',
                           'guizhou_guizhousheng_zfcg',
                           'guizhou_tongren_zfcg',
                           'hainan_haikou_zfcg',
                           'hainan_hainansheng_zfcg',
                           'hainan_wenchang_zfcg',
                           'hebei_hebeisheng_zfcg',
                           'heilongjiang_heilongjiangsheng_zfcg',
                           'heilongjiang_yichun_zfcg',
                           'hubei_huanggang_zfcg',
                           'hubei_hubeisheng_zfcg',
                           'hubei_shiyan_zfcg',
                           'hunan_changde_zfcg',
                           'jiangsu_changzhou_zfcg',
                           'jiangsu_huaian_zfcg',
                           'jiangsu_lianyungang_zfcg',
                           'jiangsu_nanjing_zfcg',
                           'jiangsu_nantong_zfcg',
                           'jiangsu_xuzhou_zfcg',
                           'jiangsu_xuzhou_1_zfcg',
                           'jiangsu_zhenjiang_zfcg',
                           'jiangxi_jian_zfcg',
                           'jilin_jilinshi_zfcg',
                           'jilin_jilinsheng_zfcg',
                           'jilin_changchun_zfcg',
                           'liaoning_chaoyang_zfcg',
                           'neimenggu_eerduosi_zfcg',
                           'neimenggu_tongliao_zfcg',
                           'qinghai_qinghaisheng_zfcg',
                           'shandong_rizhao_zfcg',
                           'shanxi_shanxisheng_zfcg',
                           'shanxi1_changzhi_zfcg',
                           'shanxi1_shanxi1sheng_zfcg',
                           'sichuan_sichuansheng_zfcg',
                           'xinjiang_alashankou_zfcg',
                           'xinjiang_xinjiangsheng_zfcg',
                           'shanxi_hanzhong_zfcg',
                           'xizang_xizangsheng_zfcg',
                           'zhejiang_hangzhou_zfcg',
                           'zhejiang_quzhou_zfcg',
                           'zhejiang_zhejiangsheng_zfcg',
                           'qycg_b2bcoal_crp_net_cn',
                           'qycg_bid_ansteel_cn',
                           'qycg_bid_powerchina_cn',
                           'qycg_buy_cnooc_com_cn',
                           'qycg_csbidding_csair_com',
                           'qycg_dzzb_ciesco_com_cn',
                           'qycg_www_cdt_eb_com',
                           'qycg_www_mgzbzx_com',
                           'qycg_www_qhbidding_com',
                           'qycg_www_sztc_com',
                           'qycg_www_wiscobidding_com_cn',
                           'qycg_www_ykjtzb_com',
                           'qycg_www_zeec_cn',
                           'qycg_www_zmzb_com',
                           'qycg_wzcgzs_95306_cn',
                           'qycg_zb_crlintex_com'
                           ]

not_ggzy_list_page_notime = [
    'fujian_sanming_gcjs',
    'jilin_siping_gcjs',
    'shanxi_yulin_gcjs',
    'beijing_beijingshi_zfcg',
    'guangdong_shantou_zfcg',
    'guangxi_fangchenggang_zfcg',
    'guangxi_wuzhou_zfcg',
    'hunan_changsha_1_zfcg',
    'jiangxi_jiangxisheng_zfcg',
    'neimenggu_bayannaoer_zfcg',
    'shandong_liaocheng_zfcg',
    'shandong_qingdao_zfcg',
    'xinjiang_changji_zfcg',
    'xizang_shannan_zfcg',
    'ningxia_yinchuan_zfcg',
    'xizang_shannan_zfcg',
    'xinjiang_changji_1_zfcg',
    'guangdong_zhongshan_gcjs',
    'hebei_langfang_gcjs',
    'hunan_huaihua_gcjs',
    'jilin_jilinsheng_gcjs',
    'jilin_tonghua_gcjs',
    'liaoning_shenyang_gcjs',
    'neimenggu_neimenggusheng_gcjs',
    'shanxi_baoji_gcjs',
    'shanxi1_taiyuan_gcjs',
    'shanxi1_xinzhou_1_gcjs',
    'jiangsu_wuxi_zfcg',
    'shanxi1_taiyuan_zfcg',
    'qycg_www_namkwong_com_mo',
    'qycg_www_sinochemitc_com',
    'gansu_gansusheng_gcjs',
    'anhui_wuhu_zfcg',
    'guangxi_baise_zfcg',
    'sichuan_mianyang_zfcg',
    'xinjiang_hetian_zfcg',
    'qycg_www_dlztb_com',
    'fujian_zhangzhou_gcjs',
    'henan_kaifeng_gcjs',
    'hunan_changsha_gcjs',
    'hunan_changsha_1_gcjs',
    'hunan_shaoyang_gcjs',
    'hunan_wugang_gcjs',
    'hunan_yueyang_gcjs',
    'jiangxi_jiujiang_gcjs',
    'shandong_jinan_gcjs',
    'shandong_linyi_gcjs',
    'fujian_nanping_zfcg',
    'henan_hebi_zfcg',
    'henan_henansheng_zfcg',
    'henan_jiaozuo_zfcg',
    'henan_kaifeng_zfcg',
    'henan_luohe_zfcg',
    'henan_luoyang_zfcg',
    'henan_nanyang_zfcg',
    'henan_pingdingshan_zfcg',
    'henan_puyang_zfcg',
    'henan_sanmenxia_zfcg',
    'henan_shangqiu_zfcg',
    'henan_xinxiang_zfcg',
    'henan_xinyang_zfcg',
    'henan_xuchang_zfcg',
    'henan_zhengzhou_zfcg',
    'henan_zhoukou_zfcg',
    'henan_zhumadian_zfcg',
    'hunan_changsha_zfcg',
    'hunan_xiangtan_zfcg',
    'shandong_yantai_zfcg',
    'qycg_dzzb_ciesco_com_cn',
    'qycg_epp_ctg_com_cn',
    'qycg_jzcg_cfhi_com',
    'qycg_thzb_crsc_cn',
    'qycg_www_bidding_csg_cn',
    'qycg_www_china_tender_com_cn',
    'qycg_www_chinabidding_com',
    'qycg_www_dlzb_com',
    'qycg_www_dlzb_com_c1608',
    'qycg_www_ngecc_com',
    'fujian_fuqing_gcjs',
    'fujian_fuzhou_gcjs',
    'fujian_quanzhou_gcjs',
    'guangdong_shantou_gcjs',
    'guangdong_shaoguan_gcjs',
    'guangdong_shenzhen_gcjs',
    'guangxi_guangxisheng_gcjs',
    'hebei_hebeisheng_gcjs',
    'heilongjiang_haerbin_gcjs',
    'heilongjiang_qqhaer_gcjs',
    'heilongjiang_heilongjiangsheng_gcjs',
    'jiangsu_nantong_gcjs',
    'shandong_heze_gcjs',
    'shanxi1_changzhi_gcjs',
    'shanxi1_datong_gcjs',
    'guangdong_guangzhou_zfcg',
    'hainan_sanya_zfcg',
    'hubei_ezhou_zfcg',
    'hubei_wuhan_zfcg',
    'jiangsu_jiangsusheng_zfcg',
    'jiangsu_suqian_zfcg',
    'jiangsu_yangzhou_zfcg',
    'jilin_jilinsheng_zfcg',
    'liaoning_shenyang_zfcg',
    'shandong_dongying_zfcg',
    'shandong_laiwu_zfcg',
    'shandong_linyi_zfcg',
    'tianjin_tianjinshi_zfcg',
    'qycg_ec1_mcc_com_cn',
    'qycg_ec_chalieco_com',
    'qycg_ecp_sgcc_com_cn',
    'qycg_eps_sdic_com_cn',
    'qycg_fwgs_sinograin_com_cn',
    'qycg_gs_coscoshipping_com',
    'qycg_srm_crland_com_cn',
    'qycg_uat_ec_chng_com_cn',
    'qycg_www_cnpcbidding_com',
    'qycg_www_gmgitc_com',
    'zhejiang_hangzhou_gcjs',
    'hunan_hunansheng_zfcg',
    'hunan_zhuzhou_zfcg',
    'guangxi_qinzhou_zfcg',
    'hunan_chenzhou_zfcg',
    'hunan_hengyang_zfcg',
    'hunan_loudi_zfcg',
    'hunan_yiyang_zfcg',
    'hunan_yueyang_zfcg',
    'hunan_zhangjiajie_zfcg',
    'jiangxi_shangrao_gcjs',
    'chongqing_chongqingshi_zfcg',
    'qycg_etp_fawiec_com',
    'qycg_bidding_crmsc_com_cn']

not_ggzy_list_page_nokey = ['guangdong_shaoguan_gcjs',
                            'guangdong_guangdongsheng_gcjs',
                            'guangdong_shenzhen_zfcg',
                            'guangdong_shenzhen_zfcg',
                            'liaoning_wafangdian_zfcg',
                            'qycg_www_chdtp_com',
                            ]

not_ggzy_list_page_nospace = ['guangxi_beihai_gcjs',
                              'guangxi_fangchenggang_gcjs',
                              'shanxi1_yuncheng_zfcg',
                              ]

not_ggzy_not_exists_list = [
    # 不存在数据表的非ggzy的quyu
    'hebei_xingtai_gcjs',
    'henan_puyang_gcjs',
    'shanxi1_linfen_gcjs',
    'sichuan_mianyang_gcjs',
    'shandong_weihai_zfcg',
    'xinjiang_akesu_zfcg',
    'xinjiang_kashi_zfcg',
    'xinjiang_kelamayi_zfcg',
    'xinjiang_xinjiangsheng_zfcg',
    'xinjiang_tacheng_zfcg',
    'xinjiang_tulufan_zfcg',
    'xinjiang_yili_zfcg',
    'qycg_www_chinabidding_com_total',

    #    # 有问题的非ggzy的quyu
    #    'qycg_etp_fawiec_com',
    #    'qycg_syhggs_dlzb_com',
    #    'qycg_sytrq_dlzb_com',
    #    'qycg_zgdxjt_dlzb_com',
    #    'qycg_ysky_dlzb_com',
    #    'qycg_zgdzxx_dlzb_com',
    #    'qycg_zghkgy_dlzb_com',
    #    'qycg_zghkyl_dlzb_com',
    #    'qycg_zgyy_dlzb_com',

    # 'guangdong_yangjiang_gcjs',
    # 'guangxi_baise_gcjs',
    # 'heilongjiang_qqhaer_gcjs',
    # 'hunan_hunansheng_gcjs',
    # 'jiangsu_yangzhou_gcjs',
    # 'jiangsu_yangzhou_gcjs',
    # 'jiangxi_pingxiang_gcjs',
    # 'jiangxi_nanchang_gcjs',
    # 'jiangxi_shangrao_gcjs',
    # 'jilin_changchun_gcjs',
    # 'liaoning_dalian_gcjs',
    # 'ningxia_ningxiasheng_gcjs',
    # 'shandong_shandongsheng_gcjs',
    # 'shanxi_hanzhong_gcjs',
    # 'shanxi_xian_gcjs',
    # 'shanxi1_xinzhou_gcjs',
    # 'sichuan_chengdu_gcjs',
    # 'xinjiang_atushi_gcjs',
    # 'xinjiang_bole_gcjs',
    # 'xinjiang_changji_gcjs',
    # 'xinjiang_xinjiangsheng_gcjs',
    # 'xinjiang_kashi_gcjs',
    # 'xinjiang_tacheng_gcjs',
    # 'xinjiang_wulumuqi_gcjs',
    # 'xinjiang_yining_gcjs',
    # 'zhejiang_zhejiangsheng_gcjs',
    # 'anhui_anqing_zfcg',
    # 'chongqing_chongqingshi_zfcg',
    # 'fujian_sanming_zfcg',
    # 'guangdong_zhongshan_zfcg',
    # 'guangxi_guigang_zfcg',
    # 'jiangsu_suzhou_zfcg',
    # 'jiangsu_taizhou_zfcg',
    # 'jiangxi_pingxiang_zfcg',
    # 'neimenggu_neimenggusheng_zfcg',
    # 'ningxia_ningxiasheng_zfcg',
    # 'shandong_dezhou_zfcg',
    # 'shandong_shandong_zfcg',
    # 'xinjiang_wulumuqi_zfcg',
    # 'zhejiang_ningbo_zfcg',
    # 'zhejiang_wenzhou_zfcg',
    # 'qycg_baowu_ouyeelbuy_com',
    # 'qycg_bidding_ceiec_com_cn',
    # 'qycg_dfqcgs_dlzb_com',
    # 'qycg_ec_ccccltd_cn',
    # 'qycg_ec_ceec_net_cn',
    # 'qycg_ecp_cgnpc_com_cn',
    # 'qycg_etp_fawiec_com',
    # 'qycg_syhggs_dlzb_com',
    # 'qycg_sytrq_dlzb_com',
    # 'qycg_www_cgdcbidding_com',
    # 'qycg_www_dlswzb_com',
    # 'qycg_zgdxjt_dlzb_com',
    # 'qycg_ysky_dlzb_com',
    # 'qycg_zgdzxx_dlzb_com',
    # 'qycg_zghkgy_dlzb_com',
    # 'qycg_zghkyl_dlzb_com',
    # 'qycg_zgyy_dlzb_com',

]

ggzy_list_page_time = [
    'anhui_anqing_ggzy',
    'anhui_bozhou_ggzy',
    'anhui_huainan_ggzy',
    'anhui_bengbu_ggzy',
    'anhui_chaohu_ggzy',
    'anhui_chizhou_ggzy',
    'anhui_chuzhou_ggzy',
    'anhui_fuyang_ggzy',
    'anhui_huaibei_ggzy',
    'anhui_huangshan_ggzy',
    'anhui_maanshan_ggzy',
    'anhui_suzhou_ggzy',
    'anhui_tongling_ggzy',
    'chongqing_chongqingshi_ggzy',
    'anhui_xuancheng_ggzy',
    'fujian_fuqing_ggzy',
    'fujian_longyan_ggzy',
    'fujian_ningde_ggzy',
    'fujian_quanzhou_ggzy',
    'fujian_wuyishan_ggzy',
    'fujian_putian_ggzy',
    'fujian_sanming_ggzy',
    'fujian_yongan_ggzy',
    'fujian_shaowu_ggzy',
    'fujian_zhangzhou_ggzy',
    'gansu_zhangye_ggzy',
    'gansu_longnan_ggzy',
    'gansu_qingyang_ggzy',
    'guangdong_dongguan_ggzy',
    'guangdong_guangdongsheng_ggzy',
    'guangdong_heyuan_ggzy',
    'guangdong_huizhou_ggzy',
    'guangdong_jiangmen_ggzy',
    'guangdong_jieyang_ggzy',
    'guangdong_lianzhou_ggzy',
    'guangdong_maoming_ggzy',
    'guangdong_meizhou_ggzy',
    'guangdong_nanxiong_ggzy',
    'guangdong_qingyuan_ggzy',
    'guangdong_shanwei_ggzy',
    'guangdong_shaoguan_ggzy',
    'guangdong_sihui_ggzy',
    'guangdong_yangjiang_ggzy',
    'guangdong_yingde_ggzy',
    'guangdong_yunfu_ggzy',
    'guangdong_zhanjiang_ggzy',
    'guangdong_zhaoqing_ggzy',
    'guangdong_shantou_ggzy',
    'guangdong_zhuhai_ggzy',
    'guangxi_baise_ggzy',
    'guangxi_beihai_ggzy',
    'guangxi_chongzuo_ggzy',
    'guangxi_fangchenggang_ggzy',
    'guangxi_guangxisheng_ggzy',
    'guangxi_guigang_ggzy',
    'guangxi_guilin_ggzy',
    'guangxi_hechi_ggzy',
    'guangxi_laibin_ggzy',
    'guangxi_liuzhou_ggzy',
    'guangxi_nanning_ggzy',
    'guangxi_qinzhou_ggzy',
    'guangxi_wuzhou_ggzy',
    'guizhou_anshun_ggzy',
    'guizhou_bijie_ggzy',
    'guizhou_guiyang_ggzy',
    'guizhou_qiannan_ggzy',
    'guizhou_qianxi_ggzy',
    'guizhou_liupanshui_ggzy',
    'guizhou_tongren_ggzy',
    'hainan_danzhou_ggzy',
    'hainan_dongfang_ggzy',
    'hainan_haikou_ggzy',
    'hainan_hainansheng_ggzy',
    'hainan_sansha_ggzy',
    'hainan_qionghai_ggzy',
    'hainan_sanya_ggzy',
    'heilongjiang_daqing_ggzy',
    'heilongjiang_hegang_ggzy',
    'henan_anyang_ggzy',
    'henan_dengfeng_ggzy',
    'henan_gongyi_ggzy',
    'henan_hebi_ggzy',
    'henan_linzhou_ggzy',
    'henan_luohe_ggzy',
    'henan_luoyang_ggzy',
    'henan_nanyang_ggzy',
    'henan_puyang_ggzy',
    'henan_sanmenxia_ggzy',
    'henan_shangqiu_ggzy',
    'henan_weihui_ggzy',
    'henan_xinxiang_ggzy',
    'henan_xinyang_ggzy',
    'henan_xinzheng_ggzy',
    'henan_yanshi_ggzy',
    'henan_zhengzhou_ggzy',
    'henan_zhoukou_ggzy',
    'henan_zhumadian_ggzy',
    'hubei_huangshi_ggzy',
    'hubei_jingmen_ggzy',
    'hubei_suizhou_ggzy',
    'hunan_changde_ggzy',
    'hunan_changsha_ggzy',
    'hunan_chenzhou_ggzy',
    'hunan_hengyang_ggzy',
    'hunan_huaihua_ggzy',
    'hunan_liling_ggzy',
    'hunan_liuyang_ggzy',
    'hunan_shaoyang_ggzy',
    'hunan_xiangtan_ggzy',
    'hunan_yiyang_ggzy',
    'hunan_yongzhou_ggzy',
    'hunan_zhuzhou_ggzy',
    'jiangsu_changshu_ggzy',
    'jiangsu_changzhou_ggzy',
    'jiangsu_danyang_ggzy',
    'jiangsu_dongtai_ggzy',
    'jiangsu_huaian_ggzy',
    'jiangsu_jiangsusheng_ggzy',
    'jiangsu_jiangyin_ggzy',
    'jiangsu_kunshan_ggzy',
    'jiangsu_lianyungang_ggzy',
    'jiangsu_nanjing_ggzy',
    'jiangsu_nantong_ggzy',
    'jiangsu_suqian_ggzy',
    'jiangsu_suzhou_ggzy',
    'jiangsu_taizhou_ggzy',
    'jiangsu_xinyi_ggzy',
    'jiangsu_xuzhou_ggzy',
    'jiangsu_yangzhou_ggzy',
    'jiangsu_zhangjiagang_ggzy',
    'jiangsu_zhenjiang_ggzy',
    'jiangxi_ganzhou_ggzy',
    'jiangxi_jian_ggzy',
    'jiangxi_jiangxisheng_ggzy',
    'jiangxi_jingdezhen_ggzy',
    'jiangxi_jinggangshan_ggzy',
    'jiangxi_lushan_ggzy',
    'jiangxi_ruichang_ggzy',
    'jiangxi_ruijin_ggzy',
    'jiangxi_yingtan_ggzy',
    'jilin_baicheng_ggzy',
    'liaoning_anshan_ggzy',
    'liaoning_chaoyang_ggzy',
    'liaoning_dalian_ggzy',
    'liaoning_dandong_ggzy',
    'liaoning_donggang_ggzy',
    'liaoning_fuxin_ggzy',
    'liaoning_huludao_ggzy',
    'liaoning_liaoyang_ggzy',
    'liaoning_panjin_ggzy',
    'liaoning_jinzhou_ggzy',
    'neimenggu_alashan_ggzy',
    'neimenggu_baotou_ggzy',
    'neimenggu_bayannaoer_ggzy',
    'neimenggu_eeduosi_ggzy',
    'neimenggu_huhehaote_ggzy',
    'neimenggu_hulunbeier_ggzy',
    'neimenggu_manzhouli_ggzy',
    'neimenggu_neimenggusheng_ggzy',
    'neimenggu_tongliao_ggzy',
    'neimenggu_wuhai_ggzy',
    'neimenggu_wulanchabu_ggzy',
    'neimenggu_chifeng_ggzy',
    'neimenggu_xinganmeng_ggzy',
    'qinghai_xining_ggzy',
    'shandong_anqiu_ggzy',
    'shandong_binzhou_ggzy',
    'shandong_feicheng_ggzy',
    'shandong_jinan_ggzy',
    'shandong_linqing_ggzy',
    'shandong_rizhao_ggzy',
    'shandong_rongcheng_ggzy',
    'shandong_shandongsheng_ggzy',
    'shandong_taian_ggzy',
    'shandong_weifang_ggzy',
    'shandong_xintai_ggzy',
    'shandong_yucheng_ggzy',
    'shandong_dezhou_ggzy',
    'shandong_weihai_ggzy',
    'shandong_zibo_ggzy',
    'shanxi_shanxisheng_ggzy',
    'shanxi_weinan_ggzy',
    'shanxi_xianyang_ggzy',
    'shanxi_yanan_ggzy',
    'sichuan_bazhong_ggzy',
    'sichuan_dazhou_ggzy',
    'sichuan_deyang_ggzy',
    'sichuan_dujiangyan_ggzy',
    'sichuan_guangan_ggzy',
    'sichuan_guanghan_ggzy',
    'sichuan_guangyuan_ggzy',
    'sichuan_leshan_ggzy',
    'sichuan_luzhou_ggzy',
    'sichuan_meishan_ggzy',
    'sichuan_nanchong_ggzy',
    'sichuan_pengzhou_ggzy',
    'sichuan_qionglai_ggzy',
    'sichuan_shifang_ggzy',
    'sichuan_sichuansheng_ggzy',
    'sichuan_sichuansheng_1_ggzy',
    'sichuan_suining_ggzy',
    'sichuan_wanyuan_ggzy',
    'sichuan_yaan_ggzy',
    'xinjiang_akesu_ggzy',
    'xinjiang_wulumuqi_ggzy',
    'xinjiang_xinjiangsheng_ggzy',
    'xizang_xizangsheng_ggzy',
    'yunnan_kunming_ggzy',
    'zhejiang_cixi_ggzy',
    'zhejiang_huzhou_ggzy',
    'zhejiang_jiaxing_ggzy',
    'zhejiang_jinhua_ggzy',
    'zhejiang_lishui_ggzy',
    'zhejiang_ningbo_ggzy',
    'zhejiang_pinghu_ggzy',
    'zhejiang_ruian_ggzy',
    'zhejiang_shaoxing_ggzy',
    'zhejiang_shengzhou_ggzy',
    'zhejiang_wenzhou_ggzy',
    'zhejiang_yiwu_ggzy',
    'zhejiang_yueqing_ggzy',
    'zhejiang_zhejiangsheng_ggzy',
    'zhejiang_zhoushan_ggzy',
    'zhejiang_zhuji_ggzy',
    'beijing_beijingshi_ggzy'
]

ggzy_list_page_notime = [
    'anhui_hefei_ggzy',
    'anhui_luan_ggzy',
    'anhui_wuhu_ggzy',
    'chongqing_yongchuan_ggzy',
    'fujian_fuzhou_ggzy',
    'fujian_xiamen_ggzy',
    'fujian_jianou_ggzy',
    'gansu_lanzhou_ggzy',
    'guangdong_zhongshan_ggzy',
    'guizhou_qiandong_ggzy',
    'hebei_hebeisheng_ggzy',
    'heilongjiang_heilongjiangsheng_ggzy',
    'heilongjiang_yichun_ggzy',
    'henan_kaifeng_ggzy',
    'henan_mengzhou_ggzy',
    'henan_pingdingshan_ggzy',
    'henan_ruzhou_ggzy',
    'henan_wugang_ggzy',
    'henan_xinmi_ggzy',
    'henan_yongcheng_ggzy',
    'hubei_dangyang_ggzy',
    'hubei_enshi_ggzy',
    'hubei_lichuan_ggzy',
    'hubei_xiaogan_ggzy',
    'hubei_yichang_ggzy',
    'hubei_yidu_ggzy',
    'hunan_yueyang_ggzy',
    'hunan_zhangjiajie_ggzy',
    'jiangxi_dexing_ggzy',
    'jiangxi_fengcheng_ggzy',
    'jiangxi_fuzhou_ggzy',
    'jiangxi_nanchang_ggzy',
    'jiangxi_xinyu_ggzy',
    'jiangxi_yichun_ggzy',
    'jiangxi_zhangshu_ggzy',
    'jilin_baishan_ggzy',
    'jilin_changchun_ggzy',
    'jilin_jilinshi_ggzy',
    'jilin_siping_ggzy',
    'jilin_songyuan_ggzy',
    'jilin_jilinshi_ggzy',
    'jilin_tonghua_ggzy',
    'ningxia_ningxiasheng_ggzy',
    'ningxia_yinchuan_ggzy',
    'qinghai_qinghaisheng_ggzy',
    'shandong_heze_ggzy',
    'shandong_jiaozhou_ggzy',
    'shandong_laiwu_ggzy',
    'shandong_linyi_ggzy',
    'shandong_pingdu_ggzy',
    'shandong_rushan_ggzy',
    'shandong_zaozhuang_ggzy',
    'sichuan_jiangyou_ggzy',
    'sichuan_yibin_ggzy',
    'xizang_lasa_ggzy',
    'zhejiang_longquan_ggzy',
    'zhejiang_yuhuan_ggzy',
    'zhejiang_dongyang_ggzy',
    'guangxi_hezhou_ggzy',
    'yunnan_tengchong_ggzy',
    'fujian_nanan_ggzy',
    'fujian_nanping_ggzy',
    'gansu_baiyin_ggzy',
    'gansu_jiuquan_ggzy',
    'gansu_pingliang_ggzy',
    'gansu_wuwei_ggzy',
    'gansu_longnan_ggzy',
    'gansu_gansusheng_ggzy',
    'gansu_tianshui_ggzy',
    'gansu_dingxi_ggzy',
    'gansu_jiayuguan_ggzy',
    'guangdong_chaozhou_ggzy',
    'heilongjiang_qiqihaer_ggzy',
    'henan_xuchang_ggzy',
    'henan_jiaozhuo_ggzy',
    'henan_jiyuan_ggzy',
    'henan_qinyang_ggzy',
    'hubei_shiyan_ggzy',
    'hubei_xiangyang_ggzy',
    'hunan_loudi_ggzy',
    'hunan_yuanjiang_ggzy',
    'jiangxi_ganzhou_ggzy',
    'jiangxi_shangrao_ggzy',
    'liaoning_haicheng_ggzy',
    'liaoning_liaoningsheng_ggzy',
    'liaoning_yingkou_ggzy',
    'shandong_leling_ggzy',
    'shandong_qingdao_ggzy',
    'shandong_qufu_ggzy',
    'shandong_jining_ggzy',
    'shandong_liaocheng_ggzy',
    'shandong_zoucheng_ggzy',
    'shandong_tengzhou_ggzy',
    'sichuan_longchang_ggzy',
    'sichuan_mianyang_ggzy',
    'sichuan_chengdu_ggzy',
    'sichuan_chongzhou_ggzy',
    'sichuan_jianyang_ggzy',
    'sichuan_mianyang_1_ggzy',
    'xizang_rikaze_ggzy',
    'yunnan_tengchong_ggzy',
    'zhejiang_linhai_ggzy',
    'zhejiang_hangzhou_ggzy',
    'yunnan_yunnansheng_ggzy',
]

ggzy_list_page_yunan = ['yunnan_baoshan_ggzy',
                        'yunnan_chuxiong_ggzy',
                        'yunnan_wenshan_ggzy',
                        'yunnan_xishuangbanna_ggzy',
                        'yunnan_yunnan2_ggzy',
                        'yunnan_yuxi_ggzy',
                        'yunnan_zhaoton_ggzyg'
                        ]

ggzy_not_exists_list = [
    # 不存在数据的quyu
    'jiangsu_yancheng_ggzy',  # 网站挂了
    'liaoning_beizhen_ggzy',  # 网站挂了
    'liaoning_fushun_ggzy',  # 网站挂了
    'shandong_dongying_ggzy',
    'tianjin_tianjin_ggzy',
    'shanghai_shanghai_ggzy'

    # # 有问题的quyu
    # 'fujian_fujiansheng_ggzy',
    # 'guizhou_guizhousheng_ggzy',
    # 'hubei_huanggang_ggzy',
    # 'hubei_wuhan_ggzy',
    # 'liaoning_shenyang_ggzy',
    # 'liaoning_tieling_ggzy',
    # 'neimenggu_xilinguolemeng_ggzy',
    # 'shanxi_xian_ggzy',
    # 'sichuan_neijiang_ggzy',
    # 'sichuan_panzhihua_ggzy',
    # 'zhejiang_taizhou_ggzy',
    # 'zhejiang_tongxia_ggzyn'
    # 'jiangsu_wuxi_ggzy',
    # 'yunnan_lijiang_ggzy',
    # 'yunnan_puer_ggzy',
    # 'yunnan_dali_ggzy',
    # 'yunnan_honghe_ggzy',
    # 'yunnan_lincang_ggzy',

]


# 提取特殊的时间
def strptime_transfrom_CST(page):
    soup = BeautifulSoup(page, 'lxml')
    p = "(?:信息时间|信息日期|信息发布日期|发稿时间|发布时间|生成日期)[：:\s]{,4}(.{0,20}CST.{0,5})"

    txt = soup.text

    a = re.findall(p, txt)
    if a != []:
        a = time.strptime(a[0], '%a %b %d %H:%M:%S CST %Y')
        a = time.strftime('%Y-%m-%d', a)
        return a

    return None


def strptime_transfrom_nokey(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = soup.text
    parterns = [
        "(?:更新时间|发布时间|发布|加入时间|信息提供日期)[：:]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})",
        "(20[0-2][0-9])[\-\.年\\/]{0,1}([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]{0,1}([0-9]{,2})(?:发布)"
    ]
    for p in parterns:
        a = re.findall(p, txt.replace('varstrvarstr1', ''))
        if a != []:
            return '-'.join(a[0])
    return None


def strptime_transfrom_nofg(page):
    # 时间没有分隔。
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    patterns = ["(?:变更日期时间|更新时间|发布时间|发布日期)[：:]([0-9]{8})", "(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2}).{1}公布"]
    for p in patterns:
        a = re.findall(p, txt)
        if a != []:
            return '-'.join([a[0][:4], a[0][4:6], a[0][6:]])
        return None


##不去掉空格
def strptime_transfrom_nospace(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = soup.text
    p = "(?:更新时间|发布时间|公示开始时间)[：:]{0,1}.{0,2}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt)
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
    #    print('----',txt)
    if list1 != []:
        return ('-'.join([list1[0], list1[1], list1[2]]))
    return None


def strptime_transfromgs(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:信息时间|信息日期|信息发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期|公示日期|公示时间|公告时间)[:：]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
    # print(txt)
    a = re.findall(p, txt)
    #    print('----',txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def strptime_transfromrq(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:日期|信息时间|信息日期|信息发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期)[:：]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
    # print(txt)
    a = re.findall(p, txt)
    #    print('----',txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def not_ggzy_extime_all(page, ggstart_time, quyu):
    if quyu in not_ggzy_list_page_time:
        if extime(page) is not None:
            return extime(page)
        elif strptime_transfrom_CST(page):
            return strptime_transfrom_CST(page)
        elif ggstart_time is not None:
            return ggstart_time
    elif quyu in not_ggzy_list_page_notime:
        if ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in not_ggzy_list_page_nokey:
        # 没有标准头部时间
        if strptime_transfrom_nokey(page) is not None:
            return strptime_transfrom_nokey(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in not_ggzy_list_page_nospace:
        if strptime_transfrom_nospace(page) is not None:
            # print(strptime_transfrom_nospace(page))
            return strptime_transfrom_nospace(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in ['heilongjiang_qqhaer_gcjs',
                  'hunan_hunansheng_gcjs',
                  'jiangsu_yangzhou_gcjs',
                  'jiangxi_pingxiang_gcjs',
                  'jilin_changchun_gcjs',
                  'xinjiang_atushi_gcjs',
                  'shandong_shandongsheng_gcjs',
                  'shanxi_hanzhong_gcjs',
                  'shanxi_xian_gcjs',
                  'sichuan_chengdu_gcjs',
                  'anhui_anqing_zfcg',
                  'fujian_sanming_zfcg',
                  'jiangsu_taizhou_zfcg',
                  'jiangxi_pingxiang_zfcg',
                  'neimenggu_neimenggusheng_zfcg',
                  'shandong_dezhou_zfcg',
                  'qycg_baowu_ouyeelbuy_com',
                  'qycg_bidding_ceiec_com_cn',
                  'qycg_ecp_cgnpc_com_cn',
                  'qycg_syhggs_dlzb_com',
                  'qycg_sytrq_dlzb_com',
                  'qycg_www_cgdcbidding_com',
                  'qycg_zgdxjt_dlzb_com',
                  'qycg_ysky_dlzb_com',
                  'qycg_zgdzxx_dlzb_com',
                  'qycg_zghkgy_dlzb_com',
                  'qycg_zghkyl_dlzb_com',
                  'qycg_zgyy_dlzb_com',
                  'guangdong_yangjiang_gcjs',
                  'jiangxi_nanchang_gcjs',
                  'ningxia_ningxiasheng_gcjs',
                  'shanxi1_xinzhou_gcjs',
                  'xinjiang_atushi_gcjs',
                  'xinjiang_bole_gcjs',
                  'xinjiang_changji_gcjs',
                  'xinjiang_xinjiangsheng_gcjs',
                  'xinjiang_kashi_gcjs',
                  'xinjiang_tacheng_gcjs',
                  'xinjiang_wulumuqi_gcjs',
                  'xinjiang_yining_gcjs',
                  'zhejiang_zhejiangsheng_gcjs',
                  'guangdong_zhongshan_zfcg',
                  'guangxi_guigang_zfcg',
                  'jiangsu_suzhou_zfcg',
                  'ningxia_ningxiasheng_zfcg',
                  'shandong_shandongsheng_zfcg',
                  'xinjiang_wulumuqi_zfcg',
                  'zhejiang_ningbo_zfcg',
                  'guangxi_baise_gcjs',
                  'zhejiang_wenzhou_zfcg',
                  'qycg_dfqcgs_dlzb_com',
                  'qycg_ec_ccccltd_cn',
                  'qycg_ec_ceec_net_cn',
                  'qycg_www_dlswzb_com', ]:
        if quyu in ['heilongjiang_qqhaer_gcjs',
                    'hunan_hunansheng_gcjs',
                    'jiangsu_yangzhou_gcjs',
                    'jiangxi_pingxiang_gcjs',
                    'jilin_changchun_gcjs',
                    'xinjiang_atushi_gcjs',
                    'shandong_shandongsheng_gcjs',
                    'shanxi_hanzhong_gcjs',
                    'shanxi_xian_gcjs',
                    'sichuan_chengdu_gcjs',
                    'anhui_anqing_zfcg',
                    'fujian_sanming_zfcg',
                    'jiangsu_taizhou_zfcg',
                    'jiangxi_pingxiang_zfcg',
                    'neimenggu_neimenggusheng_zfcg',
                    'shandong_dezhou_zfcg',
                    'qycg_baowu_ouyeelbuy_com',
                    'qycg_bidding_ceiec_com_cn',
                    'qycg_ecp_cgnpc_com_cn',
                    'qycg_syhggs_dlzb_com',
                    'qycg_sytrq_dlzb_com',
                    'qycg_www_cgdcbidding_com',
                    'qycg_zgdxjt_dlzb_com',
                    'qycg_ysky_dlzb_com',
                    'qycg_zgdzxx_dlzb_com',
                    'qycg_zghkgy_dlzb_com',
                    'qycg_zghkyl_dlzb_com',
                    'qycg_zgyy_dlzb_com', ]:
            if quyu in ['hunan_hunansheng_gcjs']:
                if strptime_transfromrq(page):
                    return strptime_transfromrq(page)
                return ggstart_time
            elif quyu in ['jiangsu_yangzhou_gcjs']:
                if strptime_transfrom_nospace(page):
                    return (strptime_transfrom_nospace(page))
                return ggstart_time
            elif quyu in ['jiangsu_yangzhou_gcjs',
                          'qycg_ec_ceec_net_cn']:
                if strptime_transfromgs(page):
                    return (strptime_transfromgs(page))
                return ggstart_time
            elif quyu in [
                'hunan_hunansheng_gcjs',
            ]:
                if strptime_transfromrq(page):
                    return strptime_transfromrq(page)
                return None
            elif extime(page) is not None:
                return extime(page)
            else:
                return None
        else:
            if quyu in ['xinjiang_wulumuqi_gcjs']:
                if extime(page) is not None:
                    return extime(page)
                elif strptime_transfrom_nospace(page):
                    return (strptime_transfrom_nospace(page))
                return None
            elif quyu in ['guangxi_baise_gcjs', 'shanxi1_xinzhou_gcjs']:
                if strptime_transfromsj(page):
                    return (strptime_transfromsj(page))
                return None
            else:
                return strptime_transfrom_nokey(page)
    elif quyu in ['henan_sanmenxia_gcjs',
                  'sichuan_bazhong_gcjs',
                  'sichuan_sichuansheng_gcjs',
                  'anhui_huainan_zfcg',
                  'fujian_nanping1_zfcg',
                  'guangdong_guangdongsheng_zfcg',
                  'hubei_jingmen_zfcg',
                  'hubei_wuhan_1_zfcg',
                  'jiangsu_yancheng_zfcg',
                  'neimenggu_baotou_zfcg',
                  'neimenggu_huhehaote_zfcg',
                  'qycg_www_crpsz_com',
                  'qycg_zgyy_dlzb_com',
                  'qycg_zghkyl_dlzb_com',
                  'qycg_zghkgy_dlzb_com',
                  'qycg_zgdzxx_dlzb_com',
                  'qycg_ysky_dlzb_com',
                  'qycg_zgdxjt_dlzb_com',
                  'qycg_www_dlswzb_com',
                  'qycg_sytrq_dlzb_com',
                  'qycg_syhggs_dlzb_com',
                  'guangdong_dongguan_gcjs',
                  'jinlin_jinlinsheng_gcjs',
                  'qycg_b2b_10086_cn',
                  ]:
        if quyu in ['guangdong_guangdongsheng_zfcg', ]:
            if strptime_transfromgg_guangdong_guangdongsheng(page):
                return (strptime_transfromgg_guangdong_guangdongsheng(page))
            return None
        if quyu in ['hubei_wuhan_1_zfcg']:
            if extime(page):
                return (extime(page))
            return None
        if quyu in ['henan_sanmenxia_gcjs',
                    'sichuan_bazhong_gcjs',
                    ]:
            if strptime_transfromsj(page):
                return (strptime_transfromsj(page))
            return ggstart_time
        elif extime(page):
            return extime(page)
        else:
            return ggstart_time


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


# 大部分区域提取时间的格式
def extime(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:信息时间|信息日期|更新时间|发稿时间|发文时间|发文日期|发布时间|发布日期|录入时间|生成时间|生成日期|公示期为)[：:](20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt.replace('documentwrite', ''))
    # print(a)
    if a != []:
        return '-'.join(a[0])
    return None


def strptime_transfrom_yunan(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = '(?:发布时间|提交时间|公示时间)[：:]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})'

    a = re.findall(p, txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def strptime_transfrom_jiangxi(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/', '', soup.text.strip())
    p = "\[(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})\]"

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


# def strptime_transfromgg_question1(page):
#    soup = BeautifulSoup(page, 'lxml')
#    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
#    p = "(?:信息时间|信息日期|发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期|公示期为)(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
#    # print(txt)
#    a = re.findall(p, txt)
#    #    print('----',txt)
#    if a != []:
#        return ('-'.join(a[0]))
#    return None


def strptime_transfromsj(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:时间|信息日期|信息发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期)[:：]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
    # print(txt)
    a = re.findall(p, txt)
    #    print('----',txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def ggzy_extime_all(page, ggstart_time, quyu):
    if quyu in ggzy_list_page_time:
        if extime(page) is not None:
            return extime(page)
        elif strptime_transfrom_CST(page):
            return strptime_transfrom_CST(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in ggzy_list_page_notime:
        if ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in ggzy_list_page_yunan:
        if strptime_transfrom_yunan(page) is not None:
            return strptime_transfrom_yunan(page)
        elif ggstart_time is not None:
            return extime(page)
        else:
            return None
    elif quyu in ['jiangxi_gaoan_ggzy']:
        if strptime_transfrom_jiangxi(page) is not None:
            return strptime_transfrom_jiangxi(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None

    # ggstart_time时间有问题
    elif quyu in ['fujian_fujiansheng_ggzy',
                  'guizhou_guizhousheng_ggzy',
                  'hubei_huanggang_ggzy',
                  'hubei_wuhan_ggzy',
                  'liaoning_shenyang_ggzy',
                  'liaoning_tieling_ggzy',
                  'neimenggu_xilinguolemeng_ggzy',
                  'shanxi_xian_ggzy',
                  'sichuan_panzhihua_ggzy',
                  'zhejiang_tongxiang_ggzy',
                  'jiangsu_wuxi_ggzy',
                  'yunnan_lijiang_ggzy',
                  'yunnan_puer_ggzy',
                  'yunnan_dali_ggzy',
                  'yunnan_honghe_ggzy',
                  'yunnan_lincang_ggzy',
                  ]:
        if quyu in ['yunnan_lijiang_ggzy',
                    'yunnan_puer_ggzy',
                    'yunnan_dali_ggzy',
                    'yunnan_honghe_ggzy',
                    'yunnan_lincang_ggzy',
                    ]:
            if strptime_transfrom_yunan(page):
                return (strptime_transfrom_yunan(page))
            return None
        elif quyu in ['liaoning_shenyang_ggzy']:
            if strptime_transfrom_yue_r_n(page) is not None:
                return strptime_transfrom_yue_r_n(page)
            else:
                return None
        elif extime(page) is not None:
            return extime(page)
        else:
            return None
    elif quyu in ['gansu_gansusheng_ggzy',
                  'gansu_jiayuguan_ggzy',
                  'gansu_tianshui_ggzy',
                  'guangdong_foshan_ggzy',
                  'guizhou_zunyi_ggzy',
                  'hunan_hunansheng_ggzy',
                  'jilin_liaoyuan_ggzy',
                  'liaoning_benxi_ggzy',
                  'qycg_www_cgdcbidding_com',
                  'shanxi_shanxisheng_ggzy',
                  'xinjiang_kezhou_ggzy',
                  'yunnan_dehong_ggzy',
                  'jiangsu_yizheng_ggzy',

                  ]:
        if quyu in ['guangdong_foshan_ggzy']:
            if strptime_transfromsj(page):
                return (strptime_transfromsj(page))
            return ggstart_time
        if quyu in ['hunan_hunansheng_ggzy']:
            if strptime_transfromsj(page):
                return (strptime_transfromsj(page))
            return ggstart_time
        elif extime(page) is not None:
            return extime(page)
        else:
            return ggstart_time


def extime_all(page, ggstart_time, quyu):
    '''
    df['data']=df['data'].map(lambda x:x if x is not None  else '')
    df['ggstart_time']=df['ggstart_time'].map(lambda x:x if x is not None  else '')

    '''
    ggstart_time = ext_from_ggtime(ggstart_time if ggstart_time is not None else '')

    if 'ggzy' in quyu:
        if quyu not in ggzy_not_exists_list:
            res = ggzy_extime_all(page, ggstart_time, quyu)
        else:
            res = ggstart_time
    else:
        if quyu not in not_ggzy_not_exists_list:
            res = not_ggzy_extime_all(page, ggstart_time, quyu)
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
    pass
