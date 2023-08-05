"""
@project:medical_robot_backend
@language:python3
@create:2019/4/26
@author:qianyang@aibayes.com
@description:none
"""
import json
import tkinter.messagebox
from bayeslibs.config.setting import ApolloConfig
from tkinter import Tk
from urllib.request import Request, urlopen


class Http:
    REQUEST_COUNT = 1

    def __init__(self):
        pass

    @staticmethod
    def request_json(url, data=None):
        if not data:
            return None
        if ApolloConfig().get_apollo_network() == 'bad':
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            tkinter.messagebox.showerror('错误', '网络质量差，请重新配置网络')
            print('--------------------------------------------------')
            print('网络质量差，请重新配置网络')
            exit(0)
        data_rq = json.dumps(data).encode('utf-8')
        header = {'Content-Type': 'application/json'}
        req = Request(url, data_rq, header)
        try:
            f = urlopen(req, timeout=3)
            result_json = f.read().decode('utf-8')
            result_json = json.loads(result_json)
            f.close()
            Http.REQUEST_COUNT = 1
            return result_json
        except Exception as err:
            if Http.REQUEST_COUNT >= 3:
                root = Tk()
                root.withdraw()
                root.wm_attributes('-topmost', 1)
                tkinter.messagebox.showerror('错误', '请求超时，请检查初始化配置是否正确和网络信号是否良好')
                print('--------------------------------------------------')
                print('网络异常退出:{}，请检查你的网络配置是否正确，网络信号是否良好'.format(err))
                exit(0)
            else:
                Http.REQUEST_COUNT += 1
                print('Http.REQUEST_COUNT', Http.REQUEST_COUNT)
                return Http.request_json(url, data)


if __name__ == '__main__':
    pass
