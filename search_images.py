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


def retrieval_get_group_id(tag, marker, limit):
    """
    :param tag: 只查询指定 tag 的图片，可选
    :param marker: 上一次列举返回的位置标记，作为本次列举的起点信息。默认值为空字符串，可选。
    :param limit: 本次列举的条目数，范围为 1-1000。默认值为 1000。
    :return:
    """
    req_url = 'http://argus.atlab.ai/v1/image/groups/test_0810/images?tag={}&marker={}&limit={}'.format(tag, marker, limit)
    token = QiniuMacAuth(access_key, secret_key).token_of_request(
        method='GET',
        host='argus.atlab.ai',
        url="/v1/image/groups/test_0810/images?tag={}&marker={}&limit={}".format(tag, marker, limit),
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
    parser.add_argument('--tag', dest='tag', help='image tag to search',
                        type=str)
    parser.add_argument('--marker', dest='marker', help='marker for last search',
                        type=str)
    parser.add_argument('--limit', dest='limit', help='limit number to search',
                        type=str)


    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    
    with open(args.taglist_file) as idlist_f, \
        open(args.idlist_f+'.retrieval.json', 'w+') as json_f,\
        open(args.idlist_f+'.error.log', 'w+') as error_f:
    id = idlist_f.readlines()
    len_file = len(id)
    list_all = get_list_all(args.taglist_file)
    try: 
        pool = Pool(processes=20)
        result = pool.map(retrieval_upload_img, list_all, args.marker, args.limit)
        pool.close()
        pool.join()
        for j in range(len(result)):
            json_f.write(str(result[j])+'\n')
    except Exception, e:
            print(e)
            error_f.writelines(str(e)+'\n')
    
    print datetime.datetime.now(), 'done'
