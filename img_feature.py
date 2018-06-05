# -*- coding: utf-8 -*-
"""
调用线上以图搜图接口识别图片
input: urllist file
output: json file

@author: songqian
"""

import requests
import json
from qiniu import QiniuMacAuth
import argparse
import datetime


def retrieval_upload_img(access_key, secret_key, url):
    """
    以图搜图传图
    :return:
    """
    req_url = 'http://argus.atlab.ai/v1/image/group/retrieval-fortest-v0_1_/add'
    data = {
        "data": [
            {"uri": url}
            ]
    }
    # data = 
    # {
	# "data": [
	# 	{
	# 		"uri": "",
	# 		"attribute": {
	# 			"label": "retrieval-fortest-v0_1_similar"
	# 		}
	# 	}
	# ]
    # }
    token = QiniuMacAuth(access_key, secret_key).token_of_request(
        method='POST',
        host='argus.atlab.ai',
        url="/v1/image/group/retrieval-fortest-v0_1_/add",
        content_type='application/json',
        qheaders='',
        body=json.dumps(data)
    )
    token = 'Qiniu ' + token
    headers = {"Content-Type": "application/json", "Authorization": token}
    response = requests.post(req_url, headers=headers, data=json.dumps(data))

    print '-'*80
    print(response.text)
    print(response.text).replace('false', 'False').replace('true', 'True')
    ret = eval(response.text.replace('false', 'False').replace('true', 'True'))

    print(json.dumps(ret, encoding="utf-8", ensure_ascii=False))
    return json.dumps(ret, encoding="utf-8", ensure_ascii=False)


def parse_args():
    """
    Parse input arguments.
    :return:
    """
    parser = argparse.ArgumentParser(description='政治人物API测试')
    parser.add_argument('--ak', dest='access_key', help='access_key for qiniu account',
                        type=str)

    parser.add_argument('--sk', dest='secret_key', help='secret_key for qiniu account',
                        type=str)

    parser.add_argument('--in', dest='urllist_file', help='urllist file',
                        type=str)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    with open(args.urllist_file) as urllist_f, \
            open(args.urllist_file+'.politician_online.json', 'w+') as json_f,\
            open(args.urllist_file+'.error.log', 'w+') as error_f:
        url = urllist_f.readline().rstrip('\n')
        while url:
            print url
            # retrieval_upload_img(args.access_key, args.secret_key, url)
            try:
                result = retrieval_upload_img(args.access_key, args.secret_key, url)
                json_f.write(result+'\n')
            except Exception, e:
                print e
                error_f.writelines(url+', '+str(e)+'\n')
            url = urllist_f.readline().rstrip('\n')

    print datetime.datetime.now(), 'done'
