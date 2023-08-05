# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import face_recog_bridge
from bayeslibs.config import const


class ApolloFaceRecognizer:
    """
    人脸识别模块封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def open(is_show=True):
        return open_face_recognizer(is_show)

    @staticmethod
    def close():
        return close_face_recognizer()

    @staticmethod
    def persons():
        return get_faces_recognized()


def open_face_recognizer(is_show=True):
    """
    开启机器人人脸识别功能
    :param
    :return:result
    :example:
        result = open_face_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = face_recog_bridge(req_type=const.TYPE_START, is_show=is_show)
    return result


def close_face_recognizer():
    """
    关闭机器人人脸识别功能
    :param 
    :return:result
    :example:
        result = close_face_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = face_recog_bridge(req_type=const.TYPE_STOP)
    return result


def get_faces_recognized():
    """
    查询机器人人脸识别出的人脸信息
    :return:result
    :example:
        result = get_faces_recognized()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                 {
                    'face_name':'qianyang',
                    'score':95,
                    'width':123,
                    'height':223,
                    'top':12,
                    'left':33
                 },
                 {
                    'face_name':'shuqing',
                    'score':99,
                    'width':63,
                    'height':53,
                    'top':121,
                    'left':133
                 },
                 {...}
            ]
        }
    """
    result = face_recog_bridge(req_type=const.TYPE_QUERY)
    return result
