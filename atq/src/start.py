import os
from datetime import datetime

import sys
from PIL import Image
from aip import AipOcr
from selenium import webdriver

APP_ID = '10646355'
API_KEY = 'yGSQzcabg1Qb2ZHFAwVBuyMy'
SECRET_KEY = '3K0MSeFVLmWZ25FYFlVbMF5Pn52f42j1'
WEB_DRIVER = webdriver.Chrome('/Applications/Google Chrome.app/Contents/MacOS/chromedriver')


def choose(choosed):
    # TODO get x y
    cmd = ''
    if choosed == 1:
        cmd = 'adb shell input tap 540 709'
    elif choosed == 2:
        cmd = 'adb shell input tap 540 895'
    elif choosed == 3:
        cmd = 'adb shell input tap 540 1095'
    os.system(cmd)


def logger(msg, level='INFO'):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print >> sys.stdout, '[%s] %s %s' % (now, level, msg)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def pull_screen_shot():
    os.system('adb shell screencap -p /sdcard/screen_shot.png')
    os.system('adb pull /sdcard/screen_shot.png ../res/')
    logger('Get screen shot successful')


def crop_img():
    image = Image.open('../res/screen_shot.png')
    image_size = image.size
    print image_size
    width = image_size[0]
    height = image_size[1]
    region = image.crop((0, height * 0.15, width, height * 0.7))
    region.save('../res/screen_shot_crop.png')
    logger('Crop Image successful')


def ocr():
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content('../res/screen_shot_crop.png')
    ret = client.basicGeneral(image)
    if ret['words_result_num'] > 0:
        logger('Image identify successful')
        return ret
    else:
        logger('Image identify failed')


def search(str):
    url = 'https://www.baidu.com/s?wd=%s' % str
    WEB_DRIVER.get(url)
    logger('Open result in browser')


def analysis():
    pull_screen_shot()
    crop_img()
    result = ocr()
    if result:
        ask = ''
        lines = result['words_result']
        for line in lines:
            logger(line['words'])
        
        if len(lines) == 4:
            ask = lines[0]['words']
            q1 = lines[1]['words']
            q2 = lines[2]['words']
            q3 = lines[3]['words']
        elif len(lines) == 5:
            ask = lines[0]['words'] + lines[1]['words']
            q1 = lines[2]['words']
            q2 = lines[3]['words']
            q3 = lines[4]['words']
        elif len(lines) > 5:
            ask = lines[0]['words'] + lines[1]['words'] + lines[2]['words']
        
        logger('QUESTION:' + ask)
        search(ask)


if '__main__' == __name__:
    WEB_DRIVER.get('https://www.baidu.com')
    while True:
        input = raw_input(
            "Menu:--\n1:Choose Answer 1;\n2:Choose Answer 2;\n3:Choose Answer 3;\n4:Random Answer\n5:Auto Analysis\n")
        if input == '1':
            choose(1)
        elif input == '2':
            choose(2)
        elif input == '3':
            choose(3)
        elif input == '4':
            choose(4)
        elif input == '5':
            analysis()
        else:
            print 'unknow'
