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


def retrieval_delete_images(access_key, secret_key, id):
    """
    以图搜图删除单张或多张图片
    :param image_id: 要识别的图片id
    :return: 
    200 OK
    """
    req_url = 'http://argus.atlab.ai/v1/image/groups/test_0810/delete'
    id = {
    "ids":id
        } 
    token = QiniuMacAuth(access_key, secret_key).token_of_request(
        method='POST',
        host='argus.atlab.ai',
        url="/v1/image/groups/test_0810/delete",
        content_type='application/json',
        qheaders='',
        body=json.dumps(id)
    )
    token = 'Qiniu ' + token
    headers = {"Content-Type": "application/json", "Authorization": token}
    response = requests.post(req_url, headers=headers, data=json.dumps(id))

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

    parser.add_argument('--ids', dest='idlist_file', help='image id to delete',
                        type=str)

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    with open(args.idlist_file) as idlist_f, \
        open(args.idlist_f+'.retrieval.json', 'w+') as json_f,\
        open(args.idlist_f+'.error.log', 'w+') as error_f:
    id = idlist_f.readlines()
    len_file = len(id)
    list_all = get_list_all(args.idlist_file)
    try: 
        pool = Pool(processes=20)
        result = pool.map(retrieval_upload_img, args.access_key, args.secret_key, list_all)
        pool.close()
        pool.join()
        for j in range(len(result)):
            json_f.write(str(result[j])+'\n')
    except Exception, e:
            print(e)
            error_f.writelines(str(e)+'\n')
    
    print datetime.datetime.now(), 'done'
