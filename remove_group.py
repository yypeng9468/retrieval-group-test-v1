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


def retrieval_remove_group(access_key, secret_key):
    """
    销毁 Group，单次请求删除单个 Group
    :return: 200 OK
    """
    req_url = 'http://argus.atlab.ai/v1/image/groups/test_0810/remove'
    data = {"images":["BwAAAKaNDYQ55DQV", "aaa"]}
    token = QiniuMacAuth(access_key, secret_key).token_of_request(
        method='POST',
        host='argus.atlab.ai',
        url="/v1/image/groups/test_0810/remove",
        content_type='application/json',
        qheaders='',
        body=json.dumps(data)
    )
    token = 'Qiniu ' + token
    headers = {"Content-Type": "application/json", "Authorization": token}
    response = requests.post(req_url, headers=headers, data=json.dumps(data))

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

    retrieval_remove_group(args.access_key, args.secret_key)
    
    print datetime.datetime.now(), 'done'
