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
from multiprocessing import Pool


def retrieval_delete_images(id):
    """
    以图搜图删除单张或多张图片
    :param image_id: 要识别的图片id
    :return: 
    200 OK
    """
    ids = [id]
    req_url = 'http://221.122.92.62:6126/v1/image/groups/test_0810_query/delete'
    id = {
    "ids":ids
        } 

    headers = {"Content-Type": "application/json"}
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

    parser.add_argument('--ids', dest='idlist_file', help='image id to delete',
                        type=str)

    return parser.parse_args()

def get_list_all(file_name):
    url_list=[]
    with open(file_name,"r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            url_list.append(lines[i].strip('\n'))
    return url_list


if __name__ == '__main__':

    args = parse_args()

    with open(args.idlist_file) as idlist_f, \
        open(args.idlist_file+'.retrieval.json', 'w+') as json_f,\
        open(args.idlist_file+'.error.log', 'w+') as error_f:
    
        id = idlist_f.readlines()
        len_file = len(id)
        list_all = get_list_all(args.idlist_file)

        try: 
            pool = Pool(processes=5)
            result = pool.map(retrieval_delete_images, list_all)
            pool.close()
            pool.join()
            for j in range(len(result)):
                json_f.write(str(result[j])+'\n')
        except Exception, e:
                print(e)
                error_f.writelines(str(e)+'\n')
    
    print datetime.datetime.now(), 'done'
