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


def wts_bridge(req_type, text=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'text': text
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('voice/wts'), request_json)
    return res


def tts_bridge(req_type, text=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    if text:
        request_json['text'] = text
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('voice/tts'), request_json)
    return res


def asr_bridge(req_type):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('voice/asr'), request_json)
    return res


def acr_bridge(req_type):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('voice/acr'), request_json)
    return res


def chat_bridge(req_type, text=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    if text:
        request_json['text'] = text
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('voice/chat'), request_json)
    return res


def music_bridge(req_type, text=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    if text:
        request_json['text'] = text
    res = Http.request_json(APOLLO_CONFIG.get_robot_route_url('voice/music'), request_json)
    return res
