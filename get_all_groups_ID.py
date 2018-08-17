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


def retrieval_get_group_id():
    """
    以图搜图私有云获取所有Group ID
    :return: 所有Group ID
    """
    req_url = 'http://221.122.92.62:6126/v1/image/groups'
    # headers = {"Content-Type": "application/json"}
    response = requests.get(req_url)

    print response.text
    print response.text.replace('false', 'False').replace('true', 'True')
    ret = eval(response.text.replace('false', 'False').replace('true', 'True'))

    print json.dumps(ret, encoding="utf-8", ensure_ascii=False)
    return json.dumps(ret, encoding="utf-8", ensure_ascii=False)



if __name__ == '__main__':

    retrieval_get_group_id()
    
    print datetime.datetime.now(), 'done'
