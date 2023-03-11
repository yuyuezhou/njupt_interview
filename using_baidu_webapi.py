import requests
import json
import uuid
import base64


def get_token():
    """获取百度的token"""

    url = "https://openapi.baidu.com/oauth/2.0/token"        # 获取token的网页网址
    grant_type = "client_credentials"                        # 用户模式，使用服务的
    api_key = "fBo9Tk3u7emiOkFA4a1RqWm0"                     # 自己申请的应用
    secret_key = "ebEstWzuIZ1Gj5DKxlBybzKoB5XwcBBj"          # 自己申请的应用

    """数据格式如下"""
    data = {'grant_type': grant_type, 'client_id': api_key, 'client_secret': secret_key}
    r = requests.post(url, data=data)
    #test:
    token = json.loads(r.text).get("access_token")      #json.loads()把Json格式字符串解码，转换成Python对象。
    return token


def recognize(sig, rate, token, form):
    """通过发送token，调用百度语音识别API来识别音频,返回网站的返回信息"""

    url = "http://vop.baidu.com/server_api"                 # 调用web API的网页网址

    speech_length = len(sig)                                # 语音的长度
    speech = base64.b64encode(sig).decode("utf-8")          # 得到基于base64编码的文件
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]   # 本机的Mac地址 #70-C9-4E-E1-B5-0D
    rate = rate                                             # 音频文件的码率
    data = {
        "format": form,
        "lan": "zh",
        "token": token,
        "len": speech_length,
        "rate": rate,
        "speech": speech,
        "cuid": mac_address,
        "channel": 1,
    }
    data_length = len(json.dumps(data).encode("utf-8"))     # 整个请求的长度,json.dumps将一个Python数据结构转换为JSON
    headers = {"Content-Type": "application/json",
               "Content-Length": str(data_length)}          # 请求的头部
    r = requests.post(url, data=json.dumps(data), headers=headers)   # 向网页提交请求得到网页返回的数据
    # requests.post返回的数据是一个Response对象，其中包含了请求的状态码、响应头、响应体等信息。可以通过该对象的属性和方法来获取和处理这些信息，例如：
    # status_code：获取响应的状态码
    # headers：获取响应头信息
    # text：获取响应体的文本内容
    # content：获取响应体的二进制内容
    # json()：将响应体的JSON数据转换为Python对象
    result = json.loads(r.text).get("result")
    initial_result = r.text                                 # str类型
    initial_result = eval(initial_result)                   # 使这个数据字典化，不然没法根据value值得到想要的数据
    result = str(initial_result['result'])                  # 把得到的value值字符串化
    return result[2:len(result) - 3]     #result[0:len(result)]输出为['识别结果']



