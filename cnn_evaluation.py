import os
import numpy as np

def recall_by_image(image_dir, k):
    img_names = os.listdir(image_dir)
    query_img = [i for i in img_names if 'query' in i]
    result_imgs = img_names.copy()
    result_imgs.pop(result_imgs.index(query_img[0]))

    tp = 0
    i = 0
    key = (query_img[0].split('-')[1]).split('.')[0]
    for im in result_imgs:
        i += 1
        index = int(im.split('-')[0])
        if key in im and index<=k:
            tp += 1
            
    recall = tp/15.0
    return recall

if name == '__main__':
    cur = '/Users/pengyuyan/Documents/cnn-aika-2-eval_eucli-force/topk-images-result/'
    os.chdir(cur)

    sum_recall = []
    cur_dir_fname = os.listdir('.')
    cur_dir_fname.pop(cur_dir_fname.index('.DS_Store'))
    for f in cur_dir_fname:
        f = cur + f
        sum_recall.append(recall_by_image(f, 15))
        
    final_recall = np.mean(sum_recall) 
    print(final_recall)

