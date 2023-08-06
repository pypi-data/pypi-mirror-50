#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: darknet.py
Desc: 图像目标识别封装
Author:yanjingang(yanjingang@mail.com)
Date: 2019/8/2 23:34
"""

from ctypes import *
import math
import random
import cv2
import logging
import time
from dp import utils, constants


# Darknet detect出的所有label枚举
LABELS = {
    'person': {
        'name': '人',
        'unit': '个',
        'units': '一群',
    },
    'bicycle': {
        'name': '自行车',
        'unit': '辆',
        'units': '很多',
    },
    'car': {
        'name': '汽车',
        'unit': '辆',
        'units': '很多',
    },
    'motorbike': {
        'name': '摩托车',
        'unit': '辆',
        'units': '很多',
    },
    'aeroplane': {
        'name': '飞机',
        'unit': '架',
        'units': '很多',
    },
    'bus': {
        'name': '公共汽车',
        'unit': '辆',
        'units': '很多',
    },
    'train': {
        'name': '火车',
        'unit': '列',
        'units': '很多',
    },
    'truck': {
        'name': '卡车',
        'unit': '辆',
        'units': '很多',
        'category': 'car',  # 用于识别不准确的分类合并
    },
    'boat': {
        'name': '船',
        'unit': '艘',
        'units': '很多',
    },
    'traffic light': {
        'name': '红绿灯',
        'unit': '个',
        'units': '',
    },
    'fire hydrant': {
        'name': '消防栓',
        'unit': '个',
        'units': '',
    },
    'stop sign': {
        'name': '停止标志',
        'unit': '个',
        'units': '很多',
    },
    'parking meter': {
        'name': '停车收费表',
        'unit': '个',
        'units': '很多',
    },
    'bench': {
        'name': '长凳',
        'unit': '个',
        'units': '很多',
    },
    'bird': {
        'name': '鸟',
        'unit': '只',
        'units': '一群',
    },
    'cat': {
        'name': '猫',
        'unit': '只',
        'units': '一群',
    },
    'dog': {
        'name': '狗',
        'unit': '只',
        'units': '一群',
    },
    'horse': {
        'name': '马',
        'unit': '匹',
        'units': '一群',
    },
    'sheep': {
        'name': '羊',
        'unit': '只',
        'units': '一群',
    },
    'cow': {
        'name': '牛',
        'unit': '只',
        'units': '一群',
    },
    'elephant': {
        'name': '大象',
        'unit': '只',
        'units': '一群',
    },
    'bear': {
        'name': '熊',
        'unit': '只',
        'units': '一群',
    },
    'zebra': {
        'name': '斑马',
        'unit': '屁',
        'units': '一群',
    },
    'giraffe': {
        'name': '长颈鹿',
        'unit': '只',
        'units': '一群',
    },
    'backpack': {
        'name': '背包',
        'unit': '个',
        'units': '很多',
    },
    'umbrella': {
        'name': '雨伞',
        'unit': '把',
        'units': '很多',
    },
    'handbag': {
        'name': '手提包',
        'unit': '个',
        'units': '很多',
    },
    'tie': {
        'name': '领带',
        'unit': '条',
        'units': '很多',
    },
    'suitcase': {
        'name': '手提箱',
        'unit': '只',
        'units': '很多',
    },
    'frisbee': {
        'name': '飞盘',
        'unit': '个',
        'units': '很多',
    },
    'skis': {
        'name': '滑雪板',
        'unit': '个',
        'units': '很多',
    },
    'snowboard': {
        'name': '滑雪单板',
        'unit': '个',
        'units': '很多',
    },
    'sports ball': {
        'name': '球',
        'unit': '个',
        'units': '很多',
    },
    'kite': {
        'name': '风筝',
        'unit': '支',
        'units': '很多',
    },
    'baseball bat': {
        'name': '棒球棒',
        'unit': '支',
        'units': '很多',
    },
    'baseball glove': {
        'name': '棒球手套',
        'unit': '个',
        'units': '很多',
    },
    'skateboard': {
        'name': '滑板',
        'unit': '个',
        'units': '很多',
    },
    'surfboard': {
        'name': '冲浪板',
        'unit': '个',
        'units': '很多',
    },
    'tennis racket': {
        'name': '网球拍',
        'unit': '个',
        'units': '很多',
    },
    'bottle': {
        'name': '瓶子',
        'unit': '个',
        'units': '很多',
    },
    'wine glass': {
        'name': '红酒杯',
        'unit': '个',
        'units': '很多',
    },
    'cup': {
        'name': '杯子',
        'unit': '个',
        'units': '很多',
    },
    'fork': {
        'name': '叉子',
        'unit': '个',
        'units': '很多',
    },
    'knife': {
        'name': '刀',
        'unit': '把',
        'units': '很多',
    },
    'spoon': {
        'name': '勺',
        'unit': '个',
        'units': '很多',
    },
    'bowl': {
        'name': '碗',
        'unit': '个',
        'units': '很多',
    },
    'banana': {
        'name': '香蕉',
        'unit': '根',
        'units': '很多',
    },
    'apple': {
        'name': '苹果',
        'unit': '个',
        'units': '很多',
    },
    'sandwich': {
        'name': '三明治',
        'unit': '个',
        'units': '很多',
    },
    'orange': {
        'name': '橙子',
        'unit': '个',
        'units': '很多',
    },
    'broccoli': {
        'name': '西兰花',
        'unit': '个',
        'units': '很多',
    },
    'carrot': {
        'name': '胡萝卜',
        'unit': '根',
        'units': '很多',
    },
    'hot dog': {
        'name': '热狗',
        'unit': '个',
        'units': '很多',
    },
    'pizza': {
        'name': '披萨',
        'unit': '个',
        'units': '很多',
    },
    'donut': {
        'name': '甜甜圈',
        'unit': '个',
        'units': '很多',
    },
    'cake': {
        'name': '蛋糕',
        'unit': '个',
        'units': '很多',
    },
    'chair': {
        'name': '椅子',
        'unit': '把',
        'units': '很多',
    },
    'sofa': {
        'name': '沙发',
        'unit': '个',
        'units': '很多',
    },
    'pottedplant': {
        'name': '盆栽',
        'unit': '盆',
        'units': '很多',
    },
    'bed': {
        'name': '床',
        'unit': '个',
        'units': '很多',
    },
    'diningtable': {
        'name': '餐桌',
        'unit': '个',
        'units': '很多',
    },
    'toilet': {
        'name': '厕所',
        'unit': '个',
        'units': '',
    },
    'tvmonitor': {
        'name': '电视',
        'unit': '个',
        'units': '很多',
    },
    'laptop': {
        'name': '笔记本电脑',
        'unit': '个',
        'units': '很多',
    },
    'mouse': {
        'name': '鼠标',
        'unit': '个',
        'units': '很多',
    },
    'remote': {
        'name': '遥控器',
        'unit': '个',
        'units': '很多',
    },
    'keyboard': {
        'name': '键盘',
        'unit': '个',
        'units': '很多',
    },
    'cell phone': {
        'name': '手机',
        'unit': '个',
        'units': '很多',
    },
    'microwave': {
        'name': '微波炉',
        'unit': '个',
        'units': '',
    },
    'oven': {
        'name': '烤箱',
        'unit': '个',
        'units': '',
    },
    'toaster': {
        'name': '烤面包机',
        'unit': '个',
        'units': '',
    },
    'sink': {
        'name': '洗碗池',
        'unit': '个',
        'units': '',
    },
    'refrigerator': {
        'name': '冰箱',
        'unit': '个',
        'units': '',
    },
    'book': {
        'name': '书',
        'unit': '个',
        'units': '很多',
    },
    'clock': {
        'name': '时钟',
        'unit': '个',
        'units': '很多',
    },
    'vase': {
        'name': '花瓶',
        'unit': '个',
        'units': '很多',
    },
    'scissors': {
        'name': '剪刀',
        'unit': '个',
        'units': '很多',
    },
    'teddy bear': {
        'name': '泰迪熊',
        'unit': '个',
        'units': '很多',
    },
    'hair drier': {
        'name': '吹风机',
        'unit': '个',
        'units': '很多',
    },
    'toothbrush': {
        'name': '牙刷',
        'unit': '把',
        'units': '很多',
    },
}


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


class Darknet():
    """darknet封装"""

    def __init__(self,
                 so_file='./libdarknet.so',
                 cfg_file='./cfg/yolov3.cfg',
                 model_file='./yolov3.weights',
                 meta_file='cfg/coco.data'):
        """
        初始化

        :param so_file: 编译好的libdarknet.so文件位置
        :param cfg_file: 模型配置文件yolov3.cfg位置
        :param model_file: 模型网络权重文件yolov3.weights位置
        :param meta_file: meato文件coco.data位置
        :returns: 
        """
        # darknet func
        self.load_net = None
        self.load_meta = None
        self.get_network_boxes = None
        self.do_nms_obj = None
        self.free_image = None
        self.free_detections = None
        self.load_image = None
        self.predict_image = None

        # init libdarknet.so
        lib = CDLL(so_file, RTLD_GLOBAL)
        lib.network_width.argtypes = [c_void_p]
        lib.network_width.restype = c_int
        lib.network_height.argtypes = [c_void_p]
        lib.network_height.restype = c_int

        predict = lib.network_predict
        predict.argtypes = [c_void_p, POINTER(c_float)]
        predict.restype = POINTER(c_float)

        set_gpu = lib.cuda_set_device
        set_gpu.argtypes = [c_int]

        make_image = lib.make_image
        make_image.argtypes = [c_int, c_int, c_int]
        make_image.restype = IMAGE

        self.get_network_boxes = lib.get_network_boxes
        self.get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
        self.get_network_boxes.restype = POINTER(DETECTION)

        make_network_boxes = lib.make_network_boxes
        make_network_boxes.argtypes = [c_void_p]
        make_network_boxes.restype = POINTER(DETECTION)

        self.free_detections = lib.free_detections
        self.free_detections.argtypes = [POINTER(DETECTION), c_int]

        free_ptrs = lib.free_ptrs
        free_ptrs.argtypes = [POINTER(c_void_p), c_int]

        network_predict = lib.network_predict
        network_predict.argtypes = [c_void_p, POINTER(c_float)]

        reset_rnn = lib.reset_rnn
        reset_rnn.argtypes = [c_void_p]

        self.load_net = lib.load_network
        self.load_net.argtypes = [c_char_p, c_char_p, c_int]
        self.load_net.restype = c_void_p

        self.do_nms_obj = lib.do_nms_obj
        self.do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        do_nms_sort = lib.do_nms_sort
        do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        self.free_image = lib.free_image
        self.free_image.argtypes = [IMAGE]

        letterbox_image = lib.letterbox_image
        letterbox_image.argtypes = [IMAGE, c_int, c_int]
        letterbox_image.restype = IMAGE

        self.load_meta = lib.get_metadata
        lib.get_metadata.argtypes = [c_char_p]
        lib.get_metadata.restype = METADATA

        self.load_image = lib.load_image_color
        self.load_image.argtypes = [c_char_p, c_int, c_int]
        self.load_image.restype = IMAGE

        rgbgr_image = lib.rgbgr_image
        rgbgr_image.argtypes = [IMAGE]

        self.predict_image = lib.network_predict_image
        self.predict_image.argtypes = [c_void_p, IMAGE]
        self.predict_image.restype = POINTER(c_float)

        # init net/meta
        if utils.get_python_version() == 3:  # python3 need str.encode()
            cfg_file = str.encode(cfg_file)
            model_file = str.encode(model_file)
            meta_file = str.encode(meta_file)
        #print(cfg_file, model_file, meta_file)
        self.net = self.load_net(cfg_file, model_file, 0)
        self.meta = self.load_meta(meta_file)

    def sample(self, probs):
        s = sum(probs)
        probs = [a/s for a in probs]
        r = random.uniform(0, 1)
        for i in range(len(probs)):
            r = r - probs[i]
            if r <= 0:
                return i
        return len(probs)-1

    def c_array(self, ctype, values):
        arr = (ctype*len(values))()
        arr[:] = values
        return arr

    def classify(self, im):
        out = self.predict_image(self.net, im)
        res = []
        for i in range(self.meta.classes):
            res.append((self.meta.names[i], out[i]))
        res = sorted(res, key=lambda x: -x[1])
        return res

    @classmethod
    def get_label(cls, label):
        """获得label英文名(识别不准确的分类合并)"""
        if label in LABELS and 'category' in LABELS[label]:
            return LABELS[label]['category']
        return label

    def detect(self, img_file, thresh=.25, hier_thresh=.25, nms=.15, tag=False):
        """
        目标检测

        :param img_file: 图像文件地址
        :param thresh: 对象识别置信度（默认>0.5）
        :param hier_thresh: 
        :param nms: 
        :param tag: 是否在图片上标注识别结果（默认False）
        :returns: 检测结果
        """
        if utils.get_python_version() == 3:  # python3 need str.encode()
            img_file = str.encode(img_file)
        im = self.load_image(img_file, 0, 0)
        num = c_int(0)
        pnum = pointer(num)
        self.predict_image(self.net, im)
        dets = self.get_network_boxes(self.net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
        num = pnum[0]
        if (nms):
            self.do_nms_obj(dets, num, self.meta.classes, nms)

        res = []
        for j in range(num):
            for i in range(self.meta.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    res.append((self.meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
        res = sorted(res, key=lambda x: -x[1])
        self.free_image(im)
        self.free_detections(dets, num)
        logging.info(res)

        # 数据格式化
        result = []
        uniq = set()
        for o in res:
            # 目标分类合并
            label = self.get_label(str(o[0], 'utf-8'))
            x, y, w, h = o[2]
            left = int(x - w / 2)
            right = int(x + w / 2)
            top = int(y - h / 2)
            bottom = int(y + h / 2)
            # 目标中心点相对位置
            rl_pos = round(((right - left) / 2 + left) / im.w, 2)
            tb_pos = round(((bottom - top) / 2 + top) / im.h, 2)
            pos_name = '前方'  # 主视角方位名
            if rl_pos >= 0.75 and tb_pos <= 0.25:
                pos_name = '右前方'
            elif rl_pos >= 0.75 and tb_pos >= 0.75:
                pos_name = '右下方'
            elif rl_pos <= 0.25 and tb_pos <= 0.25:
                pos_name = '左前方'
            elif rl_pos <= 0.25 and tb_pos >= 0.75:
                pos_name = '左下方'

            # 轮廓去重（用于同轮廓多分类场景）
            rect_id = utils.md5("{},{},{},{}".format(left, right, top, bottom))
            if rect_id in uniq:
                logging.info('uniq! {}'.format(label))
                continue

            # 同分类轮廓嵌套清理
            # -历史目标完全嵌套了当前目标
            skip = False
            for i in range(len(result) - 1, -1, -1):
                obj = result[i]
                if obj['label'] != label:  # 嵌套只同分类才清理
                    continue
                # 有历史目标完全嵌套了当前目标
                if obj['rect'][0] < left and obj['rect'][2] < top and obj['rect'][1] > right and obj['rect'][3] > bottom:
                    logging.info('skip! {}'.format(label))
                    skip = True
                    break
            if skip:
                continue
            # -当前目标可以保留时，检查是否需要替换历史目标
            for i in range(len(result) - 1, -1, -1):
                obj = result[i]
                if obj['label'] != label:  # 嵌套只同分类才清理
                    continue
                # 当前目标完全嵌套了历史目标
                if obj['rect'][0] > left and obj['rect'][2] > top and obj['rect'][1] < right and obj['rect'][3] < bottom:
                    del (result[i])
                    logging.info('clear {} {} !'.format(label, i))

            # 保存目标对象
            data = {
                'label': label,  # 目标英文label
                'label_name': LABELS[label]['name'],    # 目标中文label
                'weight': round(o[1], 4),   # 目标置信度
                'rect': (left, right, top, bottom),  # 目标位置
                'pos': (rl_pos, tb_pos, pos_name),  # 目标相对位置(左右位置, 上下位置, 主视角度方位名)
            }
            result.append(data)
            uniq.add(rect_id)
        # print(result)

        # 在图片上标注识别结果
        if tag and len(result) > 0:
            img_file = str(img_file, 'utf-8')
            print(img_file)
            image = cv2.imread(img_file)
            for obj in result:
                left, right, top, bottom = obj['rect']
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(image, '{} {}'.format(obj['label'], round(obj['weight'], 2)), (left + 6, top + 12), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
            cv2.imwrite(img_file, image)
        return result

    def caption(self, result, thresh=0.25):
        """
        生成图像目标检测的文本描述

        :param result: detect目标检测结果
        :returns: str {'pos': '前方有汽车,自行车,狗.右前方有红绿灯.', 'label': '汽车,自行车,狗,红绿灯', 'label_all': '汽车,自行车,狗,卡车,红绿灯'}
        """
        # 1.汇总
        label_stat_all = {}  # 按检测目标统计（不论概率多少都统计）
        label_stat = {}  # 按检测目标统计(只检测概率>thresh的目标)
        pos_stat = {}  # 按方位+目标统计(只检测概率>thresh的目标)
        for obj in result:
            label = obj['label']
            pos_name = obj['pos'][2]
            # 1.1按检测目标统计（不论概率多少都统计）
            if label not in label_stat:
                label_stat_all[label] = {'cnt': 0, 'pos_name': pos_name}
            label_stat_all[label]['cnt'] += 1
            if obj['weight'] < thresh:
                continue
            # 1.2按检测目标统计(只检测概率>thresh的目标)
            if label not in label_stat:
                label_stat[label] = {'cnt': 0, 'pos_name': pos_name}
            label_stat[label]['cnt'] += 1
            # 1.3按方位+目标统计(只检测概率>thresh的目标)
            if pos_name not in pos_stat:
                pos_stat[pos_name] = {}
            if label not in pos_stat[pos_name]:
                pos_stat[pos_name][label] = 0
            pos_stat[pos_name][label] += 1
        #label_sort = sorted(label_stat.items(), key=lambda x: x[1], reverse=True)
        #print(label_stat, label_sort)
        # 2.组织表达
        # 2.1按label_all组织表达
        caption_label_all = ''
        for label in label_stat_all:
            count = label_stat_all[label]['cnt']
            pos_name = label_stat_all[label]['pos_name']
            if count < 3:
                caption_label_all += '{},'.format(LABELS[label]['name'])
            elif count >= 3:
                caption_label_all += '{}{},'.format(LABELS[label]['units'], LABELS[label]['name'])
            # else:
            #    caption_label_all += '{}{}{},'.format(utils.NUMERALS[count], LABELS[label]['unit'], LABELS[label]['name'])
        # 2.2按label组织表达
        caption_label = ''
        for label in label_stat:
            count = label_stat[label]['cnt']
            pos_name = label_stat[label]['pos_name']
            if count < 3:
                caption_label += '{},'.format(LABELS[label]['name'])
            elif count >= 3:
                caption_label += '{}{},'.format(LABELS[label]['units'], LABELS[label]['name'])
            # else:
            #    caption_label += '{}{}{},'.format(utils.NUMERALS[count], LABELS[label]['unit'], LABELS[label]['name'])
        # 2.3按方位组织表达
        caption_pos = ''
        for pos_name in pos_stat:
            caption_pos += '{}有'.format(pos_name)
            for label in pos_stat[pos_name]:
                count = pos_stat[pos_name][label]
                if count < 3:
                    caption_pos += '{},'.format(LABELS[label]['name'])
                elif count >= 3:
                    caption_pos += '{}{},'.format(LABELS[label]['units'], LABELS[label]['name'])
                # else:
                #    caption_pos += '{}{}{},'.format(utils.NUMERALS[count], LABELS[label]['unit'], LABELS[label]['name'])

            caption_pos = caption_pos[:-1] + '.'

        return {'pos': caption_pos, 'label': caption_label[:-1], 'label_all': caption_label_all[:-1]}

    def detect_camera(self, camera_id=0, window_name="Camera Object Detect (process Q to exit)", thresh=0.25, hier_thresh=0.25, nms=0.15):
        """
        摄像头目标检测

        :param camera_id: 摄像头id
        :param window_name: windows窗口标题
        :param thresh: 对象识别置信度默认>0.55
        :returns: 
        """
        process_this_frame = True
        video_capture = cv2.VideoCapture(camera_id)

        # cv2 window
        cv2.namedWindow(window_name, 0)
        cv2.moveWindow(window_name, 60, 0)
        ret, image = video_capture.read()
        (window_width, window_height, color_number) = image.shape
        logging.info("{} {} {}".format(window_width, window_height, color_number))
        cv2.resizeWindow(window_name, window_height, window_width)
        print(window_height, window_width)

        # detect
        while True:
            # get cap
            ret, image = video_capture.read()
            # print(ret)
            if ret is False:
                logging.warning("video_capture.read: {} {}".format(ret, image))
                continue
            # get re
            res = []
            if process_this_frame:
                image_file = '{}/camera-{}.png'.format(constants.TEMP_PATH, int(time.time() * 1000))
                cv2.imwrite(image_file, image)
                # 目标检测
                res = self.detect(image_file, thresh=thresh, hier_thresh=hier_thresh, nms=nms)
            # show
            process_this_frame = not process_this_frame
            for obj in res:
                print(obj)
                if obj['weight'] < thresh:
                    continue
                left, right, top, bottom = obj['rect']
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, '{} {}'.format(obj['label'], round(obj['weight'], 2)), (left + 6, top + 12), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)

            # show
            cv2.imshow(window_name, image)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(200) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    """test"""
    # log
    utils.init_logging(log_file='darknet', log_path=constants.APP_PATH)

    # init
    darnet_path = '/Users/yanjingang/project/darknet'
    dn = Darknet(
        so_file=darnet_path + '/libdarknet.so',
        #cfg_file=darnet_path + '/cfg/yolov3.cfg',
        #model_file=darnet_path + '/yolov3.weights',
        cfg_file=darnet_path + '/cfg/yolov3-tiny.cfg',  # tiny低性能版
        model_file=darnet_path + '/yolov3-tiny.weights',
        meta_file=darnet_path + '/cfg/coco.data',  # 如果命令不在darknet目录执行时，需要把coco.data里的“names = data/coco.names”改为绝对路径
    )
    # detect检测
    res = dn.detect(darnet_path + '/data/dog.jpg')  # , tag=True)
    #res = dn.detect(darnet_path + '/data/dog-test.jpg')
    print(res)

    # caption理解
    res = dn.caption(res)
    print(res)

    # camera detect
    #dn.detect_camera(thresh=0.25, hier_thresh=0.25, nms=0.15)
    '''
    video_capture = cv2.VideoCapture(0)
    while True:
        # time.sleep(0.5)
        ret, image = video_capture.read()
        # print(ret)
        if ret is False:
            print("video_capture.read fail: {} {}".format(ret, image))
            continue
        image_file = '{}/camera-{}.png'.format(constants.TEMP_PATH, int(time.time() * 1000))
        cv2.imwrite(image_file, image)
        res = dn.detect(image_file)
        print(res)
    video_capture.release()
    '''
