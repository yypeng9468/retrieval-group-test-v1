import json

file = open('/Users/pengyuyan/Desktop/org_list.txt.retrieval.json','r')
res = []
a = 0

for line in file.readlines():
    dic = json.loads(line)
    if not "error" in dic.keys():
        a += 1
        img_url = dic["url"]
        im_num = img_url.split('.')[-2].split('/')[-1].lstrip('image_group_test_')
        t = {"url": img_url, "true":0, "simialr_uri":[]}
        for i in dic["result"]:
            uri = []
            if (i["uri"].split('/'))[4] == "similar" and (im_num in (i["uri"].split('/'))[5]):
                t["simialr_uri"].append(i)
                t["true"] += 1
    res.append(t)

r = 0
for i in range(a):
    r += res[i]["true"]

correct = r/float(a)
print ("The top-5 correct percentage is %f" % correct)