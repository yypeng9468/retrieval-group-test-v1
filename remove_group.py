# -*- coding: utf-8 -*-
"""
调用线上以图搜图接口识别图片
input: access_key, secret_key
output: json file

@author: pengyuyan
"""

import requests
import json
from qiniu import QiniuMacAuth
import argparse
import datetime
import os


def retrieval_remove_group():
    """
    销毁 Group，单次请求删除单个 Group
    :return: 200 OK
    """
    req_url = 'http://100.100.58.71:6126/v1/image/groups/test_0813_v1/remove'
    # headers = {"Content-Type": "application/json"}
    response = requests.post(req_url)

    print response.text
    print response.text.replace('false', 'False').replace('true', 'True')
    ret = eval(response.text.replace('false', 'False').replace('true', 'True'))

    print json.dumps(ret, encoding="utf-8", ensure_ascii=False)
    return json.dumps(ret, encoding="utf-8", ensure_ascii=False)



if __name__ == '__main__':

    retrieval_remove_group()
    
    print datetime.datetime.now(), 'done'
