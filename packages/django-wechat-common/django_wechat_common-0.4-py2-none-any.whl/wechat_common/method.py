# -*- coding: UTF-8 _*_
"""模板消息发送"""

import requests,simplejson
from common import gettoken,wxapi_getoneuserinfo


# class WxCommon():
#     def __init__(self):
#         pass

def Send_Template(template_id, url, data, touser):
    """
    :param template_id: 模板id
    :param url: 详细url
    :param data: 数据
    :param touser: 用户openid
    :return:
    """
    try:
        urls = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"%gettoken()
        dict = {}
        dict['template_id'] = template_id
        dict_data = {}
        for item in data:  # 处理数据格式
            if "color" in item:
                dict_data[item['key']] = {
                    "value": item['value'],
                    "color": item['color']
                }
            else:
                dict_data[item['key']] = {
                    "value": item['value']
                }
        dict['data'] = dict_data
        dict['url'] = url
        for openid in touser:
            dict['touser'] = openid
            msgjson = simplejson.dumps(dict)
            requests.post(urls, msgjson)
    except Exception, e:
        return e.message
    return True


def GainUserMsg(openid):
    """获取用户信息"""""
    if openid:
        usermsg=wxapi_getoneuserinfo(openid)
        if usermsg:
            return usermsg
        return u"用户不存在"
    return u"请传openid"