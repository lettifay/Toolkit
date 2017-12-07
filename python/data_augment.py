import os,csv
from PIL import Image,ImageChops
import cv2
import numpy as np
import shutil

# add noise to image
# eg. add_noise(1000,'./test/jpg','./test/out',csv_path='./test/test.csv',dlter='|')
def add_noise(noise_num,img_dir,out_dir,csv_path=None,dlter=','):
    prefix = 'noise'+'_'+str(noise_num)+'_'
        
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for f in os.listdir(img_dir):
        noiser_name = prefix + f
        
        if noise_num == 0:
            shutil.copyfile(os.path.join(img_dir,f),os.path.join(out_dir,noiser_name))
        else:
            im = cv2.imread(os.path.join(img_dir,f))
            h,w,dim = im.shape
            for i in range(noise_num):
                x1 = np.random.randint(0,h)
                x2 = np.random.randint(0,h)
                y1 = np.random.randint(0,w)
                y2 = np.random.randint(0,w)
                im[x1,y1,:]=255
                im[x2,y2,:]=0
            cv2.imwrite(os.path.join(out_dir,noiser_name),im)
    
    if csv_path != None:
        records=[]
        with open(csv_path,'rb') as csv_file:
            reader = csv.reader(csv_file,delimiter=dlter)
            for row in reader:
                img_name,label,x,y,w,h = row
                noiser_name = prefix + img_name
                records.append([noiser_name,label,x,y,w,h])
        
        noiser_csv_name = prefix + os.path.split(csv_path)[1]
        noiser_csv_path = os.path.join(os.path.split(csv_path)[0],noiser_csv_name)
        with open(noiser_csv_path,'wb') as csv_file:
            writer = csv.writer(csv_file)
            for record in records:
                writer.writerow(record)
    print 'add_noise done.'
    return noiser_csv_path

# shift image, offset=(x_offset,y_offset)
# eg. img_shift((10,-5),'./test/jpg','./test/out',csv_path='./test/test.csv',dlter=',',background=(255,255,255))
def img_shift(offset,img_dir,out_dir,csv_path=None,dlter=',',background=(0,0,0)):
    prefix = 'shift'+'_'+str(offset[0])+'_'+str(offset[1])+'_pixels_'
    
    M = np.float32([[1,0,offset[0]],[0,1,offset[1]]])
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for f in os.listdir(img_dir):
        sft_img_name = prefix + f
        
        if offset == (0,0):
            shutil.copyfile(os.path.join(img_dir,f),os.path.join(out_dir,sft_img_name))
        else:
            im = cv2.imread(os.path.join(img_dir,f))
            sft_img = cv2.warpAffine(im,M,(im.shape[0],im.shape[1]),borderValue=background)
            cv2.imwrite(os.path.join(out_dir,sft_img_name),sft_img)
    
    if csv_path != None:
        records=[]
        with open(csv_path,'rb') as csv_file:
            reader = csv.reader(csv_file,delimiter=dlter)
            for row in reader:
                img_name,label,x,y,w,h = row
                changer_name = prefix + img_name
                sft_x = str(int(x) + offset[0])
                sft_y = str(int(y) + offset[1])
                records.append([changer_name,label,sft_x,sft_y,w,h])
        
        sft_csv_name = prefix + os.path.split(csv_path)[1]
        sft_csv_path = os.path.join(os.path.split(csv_path)[0],sft_csv_name)
        with open(sft_csv_path,'wb') as csv_file:
            writer = csv.writer(csv_file)
            for record in records:
                writer.writerow(record)
    print 'img_shift done.'
    return sft_csv_path

# adjust image brightness, adjust=('lighter'|'darker',percent), percent from 0 to 1
# eg. img_bright(('lighter','0.05')),'./test/jpg','./test/out',csv_path='./test/test.csv',dlter='|')
def img_bright(adjust,img_dir,out_dir,csv_path=None,dlter=','):
    prefix = adjust[0]+'_'+str(int(adjust[1]*100))+'%_'
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    gamma = 1
    if adjust[0] == 'lighter':
        gamma = 1 + adjust[1]
        
    if adjust[0] == 'darker':
        gamma = 1 - adjust[1]
    
    for f in os.listdir(img_dir):
        adjuster_name = prefix + f
        
        if adjust[1] == 0:
            shutil.copyfile(os.path.join(img_dir,f),os.path.join(out_dir,adjuster_name))
        else:
            im = Image.open(os.path.join(img_dir,f))
            adjuster = im.point(lambda p: p * gamma)
            adjuster.save(os.path.join(out_dir,adjuster_name))
    
    if csv_path != None:
        records=[]
        with open(csv_path,'rb') as csv_file:
            reader = csv.reader(csv_file,delimiter=dlter)
            for row in reader:
                img_name,label,x,y,w,h = row
                adjuster_name = prefix + img_name
                records.append([adjuster_name,label,x,y,w,h])
        
        adjuster_csv_name = prefix + os.path.split(csv_path)[1]
        adjuster_csv_path = os.path.join(os.path.split(csv_path)[0],adjuster_csv_name)
        with open(adjuster_csv_path,'wb') as csv_file:
            writer = csv.writer(csv_file)
            for record in records:
                writer.writerow(record)
    print 'img_bright done.'
    return adjuster_csv_path

# cut a specified rectangular regoin from every image, region=(xmin,ymin,xmax,ymax)
# eg. region_cut((10,20,1000,1500)),'./test/jpg','./test/out',csv_path='./test/test.csv',dlter='|')
def region_cut(region,img_dir,out_dir,csv_path=None,dlter=','):
    prefix = 'region_'+str(region[0])+'_'+str(region[1])+'_'+str(region[2])+'_'+str(region[3])+'_'
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for f in os.listdir(img_dir):
        im = Image.open(os.path.join(img_dir,f))
        newImg = im.crop(region)
        newImg.save(os.path.join(out_dir,f))
    
    if csv_path != None:
        records=[]
        with open(csv_path,'rb') as csv_file:
            reader = csv.reader(csv_file,delimiter=dlter)
            for row in reader:
                img_name,label,x,y,w,h = row
                new_x = str(int(round(float(x) - float(region[0]))))
                new_y = str(int(round(float(y) - float(region[1]))))
                records.append([img_name,label,new_x,new_y,w,h])
                
        cut_csv_name = prefix + os.path.split(csv_path)[1]
        cut_csv_path = os.path.join(os.path.split(csv_path)[0],cut_csv_name)
        with open(cut_csv_path,'wb') as csv_file:
            writer = csv.writer(csv_file)
            for record in records:
                writer.writerow(record)
    print 'region_cut done.'
    return cut_csv_path