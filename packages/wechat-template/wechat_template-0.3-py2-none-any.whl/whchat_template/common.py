# -*- coding:UTF-8 -*-
#发送模板消息
from models import *
import datetime,requests,simplejson
from django.conf import settings

def gettoken():
    try:
        wechat=Wechat.objects.all().first()
        if wechat.token:
            seconds = (datetime.datetime.now() - wechat.token_create_time).total_seconds()
            if seconds > 120*60:
                return refresh_token(wechat)
        else:
            return refresh_token(wechat)
    except Exception as e:
        return e

def refresh_token(app):
    """获取更新token"""""
    stoken_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
    settings.APPID, settings.APPSECRET)
    sresult = requests.get(stoken_url, verify=False)
    content_dic = eval(sresult.content)
    access_token = content_dic['access_token']
    app.token = access_token
    app.token_create_time = datetime.datetime.now()
    app.save()
    return access_token



def wxapi_getoneuserinfo(openid):
    rt = requests.get(wxapi_getoneuserinfo_url(openid))
    u = simplejson.loads(rt.content)
    if 'errcode' in u:
        if u["errcode"] == 40003:
            return False
    return u


def wxapi_getoneuserinfo_url(openid):
    return "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(gettoken(),openid)