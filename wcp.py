import requests


class WeChatPush:
    def __init__(self):
        app_id = ''#微信公众号
        app_secret = ''#微信公众号
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + \
              app_id + '&secret=' + app_secret
        dict = requests.get(url).json()
        self.token = dict['access_token']

    def push_success(self, receiver, stu_num, seat, date, time):
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + self.token
        data = {
            "touser": receiver,
            "template_id": "f1nfcLgFMg_cN_EaWGQ3n7h0-RMKgEqMqXZ0ryvifb0",#模板消息
            "data": {
                'stuNum': {
                    'value': stu_num,
                    "color": "#173177"
                },
                "seat": {
                    "value": seat,
                    "color": "#173177"
                },
                'date': {
                    "value": date,
                    "color": "#173177"
                },
                'time': {
                    "value": time,
                    "color": "#173177"
                }
            }
        }
        if receiver != '':
            requests.post(url, json=data)

    def push_fail(self, receiver, stu_num, reason):
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + self.token
        data = {
            "touser": receiver,
            "template_id": "sl-ko9IqhrtQ-IvaWjWgHo1-k-lOCoFEjm-JMVkftoc",
            "data": {
                'stuNum': {
                    'value': stu_num,
                    "color": "#173177"
                },
                "reason": {
                    "value": reason,
                    "color": "#173177"
                }
            }
        }
        if receiver != '':
            requests.post(url, json=data)

    def push_result(self, result):
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + self.token
        data = {
            "touser": 'oCLvE50F1iVn2WJ6t2_Jr2n8urr8',
            "template_id": "EpFWqvy2nOaiyITBHydryKfC7ZMRZP8vRTc_E2TKpyY",
            "data": {
                'result': {
                    'value': result,
                    "color": "#173177"
                }
            }
        }
        requests.post(url, json=data)

    def push_notice(self, receiver):
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + self.token
        data = {
            "touser": receiver,
            "url": "http://xscfw.hebust.edu.cn/survey/login",
            "template_id": "CmNwRR5PkZaNjQtexN1nh9IdVUGWBATHaDaesxUzNsg",
            "data": {
                'notice': {
                    'value': "科学防疫，你我携手，点击进入完成今日体温填报",
                    "color": "#173177"
                }
            }
        }
        requests.post(url, json=data)
