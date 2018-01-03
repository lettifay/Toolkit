# this script used for split img-xml pair dataset to train and test

import os
import random
import shutil

# customized value
all_annotations_dir = './all/Annotations/'
all_imgs_dir = './all/JPEGImages'
all_gt_dir = './all/Groundtruth'

train_annotations_dir = './train/Annotations'
train_imgs_dir = './train/JPEGImages'

test_imgs_dir = './test/imgs'
test_gt_dir = './test/Groundtruth'

test_num = 10

# main
for d in [train_annotations_dir, train_imgs_dir, test_imgs_dir, test_gt_dir]:
    if not os.path.exists(d):
        print 'create ',d
        os.makedirs(d)

all_list = os.listdir(all_imgs_dir)
all_num = len(all_list)

test_list = []
count = 0
while count < test_num:
    test_list.append(all_list[random.randint(0,all_num)])
    count += 1        

train_list = list(set(all_list) - set(test_list))

for f in test_list:
    shortname = os.path.splitext(f)[0]
    img_src = os.path.join(all_imgs_dir, shortname + '.jpg')
    img_dst = os.path.join(test_imgs_dir, shortname + '.jpg')
    shutil.copyfile(img_src,img_dst)
    
    gt_src = os.path.join(all_gt_dir, shortname + '.jpg')
    gt_dst = os.path.join(test_gt_dir, shortname + '.jpg')
    shutil.copyfile(gt_src,gt_dst)

for f in train_list:
    shortname = os.path.splitext(f)[0]
    img_src = os.path.join(all_imgs_dir, shortname + '.jpg')
    img_dst = os.path.join(train_imgs_dir, shortname + '.jpg')
    shutil.copyfile(img_src,img_dst)
    
    annotation_src = os.path.join(all_annotations_dir, shortname + '.xml')
    annotation_dst = os.path.join(train_annotations_dir, shortname + '.xml')
    shutil.copyfile(annotation_src,annotation_dst)


