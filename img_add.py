# -*- coding: utf-8 -*-
"""
调用以图搜图私有云接口识别图片
input: urllist file
output: json file

@author: pengyuyan
"""
import time
import requests
import json
from qiniu import QiniuMacAuth
import argparse
import datetime
from multiprocessing import Pool

def retrieval_upload_img(url):
    """
    以图搜图传图
    :param url:图片的uri, 必选
    :return: 200 OK  {"id":""}
    """
    req_url = 'http://100.100.58.46:6126/v1/image/groups/test_0817/add'
    data = {
        "image":
        {
        "id": url, # 图片唯一标识，建议采用业务系统自己的图片 url 或者文件系统路径，搜索图片会返回此 id，如果id为空，则会随机生成ID返回
        "uri": url,
        "tag": "", # 图片标签, 如果传空, 则默认为default
        "desc": {} # 图片描述，可选，可以是布尔值、数字、字符串、数组和map，默认为空
        }
            }

    headers = {"Content-Type": "application/json"}
    response = requests.post(req_url, headers=headers, data=json.dumps(data))

    # print response.text
    # print(response.text).replace('false', 'False').replace('true', 'True')
    ret = eval(response.text.replace('false', 'False').replace('true', 'True'))

    print(json.dumps(ret, encoding="utf-8", ensure_ascii=False))
    return json.dumps(ret, encoding="utf-8", ensure_ascii=False)


def parse_args():
    """
    Parse input arguments.
    :return:
    """
    parser = argparse.ArgumentParser(description='以图搜图API测试')

    parser.add_argument('--in', dest='urllist_file', help='urllist file',
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
    with open(args.urllist_file) as urllist_f, \
            open(args.urllist_file+'.retrieval.json', 'w+') as json_f,\
            open(args.urllist_file+'.error.log', 'w+') as error_f:
        url = urllist_f.readlines()
        len_file = len(url)
        list_all = get_list_all(args.urllist_file)
        try: 
            pool = Pool(processes=20)
            result = pool.map(retrieval_upload_img, list_all)
            pool.close()
            pool.join()
            for j in range(len(result)):
                json_f.write(str(result[j])+'\n')
        except Exception, e:
             print(e)
             error_f.writelines(str(e)+'\n')

    print (datetime.datetime.now(), 'done')
