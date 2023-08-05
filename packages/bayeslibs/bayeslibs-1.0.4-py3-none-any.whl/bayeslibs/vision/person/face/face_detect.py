# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import face_detect_bridge
from bayeslibs.config import const


class ApolloFaceDetector:
    """
    人脸检测模块封装类
    """

    def __init__(self):
        pass

    @staticmethod
    def open(is_show=True):
        return open_face_detector(is_show)

    @staticmethod
    def close():
        return close_face_detector()

    @staticmethod
    def faces():
        return get_faces_detected()


def open_face_detector(is_show=True):
    """
    开启机器人人脸检测功能
    :param
    :return:result
    :example:
        result = open_people_detector()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = face_detect_bridge(req_type=const.TYPE_START, is_show=is_show)
    return result


def close_face_detector():
    """
    关闭机器人人脸检测功能
    :param 
    :return:result
    :example:
        result = close_people_detector()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = face_detect_bridge(req_type=const.TYPE_STOP)
    return result


def get_faces_detected():
    """
    查询机器人人脸检测出的人脸信息
    :return:result
    :example:
        result = get_faces_detected()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                 {
                   'object_name':'person',
                   'probability':'1',
                   'width':123,
                   'height':223,
                   'top':12,
                   'left':33
                 },
                 {
                   'object_name':'person',
                   'probability':'1',
                   'width':53,
                   'height':63,
                   'top':122,
                   'left':133
                 },
                 ...
            ]
        }
    """
    result = face_detect_bridge(req_type=const.TYPE_QUERY)
    return result


if __name__ == '__main__':
    '''
    Python以模块运行方式启动入口
    '''
    # open_people_detector()
    close_face_detector()
    # get_faces_detected()
