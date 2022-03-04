# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import requests
from YuemiaoPublicAccount.yuemiao import YueMiao
import sys
import argparse

cookie = "UM_distinctid=17f53fc9b930-0d558aae8663bc-1051275-100200-17f53fc9b963f2; _xzkj_=wxtoken:7c4c6cc081c91e082b3ce3b370405304_ddde4b868e9ff4a911ece0c2a81cbfc3; _xxhm_=%7B%22id%22%3A28417589%2C%22mobile%22%3A%2218810913675%22%2C%22nickName%22%3A%22%E6%9E%9C%E7%8C%AB%22%2C%22headerImg%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTLNknMlYDjocHDYoe7oPXM0wDqlllqEJbWDl5ZHXAcYkzW1THm3aKoY367xWkuQ4TiadHMRzsRibZ6A%2F132%22%2C%22regionCode%22%3A%22110105%22%2C%22name%22%3A%22%E8%B5%B5*%E7%A7%80%22%2C%22uFrom%22%3A%22depa_vacc_detail%22%2C%22wxSubscribed%22%3A0%2C%22birthday%22%3A%221997-07-09+02%3A00%3A00%22%2C%22sex%22%3A2%2C%22hasPassword%22%3Atrue%2C%22birthdayStr%22%3A%221997-07-09%22%7D; CNZZDATA1261985103=542957191-1646371066-%7C1646381866"
tk = "wxtoken:7c4c6cc081c91e082b3ce3b370405304_ddde4b868e9ff4a911ece0c2a81cbfc3"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('op', help='choose [ order | subscribe | save | info ]；'
                                   'order:开始预约；subscribe：开始订阅；'
                                   'save：查找已经到苗的所有社区信息（只针对--province某一个省或者不传参针对全国）；'
                                   'info：查看保存社区信息')
    # 三个优先级从高到低
    parser.add_argument('--region_id', help='地区id（4101河南郑州）')  # , default='4101')     # 4101-郑州区域id
    parser.add_argument('--name', help='社区医院名称（新郑市龙湖镇卫生院）')  # , default='新郑市龙湖镇卫生院')
    parser.add_argument('--province', help='选择省份（河南省）', default='河南省')
    return parser.parse_args()


if __name__ == '__main__':

    yuemiao = YueMiao(tk=tk, cookie=cookie)

    args = parse_args()
    op = args.op
    name = args.name
    province = args.province
    region_id = args.region_id

    if op == 'order':
        # 开始预订
        if region_id is not None:
            flag = yuemiao.find_is_order(regionCode=region_id)
        elif name is not None:
            # departmentName = 新郑洪圣堂医院预防接种门诊
            yuemiao.order_by_name(departmentName=name)
        else:
            flag = yuemiao.find_is_order(province=province)
    elif op == 'subscribe':
        # 开始订阅
        if region_id is not None:
            flag = yuemiao.subscribe_by_region_id(region_id=region_id)
        elif name is not None:
            yuemiao.subscribe_by_name(name=name)
        else:
            flag = yuemiao.subscribe_by_province(province=province)
    elif op == 'save':
        if province is not None and province != "":
            # 保存某个省的所有一到疫苗的社区信息
            print("[info]: 查找{}内的已经到苗信息".format(province))
            yuemiao.query_arrive_vaccine_by_province(province=province)
        else:
            # 保存全国所有一到疫苗的社区信息
            print("[info]: 查找全国范围内的已经到苗信息")
            yuemiao.query_arrive_vaccine_in_china()
    elif op == 'info':
        if region_id is not None:
            yuemiao.get_all_departments_by_code(regionCode=region_id)
        elif name is not None:
            yuemiao.get_all_departments_by_name(name=name)
        elif province is not None:
            yuemiao.get_all_departments_by_province(province=province)

    else:
        print('[error]: 你输入的操作"{}" 不是 "[ order | subscribe | save | info ]"里的一个'
              .format(op))

