import cv2
import numpy as np
from fastiecm import fastiecm
import csv
def dms2dd(degrees, minutes, seconds):
    if degrees < 0:
        minutes *= -1
        seconds *= -1
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    return dd;
def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi
def green_color_detection(image):
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,50,50), (360,255,255))
    result = cv2.bitwise_and(color_mapped_image,color_mapped_image,mask=mask)
    result = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)
    green = cv2.inRange(result, (20,0,0), (100,255,255))
    green_perc = (green==255).mean() * 100
    print('green percentage:', np.round(green_perc, 2))
    return green_perc
def yellow_color_detection(image):
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,50,50), (360,255,255))
    result = cv2.bitwise_and(color_mapped_image,color_mapped_image,mask=mask)
    result = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)
    yellow = cv2.inRange(result, (15,0,0), (20,255,255))
    yellow_perc = (yellow==255).mean() * 100
    print('yellow percentage:', np.round(yellow_perc, 2))
    return yellow_perc
def red_color_detection(image):
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,50,50), (360,255,255))
    result = cv2.bitwise_and(color_mapped_image,color_mapped_image,mask=mask)
    result = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)
    red = cv2.inRange(result, (1,0,0), (10,255,255))
    red_perc = (red==255).mean() * 100
    print('red percentage', np.round(red_perc, 2))
    return red_perc
def blue_color_detection(image):
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,50,50), (360,255,255))
    result = cv2.bitwise_and(color_mapped_image,color_mapped_image,mask=mask)
    result = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(result, (120,0,0), (123,255,255))
    blue_perc = (blue==255).mean() * 100
    print('blue percentage', np.round(blue_perc, 2))
    return blue_perc
def Display(image, image_name):
    image = np.array(image,dtype = float)/float(255)
    shape = image.shape
    height = int(shape[0] / 2)
    width = int(shape[1] / 2)
    image = cv2.resize(image, (width,height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi
def add_csv_data(data_file, data):
    with open(data_file, 'a', buffering = 1) as f:
        writer = csv.writer(f)
        writer.writerow(data)
data_file = 'poze_ndvi/data.csv'
with open(data_file, 'w', buffering=1) as f:
    writer = csv.writer(f)
    header = ("imageNumber","red percentage","yellow percentage","green percentage","blue percentage","latitude","longitude")
    writer.writerow(header)
number = ""
lat = ""
latitudes = [0]
longitudes = [0]
with open("/home/pi/Desktop/poze/data.csv",'r') as csvfile:
    tabel = csv.reader(csvfile)
    for row in tabel:
        str = row[0]
        lat = ""
        split = str.split(',')
        deg = 0
        try:
            img = split[0]
            number = img.split('e')
            number = number[1].split('.')
            number = number[0]
            image = cv2.imread('/home/pi/Desktop/poze/' + img)
            contrasted = contrast_stretch(image)
            ndvi = calc_ndvi(contrasted)
            ndvi = contrast_stretch(ndvi)
            color_mapped_prep = ndvi.astype(np.uint8)
            color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
            cv2.imwrite('poze_ndvi/' + number + '_ndvi.jpg',color_mapped_image)
            masked_green = green_color_detection(color_mapped_image)
            masked_yellow = yellow_color_detection(color_mapped_image)
            masked_red = red_color_detection(color_mapped_image)
            masked_blue = blue_color_detection(color_mapped_image)
            lat = split[2].split('"')
            lat2 = lat[1].split(' ')
            deg = float(lat2[0][0] + lat2[0][1])
            minutes = float(lat2[1][0] + lat2[1][1])
            seconds = float(lat2[2])
            lati = dms2dd(deg,minutes,seconds)
            long = split[3].split('"')
            long2 = long[1].split(' ')
            degstr2 = long2[0].split('d')
            deg2 = float(degstr2[0])
            minstr2 = long2[1].split("'")
            minutes2 = float(minstr2[0])
            seconds2 = float(long2[2])
            print(deg2)
            print(minutes2)
            print(seconds2)
            longi = dms2dd(deg2,minutes2,seconds2)
            now = (number,masked_red,masked_yellow,masked_green,masked_blue,lati,longi)
            latitudes.append(lati)
            longitudes.append(longi)
            add_csv_data(data_file, now)
        except Exception as E:
            print(number)
