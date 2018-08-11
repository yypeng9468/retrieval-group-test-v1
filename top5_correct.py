# -*- coding: utf-8 -*-
import json
import argparse

def parse_args():
    """
    Parse input arguments.
    :return:
    """
    parser = argparse.ArgumentParser(description='以图搜图API测试')

    parser.add_argument('--in', dest='json_file', help='json file',
                        type=str)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    res = []
    a = 0
    j = 0

    h = open(args.json_file,'r')

    for line in h.readlines():
        j += 1 
        dic = json.loads(line)
        if not "error" in dic.keys():
            t = {"url": dic["url"], "true":0, "simialr_uri":[]}
            a += 1
            im_num = (dic["url"].split(".")[-2]).split('/')[-1]
            for results in dic["search_results"]:
                uri = []
                if ((results["results"][0]["id"].split('/'))[4].split('__')[0]=="eval") and (im_num in (results["results"][0]["id"].split('/'))[4].split('-')[0]):
                    t["simialr_uri"].append(results)
                    t["true"] += 1
            res.append(t)

    r = 0
    for i in range(a):
        r += res[i]["true"]

    correct = r/(float(a)*15)
    print ("The top-5 correct percentage is %f" % correct)
