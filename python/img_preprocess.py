from PIL import Image
import os

def pad2square(img_dir,out_dir,extension='.jpg'):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    extension_list=['.jpg','.jpeg','.png']
    for f in os.listdir(img_dir):
        if os.path.splitext(f)[1] in extension_list:
            img_file = os.path.join(img_dir,f)
            img = Image.open(img_file)
            height,width = img.size
            side = max(height,width)
            out = img.crop((0,0,side,side))
            shortname = os.path.splitext(f)[0]
            out.save(os.path.join(out_dir,shortname+extension))
    print 'pad2square done.'

# size=(64,64) in pixel
def resize(size,img_dir,out_dir,extension='.jpg'):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    extension_list=['.jpg','.jpeg','.png']
    for f in os.listdir(img_dir):
        if os.path.splitext(f)[1] in extension_list:
            img_file = os.path.join(img_dir,f)
            img = Image.open(img_file)
            out = img.resize(size)
            shortname = os.path.splitext(f)[0]
            out.save(os.path.join(out_dir,shortname+extension))
    print 'resize done.'



