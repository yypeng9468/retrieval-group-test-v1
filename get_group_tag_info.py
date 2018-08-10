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

def retrieval_get_group_tag_info(access_key, secret_key, marker, limit):
    """
    列出 group 的所有图片，可以按照 tag 过滤
    :param marker: 上一次列举返回的位置标记，作为本次列举的起点信息。默认值为空字符串，可选。
    :param limit: 本次列举的条目数，范围为 1-1000。默认值为 1000。
    :return: 200 OK
    """
    req_url = 'http://argus.atlab.ai/v1/image/groups/0810_test/tag?&marker={}&limit={}'.format(marker, limit)
    token = QiniuMacAuth(access_key, secret_key).token_of_request(
        method='GET',
        host='argus.atlab.ai',
        url="v1/image/groups/0810_test/tag?&marker={}&limit={}".format(marker, limit),
        content_type='application/json',
        qheaders=''
    )
    token = 'Qiniu ' + token
    headers = {"Content-Type": "application/json", "Authorization": token}
    response = requests.post(req_url, headers=headers)

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

    parser.add_argument('--marker', dest='marker', help='marker for last list',
                        default="")

    parser.add_argument('--limit', dest='limit', help='number to list',
                        stype=str)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    
        try: 
            pool = Pool(processes=1)
            result = pool.map(retrieval_get_group_tag_info, args.access_key, args.secret_key, args.marker, args.limit)
            pool.close()
            pool.join()
            for j in range(len(result)):
                json_f.write(str(result[j])+'\n')
        except Exception, e:
             print(e)
             
 
    print datetime.datetime.now(), 'done'
