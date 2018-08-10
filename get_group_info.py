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


def retrieval_get_group_info(access_key, secret_key):
    """
    以图搜图私有云获取 Group 信息，单次请求单个 Group
    :return: 当前 group 的 tag 数量以及当前 group 的图片数目
    """
    req_url = 'http://argus.atlab.ai/v1/image/groups/test_0810'
    token = QiniuMacAuth(access_key, secret_key).token_of_request(
        method='GET',
        host='argus.atlab.ai',
        url="/v1/image/groups/test_0810",
        content_type='application/json',
        qheaders=''
    )
    token = 'Qiniu ' + token
    headers = {"Content-Type": "application/json", "Authorization": token}
    response = requests.get(req_url, headers=headers)

    print response.text
    print response.text.replace('false', 'False').replace('true', 'True')
    ret = eval(response.text.replace('false', 'False').replace('true', 'True'))

    print json.dumps(ret, encoding="utf-8", ensure_ascii=False)
    return json.dumps(ret, encoding="utf-8", ensure_ascii=False)


def parse_args():
    """
    Parse input arguments.
    :return:
    """
    parser = argparse.ArgumentParser(description='以图搜图API测试')
    parser.add_argument('--ak', dest='access_key', help='access_key for qiniu account',
                        type=str)

    parser.add_argument('--sk', dest='secret_key', help='secret_key for qiniu account',
                        type=str)

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    retrieval_get_group_info(args.access_key, args.secret_key)
    
    print datetime.datetime.now(), 'done'
