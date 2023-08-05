# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import age_gender_recog_bridge
from bayeslibs.config import const


class ApolloAgeGenderRecognizer:
    """
    年龄性别识别模块封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def open(is_show=True):
        return open_age_gender_recognizer(is_show)

    @staticmethod
    def close():
        return close_age_gender_recognizer()

    @staticmethod
    def age_genders():
        return get_age_genders_recognized()


def open_age_gender_recognizer(is_show=True):
    """
    开启机器人年龄性别识别功能
    :param
    :return:result
    :example:
        result = open_age_gender_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = age_gender_recog_bridge(req_type=const.TYPE_START, is_show=is_show)
    return result


def close_age_gender_recognizer():
    """
    关闭机器人年龄性别识别功能
    :param
    :return:result
    :example:
        result = close_age_gender_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = age_gender_recog_bridge(req_type=const.TYPE_STOP)
    return result


def get_age_genders_recognized():
    """
    查询机器人识别出的年龄性别信息
    :return:result
    :example:
        result = get_age_genders_recognized()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                 {
                    'gender':'male',
                    'gender_confidence':0.98,
                    'age': 27,
                    'width':123,
                    'height':223,
                    'top':12,
                    'left':33
                 },
                 ...
            ]
        }
    """
    result = age_gender_recog_bridge(req_type=const.TYPE_QUERY)
    return result
