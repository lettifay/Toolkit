import os
from PIL import Image,ImageChops
import xml.etree.cElementTree as ET
import xml.dom.minidom as MD
import cv2

# check dir path
def dir_check(jpg_dir, xml_dir, trainval_txt_dir, gt_img_dir):
    input_dir_list = [jpg_dir, xml_dir]
    output_dir_list = [trainval_txt_dir, gt_img_dir]

    for d in input_dir_list:
        if not os.path.exists(d):
            print "Please check input jpg/xml dir path."

    for d in output_dir_list:
        if not os.path.exists(d):
            if d == trainval_txt_dir:
                os.makedirs(trainval_txt_dir)
                print "trainval_txt_dir made."
            if d == gt_img_dir:
                os.mkdir(gt_img_dir)
                print "gt_img_dir made."
    print 'input and output dir checked.'
    return

# check labeled sample of each class
def count_labels(xml_dir,labels):
    for label in labels:
        count = 0
        for f in os.listdir(xml_dir):
            if f.lower().endswith('.xml'):
                xml_file = os.path.join(xml_dir,f)
                tree = ET.parse(xml_file)
                root = tree.getroot()        
                for obj in root.findall('object'):
                    if obj.find('name').text == label:
                        count = count + 1
        print label,'number:',count
    return

# check jpg/xml files pair
def check_file_pair(xml_dir,jpg_dir,extension='.jpg'):
    print "xml file number: ",len(os.listdir(xml_dir))
    print "jpg file number: ",len(os.listdir(jpg_dir))

    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            shortname = os.path.splitext(f)[0]
            if not os.path.exists(os.path.join(jpg_dir, shortname + extension)):
                print "Can not find jpg file: ", f

    for f in os.listdir(jpg_dir):
        if f.lower().endswith(extension):
            shortname = os.path.splitext(f)[0]
            if not os.path.exists(os.path.join(xml_dir, shortname + '.xml')):
                print "Can not find xml file: ", f
    print "jpg/xml files pair checked."
    return

# check and update xml value
def validate_xml(xml_dir,jpg_dir,labels,extension='.jpg',update=False):
    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            xml_file = os.path.join(xml_dir,f)
            jpg_file = os.path.join(jpg_dir, os.path.splitext(f)[0] + extension)

            im = cv2.imread(jpg_file)
            h,w,dim = im.shape
            tree = ET.parse(xml_file)
            root = tree.getroot()

            #check image shape value
            width_xml = int(root.find('size').find('width').text)
            height_xml = int(root.find('size').find('height').text)
            dim_xml = int(root.find('size').find('depth').text)
            if  width_xml != w or height_xml != h or dim_xml != dim:
                if not update:
                    if width_xml != w:
                        print "width not match: %s and %s."%(jpg_file,xml_file)
                    if height_xml != h:
                        print "height not match: %s and %s."%(jpg_file,xml_file)
                    if dim_xml != dim:
                        print "dim not match: %s and %s."%(jpg_file,xml_file)
                if update:
                    print "Update the size value in xml ..."
                    root.find('size').find('width').text = str(w)
                    root.find('size').find('height').text = str(h)
                    root.find('size').find('depth').text = str(dim)
            
            #check ervry obj value 
            for obj in root.findall('object'):
                #check labels
                if (obj.find('name').text not in labels) and (obj.find('name').text.lower() in labels):
                    if not update:
                        print 'Upper case label: %s in %s' %(obj.find('name').text, xml_file)
                    if update:
                        print 'Update the label name to lower case ...'
                        obj.find('name').text = obj.find('name').text.lower()
                if (obj.find('name').text not in labels) and (obj.find('name').text.lower() not in labels):
                    print 'Undefined label: %s in %s' %(obj.find('name').text, xml_file)

                # check bnbox coordinates
                xmin = int(obj.find('bndbox').find('xmin').text)
                ymin = int(obj.find('bndbox').find('ymin').text)
                xmax = int(obj.find('bndbox').find('xmax').text)
                ymax = int(obj.find('bndbox').find('ymax').text)
                
                if xmin <= 0 or ymin <=0 or xmax >= w or ymax >= h or xmin >= xmax or ymin >= ymax:
                    if not update:
                        print xml_file, ": illegal bnbox value."
                        print 'image width=%i, height=%i' %(w,h)
                        print 'xmin=%i,ymin=%i,xmax=%i,ymax=%i' %(xmin,ymin,xmax,ymax)

                    if update :
                        print 'Update the bnbox value ...'               
                        if xmin <=0:
                            obj.find('bndbox').find('xmin').text = str(1)
                        if ymin <=0:
                            obj.find('bndbox').find('ymin').text = str(1)
                        if xmax >=w: 
                            obj.find('bndbox').find('xmax').text = str(w - 1)
                        if ymax >=h: 
                            obj.find('bndbox').find('ymax').text = str(h - 1)
                        if xmin >= xmax:
                            obj.find('bndbox').find('xmin').text = str(xmax)
                            obj.find('bndbox').find('xmax').text = str(xmin)
                        if ymin >= ymax:
                            obj.find('bndbox').find('ymin').text = str(ymax)
                            obj.find('bndbox').find('ymax').text = str(ymin)                                         
            if update:
                tree.write(xml_file)
    print "xml value checked."
    return

def parse_xml_bnbox(xml_path):
    bndbox_list=[]
    tree = ET.ElementTree(file=xml_path)
    for obj in tree.iter(tag='object'):
        xmin=int(obj.find('bndbox').find('xmin').text)
        ymin=int(obj.find('bndbox').find('ymin').text)
        xmax=int(obj.find('bndbox').find('xmax').text)
        ymax=int(obj.find('bndbox').find('ymax').text)
        name=obj.find('name').text
        bndbox_list.append((xmin,ymin,xmax,ymax,name))
    return bndbox_list

def draw_bndbox(in_img_path,bndbox_list,out_img_path,clr,thickness):
    color_dict = {
        'green':(0,255,0),
        'red':(0,0,255),
        'blue':(255,0,0)
    }
    color = color_dict.get(clr)

    im = cv2.imread(in_img_path)
    for bndbox in bndbox_list:
        cv2.rectangle(im,(bndbox[0],bndbox[1]),(bndbox[2],bndbox[3]),color,thickness)
        cv2.putText(im,bndbox[4],(bndbox[0]+10,bndbox[1]-10),0,1,color,thickness)
    cv2.imwrite(out_img_path,im)
    return

def draw_gt_img(xml_dir,jpg_dir,gt_img_dir,extension='.jpg',color='green',thickness=1):
    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            xml_file = os.path.join(xml_dir,f)
            jpg_file = os.path.join(jpg_dir, os.path.splitext(f)[0] + extension)
            gt_file = os.path.join(gt_img_dir, os.path.splitext(f)[0] + extension)
            bndbox_list = parse_xml_bnbox(xml_file)
            draw_bndbox(jpg_file,bndbox_list,gt_file,color,thickness)
    print "Ground truth image created."
    return

def create_trainval_txt(xml_dir,trainval_txt_dir):
    trainval_txt_file = os.path.join(trainval_txt_dir,'trainval.txt')
    with open(trainval_txt_file ,'wb') as f:
        for file_name in os.listdir(xml_dir):
            if file_name.lower().endswith('.xml'):
                f.write(os.path.splitext(file_name)[0] + '\n')
    print 'trainval.txt created.' 
    return

def update_label(xml_dir,ori_label,new_label):
    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            xml_file = os.path.join(xml_dir,f)
            tree = ET.parse(xml_file)
            root = tree.getroot()        
            for obj in root.findall('object'):
                if obj.find('name').text == ori_label: 
                    obj.find('name').text = new_label
            tree.write(xml_file)
            print 'Label updated, from %s to %s : %s' %(ori_label,new_label,xml_file)
    return

def remove_label(xml_dir,aim_label):
    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            xml_file = os.path.join(xml_dir,f)
            tree = ET.parse(xml_file)
            root = tree.getroot() 
            for obj in root.findall('object'):
                if obj.find('name').text == aim_label: 
                    root.remove(obj)
        tree.write(xml_file)
    print 'Object removed with label',aim_label
    return

def reserve_label(xml_dir,reserve_labels):
    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            xml_file = os.path.join(xml_dir,f)
            tree = ET.parse(xml_file)
            root = tree.getroot() 
            for obj in root.findall('object'):
                if obj.find('name').text not in reserve_labels: 
                    root.remove(obj)
            tree.write(xml_file)
    print 'Object reserved with labels', str(reserve_labels)
    return

def rm_NoneObj_pair(xml_dir,jpg_dir,extension='.jpg'):
    rm_list=[]
    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            shortname = os.path.splitext(f)[0]
            xml = os.path.join(xml_dir,f)
            tree = ET.parse(xml)
            root = tree.getroot() 
            if len(root.findall('object'))==0:
                rm_list.append(shortname)
    for f in rm_list:
        #print f
        xml_file = os.path.join(xml_dir,f + '.xml')
        img_file = os.path.join(jpg_dir,f + extension)
        #print xml_file
        #print img_file
        os.remove(xml_file)
        os.remove(img_file)
    print str(len(rm_list))+' xml-jpg files without obj removed.'
    return
