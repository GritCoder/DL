import os
from itertools import islice # d迭代库 暂时没有用到
from PIL import Image,ImageDraw
list_jpg = []
list_txt = []
def listdir(path,list_name):# 获取图片、txt文件路径列表
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):# 判断是否是目录
            listdir(file_path, list_name) # 此处没有执行
        elif os.path.splitext(file_path)[1] == '.jpg':
            list_jpg.append(file_path)
        elif os.path.splitext(file_path)[1] == '.txt':
            list_txt.append(file_path)
    list_jpg.sort()
    list_txt.sort()
    return list_jpg,list_txt

def sign (x,x1,x2,y,y1,y2): # 符号函数
    return (x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)

def isInMatrix_1(x,x1,x2,x3,y,y1,y2,y3): # 判断点是否在三角形区域内,两个三角形构成一个四边形
    d1 = sign(x,x1,x2,y,y1,y2)
    d2 = sign(x,x2,x3,y,y2,y3)
    d3 = sign(x,x3,x1,y,y3,y1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def isInMatrix_2(x,x2,x3,x4,y,y2,y3,y4):
    d1 = sign(x,x2,x3,y,y2,y3)
    d2 = sign(x,x3,x4,y,y3,y4)
    d3 = sign(x,x4,x2,y,y4,y2)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def save_crop(img,item,dest_path,k): # 裁剪图片
    x = int(item[0].split(' ')[0])
    y = int(item[0].split(' ')[1])
    w = int(item[0].split(' ')[2])
    h = int(item[0].split(' ')[3])
    im = Image.open(img).convert('RGB') # 原图本来应该就是RGB,若效果不好,可以不在此处设置convert 备选再议
    cropped = im.crop((x,y,x+w,y+h))
    cropped.save(dest_path + '\\' + 'source' + '\\' + img.split('\\')[-1].split('.')[0] + '_' + str(k) + '.jpg')

def read_txt(txt):# 以检测框为单位,每两行数据是一组,读取txt
    tmp = []
    result = []*2
    f = open(txt)
    lines = f.readlines()
    # 去\n
    for line in lines:
        tmp.append(line.strip())
    #(框、立柱)集合 每两个一组,都在一个列表里面
    for i in range(0,len(tmp),2):
        result.append(tmp[i:i+2])
    return result

def main():
    dest_path = 'D:\\images\\tmp'
    list_jpg, list_txt = listdir(r"D:\images\s", [])
    print(len(list_jpg),len(list_txt))
    for img,txt in zip(list_jpg,list_txt):
        print(img)
        result = read_txt(txt)
        global conut 
        count = 0
        global k 
        k = 0
        for item in result:
            x = int(item[0].split(' ')[0])
            y = int(item[0].split(' ')[1])
            w = int(item[0].split(' ')[2])
            h = int(item[0].split(' ')[3])
            save_crop(img,item,dest_path,k)
            k += 1 # 全局变量一定不要和局部变量重名，特别是在控制逻辑中，吸取教训！
            image = Image.new('RGB', (w, h), (255,255,255))
            draw = ImageDraw.Draw(image)
            for i in range(w):
                for j in range(h):
                    if isInMatrix_1(i,int(item[1].split(',')[0])-x,int(item[1].split(',')[2])-x,int(item[1].split(',')[4])-x,j,int(item[1].split(',')[1])-y,int(item[1].split(',')[3])-y,int(item[1].split(',')[5])-y) or isInMatrix_2(i,int(item[1].split(',')[2])-x,int(item[1].split(',')[4])-x,int(item[1].split(',')[6])-x,j,int(item[1].split(',')[3])-y,int(item[1].split(',')[5])-y,int(item[1].split(',')[7])-y):
                        draw.point((i,j),fill=(255,0,0))
                    elif isInMatrix_1(i,int(item[1].split(',')[4])-x,int(item[1].split(',')[6])-x,int(item[1].split(',')[8])-x,j,int(item[1].split(',')[5])-y,int(item[1].split(',')[7])-y,int(item[1].split(',')[9])-y) or isInMatrix_2(i,int(item[1].split(',')[6])-x,int(item[1].split(',')[8])-x,int(item[1].split(',')[10])-x,j,int(item[1].split(',')[7])-y,int(item[1].split(',')[9])-y,int(item[1].split(',')[11])-y):
                        draw.point((i,j),fill=(255,255,255))
                    elif isInMatrix_1(i,int(item[1].split(',')[8])-x,int(item[1].split(',')[10])-x,int(item[1].split(',')[12])-x,j,int(item[1].split(',')[9])-y,int(item[1].split(',')[11])-y,int(item[1].split(',')[13])-y) or isInMatrix_2(i,int(item[1].split(',')[10])-x,int(item[1].split(',')[12])-x,int(item[1].split(',')[14])-x,j,int(item[1].split(',')[11])-y,int(item[1].split(',')[13])-y,int(item[1].split(',')[15])-y):
                        draw.point((i,j),fill=(255,0,0))
                    elif isInMatrix_1(i,int(item[1].split(',')[12])-x,int(item[1].split(',')[14])-x,int(item[1].split(',')[16])-x,j,int(item[1].split(',')[13])-y,int(item[1].split(',')[15])-y,int(item[1].split(',')[17])-y) or isInMatrix_2(i,int(item[1].split(',')[14])-x,int(item[1].split(',')[16])-x,int(item[1].split(',')[18])-x,j,int(item[1].split(',')[15])-y,int(item[1].split(',')[17])-y,int(item[1].split(',')[19])-y):
                        draw.point((i,j),fill=(255,255,255))
                    elif isInMatrix_1(i,int(item[1].split(',')[16])-x,int(item[1].split(',')[18])-x,int(item[1].split(',')[20])-x,j,int(item[1].split(',')[17])-y,int(item[1].split(',')[19])-y,int(item[1].split(',')[21])-y) or isInMatrix_2(i,int(item[1].split(',')[18])-x,int(item[1].split(',')[20])-x,int(item[1].split(',')[22])-x,j,int(item[1].split(',')[19])-y,int(item[1].split(',')[21])-y,int(item[1].split(',')[23])-y):
                        draw.point((i,j),fill=(255,0,0))
                    else:
                        draw.point((i,j),fill=(0,0,0))
            image.save(dest_path + '\\' + 'train' + '\\' + img.split('\\')[-1].split('.')[0] + '_' + str(count) + '.jpg') 
            count += 1

main()
