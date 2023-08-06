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
from dp import utils, constants


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

    def detect(self, image, thresh=.5, hier_thresh=.5, nms=.45):
        """
        目标检测

        :param image: 图像文件地址
        :param thresh: 对象识别置信度（默认>0.5）
        :param hier_thresh: 
        :param nms: 
        :returns: 检测结果
        """
        if utils.get_python_version() == 3:  # python3 need str.encode()
            image = str.encode(image)
        im = self.load_image(image, 0, 0)
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
        return res


if __name__ == "__main__":
    """test"""
    darnet_path = '/Users/yanjingang/project/darknet'
    # init
    dn = Darknet(
        so_file=darnet_path + '/libdarknet.so',
        #cfg_file=darnet_path + '/cfg/yolov3.cfg',
        #model_file=darnet_path + '/yolov3.weights',
        cfg_file=darnet_path + '/cfg/yolov3-tiny.cfg',  # tiny低性能版
        model_file=darnet_path + '/yolov3-tiny.weights',
        meta_file=darnet_path + '/cfg/coco.data',  # 如果命令不在darknet目录执行时，需要把coco.data里的“names = data/coco.names”改为绝对路径
    )
    # detect
    res = dn.detect(darnet_path + '/data/dog.jpg')
    print(res)
