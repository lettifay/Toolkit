import os,csv
from PIL import Image,ImageChops
import xml.etree.cElementTree as ET
import xml.dom.minidom as MD
import cv2

# convert PascalVOC XML to csv(image_name,label_name,x,y,w,h)
def xml2csv(xml_dir,csv_path,jpg_dir,extension='.jpg'):
    annotation_list = []
    for f in os.listdir(xml_dir):
        if f.lower().endswith('.xml'):
            xml_file = os.path.join(xml_dir,f)
            jpg_name = os.path.splitext(f)[0] + extension
            
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for obj in root.findall('object'):
                label_name = obj.find('name').text
                xmin = int(obj.find('bndbox').find('xmin').text)
                ymin = int(obj.find('bndbox').find('ymin').text)
                xmax = int(obj.find('bndbox').find('xmax').text)
                ymax = int(obj.find('bndbox').find('ymax').text)
                x = xmin
                y = ymin
                w = xmax - xmin
                h = ymax - ymin
                annotation_list.append([jpg_name,label_name,x,y,w,h])
    
    with open(csv_path,'wb') as csv_file:
        writer = csv.writer(csv_file)
        for record in annotation_list:
            writer.writerow(record)
    print 'xml2csv done.'

# convert csv(image_name,label_name,x,y,w,h) to PascalVOC XML
def csv2xml(csv_path,xml_dir,jpg_dir,extension='.jpg',dlt=','):
    if not os.path.exists(xml_dir):
        os.mkdir(xml_dir)
    with open(csv_path, 'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=dlt)
        for row in reader:
            img_name,label,x,y,w,h = row
            
            newObj = ET.Element('object')
            ET.SubElement(newObj,"name").text=label
            ET.SubElement(newObj,"pose").text="Unspecified"
            ET.SubElement(newObj,"truncated").text="0"
            ET.SubElement(newObj,"difficult").text="0"
            newBndbox=ET.SubElement(newObj,"bndbox")
            ET.SubElement(newBndbox,"xmin").text=str(int(round(float(x))))
            ET.SubElement(newBndbox,"ymin").text=str(int(round(float(y))))
            ET.SubElement(newBndbox,"xmax").text=str(int(round(float(x)+float(w))))
            ET.SubElement(newBndbox,"ymax").text=str(int(round(float(y)+float(h))))
            
            shortname = os.path.splitext(img_name)[0]
            xml_path = os.path.join(xml_dir,shortname+".xml")
            
            if os.path.exists(xml_path):
                ori_tree = ET.parse(xml_path)
                ori_root = ori_tree.getroot()
                ori_root.insert(0,newObj)
                tree_str = ET.tostring(ori_root,'utf-8')
                ori_tree.write(xml_path,encoding='utf-8')
                
            else:
                annotation=ET.Element("annotation")
                annotation.insert(0,newObj)
            
                folder=ET.SubElement(annotation,"folder")
                folder.text="JPEGImages"
        
                filename=ET.SubElement(annotation,"filename")
                filename.text=shortname
        
                path=ET.SubElement(annotation,"path")
                path.text = os.path.join(jpg_dir,img_name)
        
                source=ET.SubElement(annotation,"source")
                ET.SubElement(source, "database").text = "Unknown"
        
                size=ET.SubElement(annotation,"size")
                im = cv2.imread(os.path.join(jpg_dir,shortname+extension))
                width,height,depth = im.shape
                ET.SubElement(size, "width").text = str(width)
                ET.SubElement(size, "height").text = str(height)
                ET.SubElement(size, "depth").text = str(depth)
            
                segmented=ET.SubElement(annotation,"segmented")
                segmented.text="0"
                
                with open(xml_path, "wb") as f:
                    tree_str = ET.tostring(annotation,'utf-8')
                    reparsed = MD.parseString(tree_str)
                    result = reparsed.toprettyxml(encoding="utf-8",indent="\t")
                    f.write(result)
    print 'csv2xml done.'

# merge several csv files to one csv
def merge_csv(csv_list,merged_csv,dlt=','):
    with open(merged_csv,'wb') as csv_file:
        writer = csv.writer(csv_file)
        for csv_file in csv_list:
            with open(csv_file, 'rb') as csvfile:
                reader = csv.reader(csvfile,delimiter=dlt)
                for row in reader:
                    writer.writerow(row)
            os.remove(csv_file)
    print 'merge_csv done.'