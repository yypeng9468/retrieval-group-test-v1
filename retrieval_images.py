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

def retrieval_search_group(url):
    """
    输入一张或者多张图片，返回与之相似的图片列表，按相似度排序
    :param url: 要识别的图片URL
    :return:
    {
    "search_results": [
        {
            "results":[
                {
                    "id":id, # 图片唯一标识
                    "score":0.9, # 图片搜索相似度
                    "tag":"", # 命中图片的标签
                    "desc":{} # 命中图片的描述信息
                }
            ]
        },
        ...
    ]
}
    """
    req_url = 'http://221.122.92.62:6126/v1/image/groups/test_0810_query/search'
    urls = [url]
    data = {
        "images": urls,
        "threshold": 0.9, # 搜索图片阈值， 范围 [-1,1]，推荐 0.9  
        "limit": 5 # 返回的单张图片搜索到的图片数目限制，范围 [1,10000]， 默认 100
            }
    headers = {"Content-Type": "application/json"}
    response = requests.post(req_url, headers=headers, data=json.dumps(data))

    print response.text
    print response.headers
    print response.text.replace('false', 'False').replace('true', 'True')
    ret = eval(response.text.replace('false', 'False').replace('true', 'True'))
    ret['url'] = url

    # json.load(ret, encoding="utf-8", ensure_ascii=False)
    print json.dumps(ret, encoding="utf-8", ensure_ascii=False)
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

        list_all = get_list_all(args.urllist_file)
        try: 
            pool = Pool(processes=5)
            result = pool.map(retrieval_search_group, list_all)
            pool.close()
            pool.join()
            for j in range(len(result)):
                json_f.write(str(result[j])+'\n')
        except Exception, e:
             print(e)
             
    print datetime.datetime.now(), 'done'
