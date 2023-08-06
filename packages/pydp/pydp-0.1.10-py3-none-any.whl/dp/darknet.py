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

    def detect(self, img_file, thresh=.5, hier_thresh=.5, nms=.45, tag=False):
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
        # 数据格式化
        result = []
        for o in res:
            x, y, w, h = o[2]
            left = int(x - w / 2)
            right = int(x + w / 2)
            top = int(y - h / 2)
            bottom = int(y + h / 2)
            result.append({'label': str(o[0], 'utf-8'), 'weight': round(o[1], 4), 'rect': (left, right, top, bottom)})
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
    # detect
    res = dn.detect(darnet_path + '/data/dog.jpg')
    #res = dn.detect(darnet_path + '/data/dog-test.jpg', tag=True)
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
