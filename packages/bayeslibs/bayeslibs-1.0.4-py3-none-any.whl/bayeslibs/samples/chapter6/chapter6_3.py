# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
import time
from bayeslibs.motion import start_auto_nav, get_auto_nav_status, stop_auto_nav
from bayeslibs.config import add_slam_pos, get_slam_pos

DESTINATION_POS_MAP = {'p_hr': {'x': 6.861, 'y': 6.389}, 'p_el': {'x': -1.195, 'y': 7.257},
                       'p_origin': {'x': 0, 'y': 0}}

RUN_TIME = 60 * 10


def update_nav_pos():
    """
    更新室内导航地图位置信息
    :return: True
    """
    for item, pos in DESTINATION_POS_MAP.items():
        add_slam_pos(item, pos['x'], pos['y'])
    return True


def dest_valid(dest):
    if dest not in get_slam_pos():
        return False
    else:
        return True


def auto_nav_sample(dest):
    stat_res = start_auto_nav(dest)
    if stat_res and stat_res['status'] == 0:
        print('>>> 小贝自动导航功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        stat = get_auto_nav_status()
        print('------------------------------------')
        print('小贝导航中.......')
        # 300s如果还没有导航成功就取消导航
        while stat and stat['status'] != 0 and (cur_time - start_time).seconds <= RUN_TIME:
            stat = get_auto_nav_status()
            cur_time = datetime.datetime.now()
        if (cur_time - start_time).seconds > RUN_TIME:
            print('------------------------------------')
            print('小贝导航超时.......')
            res = stop_auto_nav()
            if res['status'] == 0:
                print('导航关闭成功')
                return False
        print('------------------------------------')
        print('小贝导航成功.......')
        print('------------------------------------')
        return True, 0
    else:
        print('网络故障，请检查网络状况是否良好')
        return False, 204


if __name__ == '__main__':
    # 更新室内导航地图位置信息
    update_nav_pos()
    # 导航地点为DESTINATION_POS_MAP里的地点，输入格式为p_hr,p_el,p_origin
    valid = False
    dest_list = list()
    while not valid:
        dest_es = input('请输入导航地点:')
        dest_list = dest_es.split(',')
        valid = True
        for dest_ in dest_list:
            if not dest_valid(dest_.strip()):
                print('导航地点输入有误，请重新输入')
                valid = False
                break
    for dest_ in dest_list:
        dest_ = dest_.strip()
        # 导航到地点
        auto_nav_sample(dest_)
        # 暂停2s，再次导航到下一地点
        time.sleep(2)
