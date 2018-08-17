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

    res = []
    a = 0
    j = 0

    h = open("../txt/query.txt.retrieval.json",'r')

    k = 50

    for line in h.readlines():
        j += 1 
        dic = json.loads(line)
        if not "error" in dic.keys():
            t = {"url": dic["url"], "true":0, "simialr_uri":[], "differ_uri":[]}
            a += 1
            im_num = (dic["url"].split(".")[-2]).split('/')[-1]
            if not k > len(dic["search_results"][0]["results"]):
                for result in dic["search_results"][0]["results"][:k]:
                    if ((result["id"].split('/')[4]).split('__')[0]=="eval") and (im_num in (result["id"].split('/'))[4].split('-')[0]):
                        t["simialr_uri"].append(result["id"])
                        t["true"] += 1
                    else:
                        t["differ_uri"].append(result["id"])
                res.append(t)
            else:
                for result in dic["search_results"][0]["results"]:
                    if ((result["id"].split('/')[4]).split('__')[0]=="eval") and (im_num in (result["id"].split('/'))[4].split('-')[0]):
                        t["simialr_uri"].append(result["id"])
                        t["true"] += 1
                    else:
                        t["differ_uri"].append(result["id"])
                res.append(t)          

    p = 0
    for i in range(a):
        p += res[i]["true"]
        
    precision = p/(float(a-1)*15)
    print ("The recall percentage is %f" % recall)


    for line in h.readlines()[:1]:
        j += 1 
        dic = json.loads(line)
        
        if not "error" in dic.keys():
            t = {"url": dic["url"], "true":0, "simialr_uri":[], "differ_uri":[]}
            a += 1
            im_num = (dic["url"].split(".")[-2]).split('/')[-1]
            for result in dic["search_results"][0]["results"]:
                if ((result["id"].split('/')[4]).split('__')[0]=="eval") and (im_num in (result["id"].split('/'))[4].split('-')[0]):
                    t["simialr_uri"].append(result["id"])
                    t["true"] += 1
                else:
                    t["differ_uri"].append(result["id"])
            res.append(t)


    r = 0
    for i in range(a):
        if res[i]["true"]>=1:
            r += 1
    recall = r/float(a-1)
    print ("The top-5 correct percentage is %f" % precision)
