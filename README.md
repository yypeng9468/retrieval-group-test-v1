# retrieval-group-test-private-v1
这是一个以图搜图算法（私有云API）测试方法

1.1 创建 Group
新建 Group，单次请求创建单个 Group
usage: python2 new-group.py --ak access_key --sk secret_key --cfg config

1.2 获取所有Group ID
获取所有Group ID
python2 get_all_groups_ID.py --ak access_key --sk secret_key

1.3 获取 Group 信息
获取 Group 信息，单次请求单个 Group
python2 get_group_info.py --ak access_key --sk secret_key

1.4 销毁 Group
销毁 Group，单次请求删除单个 Group
python2 remove_group.py --ak access_key --sk secret_key

1.5 添加图片 
添加图片到一个 Group
python2 img_add.py --ak access_key --sk secret_key --in url_list

1.6 检索图片
输入一张或者多张图片，返回与之相似的图片列表，按相似度排序
python2 retrieval_images.py --ak access_key --sk secret_key --in url_list

1.7 删除图片
删除多张图片
python2 delete_images.py --ak access_key --sk secret_key --ids image_id_list

1.8 更新图片
更新 id 对应的图片内容以及 tag、desc
python2 update_images.py --ak access_key --sk secret_key

1.9 查询图片
列出 group 的所有图片，可以按照 tag 过滤
python2 search_images.py --ak access_key --sk secret_key --tag tag --marker marker --limit limit

1.10 获取Group Tag信息
列出 group 的所有tag
python2 get_group_tag_info.py --ak access_key --sk secret_key --marker marker --limit limit


