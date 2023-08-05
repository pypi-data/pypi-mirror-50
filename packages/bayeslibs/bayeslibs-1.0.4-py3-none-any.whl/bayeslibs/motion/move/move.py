# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.mbridge import move_bridge
from bayeslibs.config import const, setting

apollo_config = setting.ApolloConfig()


class ApolloMover:
    def __init__(self):
        pass

    @staticmethod
    def go_forward(distance):
        try:
            robot_move_forward(distance)
            move_stat = get_robot_move_status()
            while move_stat and move_stat['status'] != 0:
                move_stat = get_robot_move_status()
            return True
        except Exception as err:
            print('ApolloMover go_forward error:{}'.format(err))
            return False

    @staticmethod
    def go_back(distance):
        try:
            robot_move_back(distance)
            move_stat = get_robot_move_status()
            while move_stat and move_stat['status'] != 0:
                move_stat = get_robot_move_status()
            return True
        except Exception as err:
            print('ApolloMover go_back error:{}'.format(err))
            return False

    @staticmethod
    def stop_move():
        return stop_robot_move()

    @staticmethod
    def status():
        return get_robot_move_status()


def robot_move_forward(distance):
    """
    控制机器人向前运动特定距离
    :param distance:运动距离
    :return:result
    :example:
        '''向前运动3m'''
        result = robot_move_forward(3)
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    if distance > apollo_config.get_max_dist():
        distance = apollo_config.get_max_dist()
    data = {
        'x': distance,
        'y': 0,
        'theta': 0
    }
    result = move_bridge(req_type=const.TYPE_START, data=data)
    return result


def robot_move_back(distance):
    """
    控制机器人向后运动特定距离
    :param distance:运动距离
    :return:result
    :example:
        '''向后运动3m'''
        result = robot_move_back(3)
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    if distance > apollo_config.get_max_dist():
        distance = apollo_config.get_max_dist()
    data = {
        'x': -distance,
        'y': 0,
        'theta': 0
    }
    result = move_bridge(req_type=const.TYPE_START, data=data)
    return result


def stop_robot_move():
    """
    停止机器人的运动
    :return:result
    :example:
        result = stop_robot_move()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = move_bridge(req_type=const.TYPE_STOP)
    return result


def get_robot_move_status():
    """
    查询机器人状态
    :return:result
    :example:
        result = get_robot_move_status()
        ------
        result:{
            'status':0,
            'msg':'robot is moving'
        }
    """
    result = move_bridge(req_type=const.TYPE_QUERY)
    return result


if __name__ == '__main__':
    print(robot_move_forward(0.4))
