# -*- coding: UTF-8 _*_
import requests,simplejson
from common import gettoken

class TagOperate():
    def __init__(self,tag_id=None):
        """

        :param openid:
        :param tag_id:
        """
        self.token=gettoken()
        self.tag_id=tag_id

    def gain_tags(self):
        """获取微信标签"""""
        url='https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s'%self.token
        rets=requests.get(url).content
        msg=simplejson.loads(rets)
        if msg['errcode']:
            return msg['errmsg']
        return msg['tags']

    def gain_tag_users(self):
        """获取标签下的粉丝"""""
        url='https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s'%self.token
        data={'tagid':self.tag_id,'next_openid':''}
        msgjson = simplejson.dumps(data)
        ans=requests.post(url, msgjson).content
        mgsdata = simplejson.loads(ans)
        try:
            if mgsdata['errcode']:
                return mgsdata['errmsg']
        except:
            return mgsdata

    def allocate_tag(self,openid):
        """为用户打标签"""""
        url='https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=%s'%self.token
        print self.tag_id
        data = {'tagid': self.tag_id, 'openid_list':openid}

        msgjson = simplejson.dumps(data)
        ans=requests.post(url, msgjson).content
        mgsdata = simplejson.loads(ans)
        if mgsdata['errcode']:
            return mgsdata['errmsg']
        return True

    def cancels_tag(self,openid):
        """用户标签取消"""""
        url='https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=%s'%self.token
        data = {'tagid': self.tag_id, 'openid_list': openid}
        msgjson = simplejson.dumps(data)
        ans=requests.post(url, msgjson).content
        mgsdata = simplejson.loads(ans)
        if mgsdata['errcode']:
            return mgsdata['errmsg']
        return True

    def gain_user_tags(self,openid):
        """获取用户身上的标签"""""
        url='https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token=%s'%self.token
        data = {'openid':openid}
        msgjson = simplejson.dumps(data)
        ans=requests.post(url, msgjson).content
        mgsdata = simplejson.loads(ans)
        try:
            if mgsdata['errcode']:
                return mgsdata['errmsg']
        except:
            return mgsdata['tagid_list']