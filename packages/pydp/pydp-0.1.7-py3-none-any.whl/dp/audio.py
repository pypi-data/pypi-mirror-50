#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: audio.py
Desc: 音频类
      *注：此文件为音频类基础lib，不可依赖其他任何dp音频库，例如tts/asr等，以避免出现引用环
Date: 2019/2/21 23:34
"""
import subprocess
import tempfile
import threading
import requests
import os
import json
import time
import wave
import sklearn
#import librosa
import logging
from urllib.parse import urlparse
import numpy as np
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
from contextlib import contextmanager
from pydub import AudioSegment
from dp import utils, constants


def play(filename='', callback=None, media='', delete=False, volume=1):
    """
    播放声音（默认声音为报警音）

    :param filename: 要播放的外部音频文件路径
    :param callback: 播放完毕后的回调函数
    :param media: 要播放的内置音频文件名（与filename参数互斥，2选1）
    :param delete: 是否播放完毕后自动删除音频(默认False)
    :param volume: 音量（默认1）
    :returns:
    """
    if filename == '' and media == '':
        filename = constants.APP_PATH + '/data/media/warning.wav'
    elif media != '':
        filename = constants.APP_PATH + '/data/media/' + media
    #logging.info("play: "+filename)
    player = Player()
    player.play(filename, delete=delete, onCompleted=callback, volume=volume)


def get_pcm(filename):
    """ 
    从 mp3或wav 文件中读取 pcm

    :param filename: 文件路径
    :returns: pcm 数据
    """
    if utils.get_ext(filename) == '.mp3':
        filename = convert_mp3_to_wav(filename)
    return get_pcm_from_wav(filename)


def get_pcm_from_wav(wav_path):
    """ 
    从 wav 文件中读取 pcm

    :param wav_path: wav 文件路径
    :returns: pcm 数据
    """
    wav = wave.open(wav_path, 'rb')
    return wav.readframes(wav.getnframes())


def convert_wav_to_mp3(wav_path):
    """ 
    将 wav 文件转成 mp3

    :param wav_path: wav 文件路径
    :returns: mp3 文件路径
    """
    if not os.path.exists(wav_path):
        logging.critical("文件错误 {}".format(wav_path))
        return None
    mp3_path = wav_path.replace('.wav', '.mp3')
    AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3")
    return mp3_path


def convert_mp3_to_wav(mp3_path):
    """ 
    将 mp3 文件转成 wav

    :param mp3_path: mp3 文件路径
    :returns: wav 文件路径
    """
    target = mp3_path.replace(".mp3", ".wav")
    if not os.path.exists(mp3_path):
        logging.critical("文件错误 {}".format(mp3_path))
        return None
    AudioSegment.from_mp3(mp3_path).export(target, format="wav")
    return target


class Player(threading.Thread):
    """异步线程播放音频"""

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.playing = False
        self.pipe = None
        self.delete = False
        self.volume = 1

    def run(self):
        cmd = ['play', '-v', str(self.volume), str(self.src)]
        logging.debug('Executing %s', ' '.join(cmd))

        with tempfile.TemporaryFile() as f:
            self.pipe = subprocess.Popen(cmd, stdout=f, stderr=f)
            self.playing = True
            self.pipe.wait()
            self.playing = False
            f.seek(0)
            output = f.read()
            if output:
                logging.debug("play Output was: '%s'", output)
        if self.delete and os.path.exists(self.src):
            os.remove(self.src)
        if self.onCompleted:
            self.onCompleted()

    def play(self, src, delete=False, onCompleted=None, volume=1):
        self.src = src
        self.delete = delete
        self.onCompleted = onCompleted
        self.volume = volume
        self.start()

    def play_block(self):
        self.run()

    def stop(self):
        if self.pipe:
            self.onCompleted = None
            self.pipe.kill()
            if self.delete:
                os.remove(self.src)

    def is_playing(self):
        return self.playing


MUSIC_URL = "aHR0cDovL29wZW5kYXRhLmJhaWR1LmNvbS9hcGkucGhwP2Zvcm1hdD1qc29uJmllPXV0Zi04Jm9lPXV0Zi04JnJlc291cmNlX2lkPTgwNDEmcXVlcnk9e30mdG49d2lzZXhtbG5ldyZkc3A9aXBob25lJmFscj0x"
LRC_URL = {
    'music.163.com': 'aHR0cDovL211c2ljLjE2My5jb20vYXBpL3NvbmcvbHlyaWMvbHJjP3NvbmdJZD17fSZyYW5kb209e30mc2lnbj17fQ==',
}
LRC_SIGN = {
    'music.163.com': 'YmFpZHVfbHlyaWM=',
}
DOWN_URL = {
    'music.163.com': 'aHR0cDovL211c2ljLjE2My5jb20vc29uZy9tZWRpYS9vdXRlci91cmw/aWQ9e30ubXAz',
}
HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Charset': 'UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
}


def get_music(query, limit=1, cache_path='', force=False):
    """
    根据歌名或歌词获取音乐信息

    :param query: 歌名/歌手/歌词等
    :param limit: 返回搜索条数
    :param cache_path: 缓存音乐信息和首条结果mp3
    :param force: 强制更新音乐信息和mp3缓存（如果cache_path不为空的话）
    :returns: res 音乐信息
    """
    # get cache
    if cache_path != '' and force is False:
        res = utils.pickle_load(os.path.join(cache_path, utils.md5(query)+'.data'))
        if res and len(res['data']) > 0:
            logging.info('get cache!')
            return res
    # 获取信息
    req_url = utils.base64_decode(MUSIC_URL).format(query)
    # print(req_url)
    res = requests.get(req_url, headers=HEADER)
    content = json.loads(res.content.decode("utf8", "ignore"))
    # 格式清理
    res = {'status': 0, 'count': 0, 'limit': limit, 'data': []}
    res['status'] = content['status']
    music_163 = []
    if len(content['data']) > 0:
        res['count'] = content['data'][0]['resNum']
        # songs
        if len(content['data'][0]['result']) > 0 and 'songs' in content['data'][0]['result'][0] and len(content['data'][0]['result'][0]['songs']) > 0:
            for music in content['data'][0]['result'][0]['songs']:
                if len(res['data']) >= limit and music['showUrl'] != 'music.163.com':
                    continue
                # print(music)
                music['showUrl'] = urlparse(music['wap_songUrl']).netloc if 'showUrl' not in music else music['showUrl']
                id = music['musicId'].split('_')[0] if music['showUrl'] == 'music.163.com' else music['musicId']
                lrcContent = music['lrcContent'].replace('\r\n', '\n') if 'lrcContent' in music else ''
                lrcContent = music['lrcContentAll'].replace('\r\n', '\n') if 'lrcContentAll' in music else lrcContent
                if lrcContent == '':  # 歌词获取
                    lrcContent = get_lrc(music['showUrl'], id)
                data = {
                    'id': id,  # id
                    'name': music['songName'],  # 歌名
                    'image': music['musicImage'],  # 封面
                    'singer': music['allSingerName'],  # 歌手
                    'pub_company': music['pubCompany'] if 'pubCompany' in music else '',  # 发行公司
                    'publish_time': music['publishTime'] if 'publishTime' in music else '',  # 发行时间
                    'site': music['siteName'],  # 来源
                    'url': music['wap_songUrl'].replace('&market=baiduqk', '').replace('&from=baidu', ''),  # 歌曲播放页
                    'site_url': music['showUrl'],  # 来源
                    'copyright': music['copyRight'],  # 是否有版权
                    # 'search_url': music['sameNameUrl'].replace('&market=baiduqk', ''),  # 歌曲搜索结果页
                    'down_url': get_down_url(music['showUrl'], id),  # mp3下载地址
                    'duration': music['duration'],  # 时长(秒)
                    'lrc': format_lrc(lrcContent, music['duration'])  # 歌词
                }
                if music['showUrl'] == 'music.163.com':  # 163优先
                    music_163.append(data)
                else:
                    res['data'].append(data)
        # site
        if len(content['data'][0]['result']) > 0 and 'site' in content['data'][0]['result'][0] and len(content['data'][0]['result'][0]['site']) > 0:
            for music in content['data'][0]['result'][0]['site']:
                if 'song' in music:
                    music = music['song']
                    if len(res['data']) >= limit and music['showUrl'] != 'music.163.com':
                        continue
                    id = music['musicId'].split('_')[0] if music['showUrl'] == 'music.163.com' else music['musicId']
                    lrcContent = music['lrcContent'].replace('\r\n', '\n') if 'lrcContent' in music else ''
                    lrcContent = music['lrcContentAll'].replace('\r\n', '\n') if 'lrcContentAll' in music else lrcContent
                    if lrcContent == '':  # 歌词获取
                        lrcContent = get_lrc(music['showUrl'], id)
                    data = {
                        'id': id,  # id
                        'name': music['songName'],  # 歌名
                        'image': music['musicImage'],  # 封面
                        'singer': music['allSingerName'],  # 歌手
                        'pub_company': music['pubCompany'] if 'pubCompany' in music else '',  # 发行公司
                        'publish_time': music['publishTime'] if 'publishTime' in music else '',  # 发行时间
                        'site': music['siteName'],  # 来源
                        'url': music['wap_songUrl'].replace('&market=baiduqk', '').replace('&from=baidu', ''),  # 歌曲播放页
                        'site_url': music['showUrl'],  # 来源
                        'copyright': music['copyRight'],  # 是否有版权
                        # 'search_url': music['sameNameUrl'].replace('&market=baiduqk', ''),  # 歌曲搜索结果页
                        'down_url': get_down_url(music['showUrl'], id),  # mp3下载地址
                        'duration': music['duration'],  # 时长(秒)
                        'lrc': format_lrc(lrcContent, music['duration'])  # 歌词
                    }
                    if music['showUrl'] == 'music.163.com':  # 163优先
                        music_163.append(data)
                    else:
                        res['data'].append(data)

    res['data'] = music_163 + res['data']
    if len(res['data']) > limit:
        for i in range(len(res['data']) - limit):
            res['data'].pop()
    # cache res
    if cache_path != '' and len(res['data']) > 0:
        first_music = res['data'][0]
        # cache mp3
        res['data'][0]['down_file'] = down_music(first_music, cache_path, force=force)
        # cache info by query
        utils.pickle_dump(res, os.path.join(cache_path, utils.md5(query) + '.data'))
        # cache info by music_id
        utils.pickle_dump(res, os.path.join(cache_path, first_music['id'] + '.' + first_music['name'] + '.' + first_music['singer'] + '.data'))
    return res


def get_lrc(site, songid):
    """获取歌词"""
    lrcContent = ''
    if site not in LRC_URL:
        return lrcContent

    # 歌词获取
    if site == 'music.163.com':
        random = utils.md5(time.time())
        sign = utils.md5(songid+utils.base64_decode(LRC_SIGN[site])+random)
        req_url = utils.base64_decode(LRC_URL[site]).format(songid, random, sign)
        # print(req_url)
        res = requests.get(req_url, headers=HEADER)
        lrcContent = res.content.decode("utf8", "ignore")
    return lrcContent


def format_lrc(lrcContent, duration=0):
    """格式化歌词格式"""
    lrc = []
    lrcContent = lrcContent.split('\n')
    for row in lrcContent:
        row = row.split(']', 1)
        if len(row) < 2:
            continue
        t = row[0].strip()[1:]
        c = row[1].strip()
        # 清理非歌词部分
        if c == '' or c[:2] in ('作词', '作曲', '编曲', '制作', '演唱', '箱琴', '口琴', 'MI', '和声', '贝斯', '电琴',  '吉他',
                                '和音', '录音', '混音', 'OP', '出品', '键盘', '监制', '演奏', '专辑', '翻唱', '母带', '混缩'):
            continue
        logging.info(t+'\t' + c)
        lrc.append(
            {
                't': t,  # 开始时间
                'c': utils.clear_punctuation(c),  # 文本
                'ms': 0,  # 时长（毫秒）
            })

    # 补充时长（毫秒）
    duration = int(duration)
    size = len(lrc)
    if duration > 0 and size < 0:
        # print(utils.format_seconds(duration))
        lrc[size - 1]['ms'] = duration*1000 - utils.get_milliseconds(lrc[size - 1]['t'])
    for i in range(size - 2, -1, -1):
        lrc[i]['ms'] = utils.get_milliseconds(lrc[i + 1]['t']) - utils.get_milliseconds(lrc[i]['t'])

    return lrc


def get_down_url(site, songid):
    """获得下载mp3的链接"""
    down_url = ''
    if site not in LRC_URL:
        return down_url

    if site == 'music.163.com':
        down_url = utils.get_redirect_url(utils.base64_decode(DOWN_URL[site]).format(songid))
    return down_url


def down_music(music, save_path, force=False):
    """下载mp3"""
    if music['down_url'] == '' or save_path == '':
        return ''
    save_file = os.path.join(save_path, music['id'] + '.mp3')
    if os.path.exists(save_file) and force is False:  # 已存在时不再重复下载，除非强制要求
        return save_file
    ret = utils.download(music['down_url'], save_file)
    if ret is False:
        return ''
    return save_file


def split_music(source_file, start_ms, end_ms, save_file):
    """
    切割音频

    :param source_file: 原始音频文件
    :param start_ms: 切割开始位置毫秒数
    :param end_ms: 切割结束位置毫秒数
    :param save_file: 切割后的音频保存位置
    :returns: 时长h:m:s格式字符串
    """
    ext = os.path.splitext(source_file)[1]
    song = None
    if ext == '.mp3':
        song = AudioSegment.from_mp3(source_file)
    elif ext == '.wav':
        song = AudioSegment.from_wav(source_file)
    elif ext == '.ogg':
        song = AudioSegment.from_ogg(source_file)
    elif ext == '.flv':
        song = AudioSegment.from_flv(source_file)
    else:
        return False

    return song[start_ms:end_ms].export(save_file, format=ext[1:])


def split_music_by_lrc(music, save_path, offset=0, force=False):
    """
    按歌词时间切割音频

    :param music: 音乐信息&歌词&mp3文件等信息
    :param save_path: 切割后的音频保存位置（保存文件格式：歌名.歌手.片段开始时间.片段长度.片段歌词.mp3；例如：大碗宽面.吴亦凡.112565.2411.快乐才是真谛.mp3）
    :param offset: 歌词偏移时间（毫秒，默认0)
    :param force: 切割文件已存在时是否强制覆盖（默认False）
    :returns: boolean
    """
    if music is None or len(music['lrc']) == 0 or 'down_file' not in music or os.path.exists(music['down_file']) is False:
        return False
    if os.path.exists(save_path) is False:
        utils.mkdir(save_path)

    for lrc in music['lrc']:
        logging.debug(lrc)
        start_ms = utils.get_milliseconds(lrc['t']) + offset
        save_file = save_path + music['name'] + '.' + music['singer'] + '.' + str(start_ms) + '.' + str(lrc['ms']) + '.' + lrc['c'] + '.mp3'
        if os.path.exists(save_file) and force is False:
            continue
        ret = split_music(music['down_file'], start_ms, start_ms + lrc['ms'], save_file)
        logging.debug(ret)
    return True


if __name__ == '__main__':
    """test play wav"""
    utils.init_logging(log_file='audio', log_path=constants.APP_PATH)

    # 播放声音
    play(media='on.wav', callback=None)
    #play('/Users/yanjingang/project/pigrobot/data/tmp/output1559210063.wav', callback=None, delete=True)

    # 提取pcm
    filename = constants.APP_PATH + '/data/media/on.wav'
    pcm = get_pcm_from_wav(filename)
    # print(pcm)

    # 转换音频格式
    # convert_wav_to_mp3(filename)

    # 获取歌曲信息&歌词
    catch_path = constants.APP_PATH + '/data/tmp/'
    name = '吴亦凡大碗宽面'
    res = get_music(name, cache_path=catch_path)  # , force=True)
    print(res)
    # print(len(res['data']))

    # 按歌词切割音频
    '''
    if len(res['data']) > 0:
        music = res['data'][0]
        ret = split_music_by_lrc(music, catch_path + 'split/', offset=0)  # , force=True)
        print(ret)
    '''

    '''
    # 根据音波切为单字片段
    for filename in os.listdir(save_path):
        if filename in utils.SKIPS:
            continue
        filename = '大碗宽面.吴亦凡.153494.5154.我这一生漂泊四海看淡了今朝.mp3'
        name, singer, t, ms, c, ext = filename.split('.')
        print(name, singer, t, ms, c, ext)
        # 声波采样
        x, sr = librosa.load(save_path + filename, sr=100)  # , sr=44100)
        print(type(x), type(sr))
        print(x.shape, sr)
        print(x)
        x = np.where(x > 0.005, x, 0)  # 采样<0.05的直接设置为0
        print(x)
        break
    '''
