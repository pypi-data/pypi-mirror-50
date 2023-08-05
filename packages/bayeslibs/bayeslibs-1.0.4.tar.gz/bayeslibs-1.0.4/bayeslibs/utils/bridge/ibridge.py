# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.config.setting import ApolloConfig
from bayeslibs.utils.comm.http import Http

APOLLO_CONFIG = ApolloConfig()


def object_detect_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/object_detect'), request_json)
    return res


def distance_detect_bridge(req_type, pos=None, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    if pos:
        request_json['pos'] = pos
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/distance_detect'), request_json)
    return res


def color_recog_bridge(req_type, colors='red', is_multi=False, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show,
        'is_multi': is_multi,
        'colors': colors
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/color_recog'), request_json)
    return res


def face_detect_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/face_detect'), request_json)
    return res


def face_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/face_recog'), request_json)
    return res


def age_gender_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/age_gender_recog'), request_json)
    return res


def emotion_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/emotion_recog'), request_json)
    return res


def headpose_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/headpose_recog'), request_json)
    return res


def beauty_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/beauty_recog'), request_json)
    return res


def handpose_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/handpose_recog'), request_json)
    return res


def skeleton_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/skeleton_recog'), request_json)
    return res
