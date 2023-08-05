# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import tkinter.messagebox
import subprocess
import re
from tkinter import Tk


class BayesLibsConfig:
    def __init__(self, ip, port, user_id=None, password=None):
        self.ip = ip
        self.port = port
        self.network = None
        self.user_id = user_id
        self.password = password

    def ping_test(self):
        p_intranet = subprocess.Popen(["ping", self.ip, '-n', '5'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      shell=True)
        outernet_ip = 'aip.baidubce.com'
        p_outernet = subprocess.Popen(["ping", outernet_ip, '-n', '5'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      shell=True)
        out_intranet = p_intranet.stdout.read().decode('gbk')
        out_outernet = p_outernet.stdout.read().decode('gbk')
        if 'Reply' in out_intranet:
            regex_delay = re.compile("Average = (\d+)ms", re.IGNORECASE)
            regex_loss = re.compile("(\d+)% loss", re.IGNORECASE)
        else:
            regex_delay = re.compile("平均 = (\d+)ms", re.IGNORECASE)
            regex_loss = re.compile("(\d+)% 丢失", re.IGNORECASE)
        delay_intranet_list = regex_delay.findall(out_intranet)
        if not delay_intranet_list:
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            tkinter.messagebox.showerror('警告', '无法连接内网，请检查设备是否在同一局域网')
            self.network = 'bad'
            return
        loss_intranet_list = regex_loss.findall(out_intranet)
        delay_outernet_list = regex_delay.findall(out_outernet)
        loss_outernet_list = regex_loss.findall(out_outernet)
        if not delay_outernet_list:
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            tkinter.messagebox.showerror('错误', '无法连接外网，请检查本机网络环境')
            self.network = 'bad'
            return
        delay_intranet = int(delay_intranet_list[0])
        loss_intranet = int(loss_intranet_list[0])
        delay_outernet = int(delay_outernet_list[0])
        loss_outernet = int(loss_outernet_list[0])
        if delay_intranet > 100 or loss_intranet > 5 or delay_outernet > 100 or loss_outernet > 5:
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            tkinter.messagebox.showerror('错误', '检测到网络信号差，请调整网络至Bayes网络标准')
            self.network = 'bad'
            return
        else:
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            tkinter.messagebox.showinfo('提示', '网络信号达到Bayes网络标准')
            self.network = 'good'
            return

    def connect(self):
        from bayeslibs.voice.chat.small_talk import ApolloChatter
        from bayeslibs.config.setting import ApolloConfig
        apollo = ApolloConfig()
        self.ping_test()
        apollo.set_apollo_url(self.ip, self.port, self.network)
        chatter = ApolloChatter()
        res = chatter.start('连接成功')
        if res and res['status'] == 0:
            flag = True
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            tkinter.messagebox.showinfo('提示', '连接成功')
            print('connect success, apollo ip:{}'.format(apollo.get_apollo_url()))
        else:
            flag = False
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            tkinter.messagebox.showwarning('提示', '无法连接，请检查是否完成初始化配置')
            print('connect failed, please reset apollo\'s ip')
        return flag


def add_slam_pos(dest, x, y):
    """
        设置室内导航目标地点的坐标位置
        :param dest: 目标地点描述，英文
        :param x: RVIZ点x坐标
        :param y: RVIZ点y坐标
        :return:
    """
    from bayeslibs.config.setting import ApolloConfig
    apollo = ApolloConfig()
    apollo.set_nav_pos(dest, x, y)


def get_slam_pos():
    from bayeslibs.config.setting import ApolloConfig
    apollo = ApolloConfig()
    return apollo.get_nav_pos_map()


__all__ = ['BayesLibsConfig', 'add_slam_pos', 'get_slam_pos']
