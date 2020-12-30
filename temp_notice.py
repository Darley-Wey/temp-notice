import datetime
import re
import time
import muggle_ocr
import requests

from wcp import WeChatPush


class User(object):
    def __init__(self, name, wechat):
        self.name = name
        self.wechat = wechat

#实例化用户，用户名和微信公众号openid
users = [
    User("", ''),
    User("", ''),

]


def get_time_stamp(): return int(round(time.time() * 1000))


def login(ssn):
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    count = 0
    while True:
        while True:
            count += 1
            url = 'http://xscfw.hebust.edu.cn/evaluate/verifyCode?d=%s' % (
                str(get_time_stamp()))
            verify_code = ssn.get(url).content
            with open("a.jpg", "wb") as f:
                f.write(verify_code)
            with open("a.jpg", "rb") as f:
                captcha_bytes = f.read()
            # ModelType.Captcha 可识别4-6位验证码
            # im = Image.open('a.jpg')
            # im.show()
            verify_code = sdk.predict(image_bytes=captcha_bytes)
            # print(verify_code)
            if len(verify_code) == 5:
                break
        url = 'http://xscfw.hebust.edu.cn/evaluate/evaluate'#系统网址
        data = {
            'username': '',#用户名
            'password': '',#密码
            'verifyCode': verify_code
        }
        response = ssn.post(url, data=data).text
        error = re.search('var error = \'(.*?)\'', response, re.S)
        if str(error) == 'None':
            print('%d次后正确识别了验证码' % count)
            break


def get_survey_id(ssn):
    url = 'http://xscfw.hebust.edu.cn/evaluate/survey/surveyList'
    response = ssn.get(url).text
    local_date = datetime.datetime.now().strftime('%mm%dd').replace('m', '月').replace('d', '日')
    if local_date[:-5] == '0':
        local_date = local_date.replace('0', '', 1)
    if local_date[-3:-2] == '0':
        local_date = local_date.replace('0', '', 1)
    print(local_date + datetime.datetime.now().strftime('%H:%M:%S'))
    survey_id = re.search(local_date + '.*?id=(.*?)\"', response, re.S)
    survey_id = survey_id.group(1)
    # print(survey_id)
    return survey_id


def push_notice(ssn, sid, push):
    url = 'http://xscfw.hebust.edu.cn/evaluate/survey/surveyStuList?id=' + sid
    name_list = []
    for i in range(3):
        data = {
            'numberCX': '',
            'nameCX': '',
            'gradeCX': '2',
            'academyCX': '11',
            'typeCX': '0',
            'pageNo': str(i + 1)
        }
        response = ssn.post(url, data=data).text
        name_list = name_list + re.findall(
            r'<td>.*?<td>.*?<td>(.+?)</td>.*?</td>.*?</td>.*?</td>.*?</td>.*?</td>', response, re.S)
    if len(name_list) != 0:
        print(name_list)
        for name in name_list:
            for user in users:
                if name == user.name:
                    push.push_notice(user.wechat)


if __name__ == "__main__":
    push = WeChatPush()
    print()
    session = requests.session()
    session.get('http://xscfw.hebust.edu.cn/evaluate/login.jsp')
    login(session)
    survey_id = get_survey_id(session)
    push_notice(session, survey_id, push)
    exit()
