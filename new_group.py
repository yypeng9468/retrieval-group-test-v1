# -*- coding: utf-8 -*-
"""
调用以图搜图私有云接口识别图片
input: access_key, secret_key, cfg
output: json file

@author: pengyuyan
"""

import requests
import json
from qiniu import QiniuMacAuth
import argparse
import datetime
import os


def retrieval_new_group(cfg):
    """
    以图搜图私有云新建 Group，单次请求创建单个 Group
    :group_name: Group 唯一标识，长度 3-32 位，第一位必须是小写字母，其它位置是小写字母或者数字、下划线 、"-"
    :param cfg: Group 预期图片数目，必选，必须大于0，可以自动增长，实际限制受限于内存或者显存
    :return: 200 OK
    """
    req_url = 'http://221.122.92.62:6126/v1/image/groups/test_0813_v1'
    config = {
         "config":
         {
             "capacity": cfg
         }
     }


    headers = {"Content-Type": "application/json"}
    response = requests.post(req_url, headers=headers, data=json.dumps(config))

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
    parser.add_argument('--cfg', dest='config', help='预期图片数目', type=int,
                        default=300000)

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    retrieval_new_group(args.config)

    print datetime.datetime.now(), 'done'
