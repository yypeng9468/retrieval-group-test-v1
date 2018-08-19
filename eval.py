# -*- coding: utf-8 -*-
import json
import argparse
import numpy as np

def parse_args():
    """
    Parse input arguments.
    :return:
    """
    parser = argparse.ArgumentParser(description='以图搜图API测试')

    parser.add_argument('--in', dest='json_file', help='json file',
                        type=str)
    parser.add_argument('--top', dest='top_k', help='choose top k result',
                        type=int, default=15)
    

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    res_re = []
    b = 0
    h = open("ars.json",'r')

    for line in h.readlines():
        dic = json.loads(line)
        if not "error" in dic.keys():
            b += 1
            t = {"url": dic["url"], "true":0, "simialr_uri":[]}
            im_num = (dic["url"].split(".")[-2]).split('/')[-1]
            for result in dic["search_results"][0]["results"]:
                if ((result["id"].split('/')[4]).split('__')[0]=="eval") and (im_num in (result["id"].split('/'))[4].split('-')[0]):
                    t["simialr_uri"].append(result["id"])
                    t["true"] += 1
            res_re.append(t)
    h.close()

    r = 0
    for i in range(b):
        if res_re[i]["true"]>=args.top_k:
            r += 1
    recall = r/float(b-1)
    print ("The top-5 recall percentage is %f" % recall)


    a = 0
    k = args.top_k
    res_pr = []
    h = open("../txt/query.txt.retrieval.json",'r')
    for line in h.readlines():
        dic = json.loads(line)
        if not "error" in dic.keys():
            a += 1
            t = {"url": dic["url"], "true":0, "simialr_uri":[]}
            im_num = (dic["url"].split(".")[-2]).split('/')[-1]
            for i,result in enumerate(dic["search_results"][0]["results"]):
                if i <= k and ((result["id"].split('/')[4]).split('__')[0]=="eval") and (im_num in (result["id"].split('/'))[4].split('-')[0]):
                    t["simialr_uri"].append(result["id"])
                    t["true"] += 1
            res_pr.append(t)

    p = 0
    for i in range(a):
        p += res_pr[i]["true"]

    precision = p/(float(a-1)*15)
    print ("The precision percentage is %f" % precision)
