# -*- coding: UTF-8 _*_
import requests,simplejson
from common import gettoken,wxapi_getoneuserinfo



class MsgAdmin():

    def send_template(self,template_id, url, data, touser):
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

    def custom_message(self,openid,content):
        """客服文本消息"""""
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % gettoken()
        datas = {
            "touser": openid,
            "msgtype": "text",
            "text": {"content":content }
        }
        data = simplejson.dumps(datas, ensure_ascii=False).encode('utf-8')
        r = requests.post(url, data=data)
        print r.content
        mgsdata = eval(r.content)
        if mgsdata['errcode']>0:
            return mgsdata['errmsg']
        return True




    def gain_user_msg(self,openid):
        """获取用户信息"""""
        if openid:
            usermsg=wxapi_getoneuserinfo(openid)
            if usermsg:
                return usermsg
            return u"用户不存在"
        return u"请传openid"