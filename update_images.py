# -*- coding: utf-8 -*-
"""
调用以图搜图私有云接口识别图片
input: urllist file
output: json file

@author: pengyuyan
"""

import requests
import json
from qiniu import QiniuMacAuth
import argparse
import datetime
from multiprocessing import Pool

def retrieval_renew_images(id):
    """
    更新 id 对应的图片内容以及 tag、desc
    :return: 200 OK
    """
    req_url = 'http://221.122.92.62:6126/v1/image/groups/test_0810_query/update'
    # ids = [id]
    data = {
        "image":
        {
        "id": id,
        "uri": id,
        "tag": "",
        "desc": {}
        }
        }
    headers = {"Content-Type": "application/json"}
    response = requests.post(req_url, headers=headers, data=json.dumps(data))

    print response.text
    print response.headers
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

    parser.add_argument('--ids', dest='idlist_file', help='image id to update',
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
            result = pool.map(retrieval_renew_images, list_all)
            pool.close()
            pool.join()
            for j in range(len(result)):
                json_f.write(str(result[j])+'\n')
        except Exception, e:
                print(e)
                error_f.writelines(str(e)+'\n')

    print datetime.datetime.now(), 'done'
