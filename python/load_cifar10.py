import numpy as np
import cv2
import os

def unpickle(file):
    import cPickle
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo)
    return dict

def load_data_batch(data_batch_file):
    data_dict = unpickle(data_batch_file)
    X = data_dict['data'].reshape(10000,3,32,32).transpose(0,2,3,1)
    Y = np.array(data_dict['labels'])
    Z = np.array(data_dict['filenames'])
    return X,Y,Z

def load_class_name(class_name_file):
    class_list = unpickle(class_name_file)['label_names']
    class_dict = {}
    for i in range(len(class_list)):
        class_dict[i] = class_list[i]
    return class_dict

def create_imgs(file_path,dir_path,class_dict):
    X,Y,Z = load_data_batch(file_path)
    for i in range(len(X)):
        img = X[i]
        label_name = class_dict.get(Y[i])
        filename = Z[i]
        img_path = os.path.join(dir_path,label_name,filename)
        if not os.path.exists(os.path.join(dir_path,label_name)):
            os.mkdir(os.path.join(dir_path,label_name))
        cv2.imwrite(img_path,img)


# main

train_file_list = ['./data_batch_1','./data_batch_2','./data_batch_3','./data_batch_4','./data_batch_5']
test_file = './test_batch'

train_dir = './train'
test_dir = './test'

label_file = './batches.meta'

if not os.path.exists(train_dir):
    os.mkdir(train_dir)

if not os.path.exists(test_dir):
    os.mkdir(test_dir)

# parse label name
class_dict = load_class_name(label_file)
print class_dict

# parse train dataset
for f in train_file_list:
    create_imgs(f,train_dir,class_dict)
print 'train dataset done.'

# parse test dataset
create_imgs(test_file,test_dir,class_dict)
print 'test dataset done.'

