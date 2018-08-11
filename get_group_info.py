# -*- coding: utf-8 -*-
"""
调用以图搜图私有云接口识别图片
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


def retrieval_get_group_info():
    """
    以图搜图私有云获取 Group 信息，单次请求单个 Group
    :return: 当前 group 的 tag 数量以及当前 group 的图片数目
    """
    req_url = 'http://221.122.92.62:6126/v1/image/groups/test_0810_query'
    headers = {"Content-Type": "application/json"}
    response = requests.get(req_url, headers=headers)

    print response.text
    print response.text.replace('false', 'False').replace('true', 'True')
    ret = eval(response.text.replace('false', 'False').replace('true', 'True'))

    print json.dumps(ret, encoding="utf-8", ensure_ascii=False)
    return json.dumps(ret, encoding="utf-8", ensure_ascii=False)



if __name__ == '__main__':

    retrieval_get_group_info()
    
    print datetime.datetime.now(), 'done'
