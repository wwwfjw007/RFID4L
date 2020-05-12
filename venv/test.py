#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""
@File    : test.py
@Time    : 2020/5/9 上午 11:47
@Author  : wgx
@Email   : heero@ust.hk
@Software: PyCharm
"""
from general import *
import threading
import time
from define import *


# sock = open_net_port('192.168.19.24', 6000)
# print(sock)
# close_net_port(sock)
# print(sock)


def thread_func(para):
	test_para = para
	while True:
		print(test_para)
		test_para += 1
		time.sleep(3)


def pack_data():
	header = 'action' + '\n'
	header = header + 'mac' + '\n'
	print(header)


def run():
	# threading.Thread(target=thread_func, args=(10, )).start()
	# threading.Thread(target=thread_func, args=(1000, )).start()
	dist = DistrictInfo()
	print(dist.init, dist.inner, dist.outer)
	pack_data()


if __name__ == '__main__':
	run()
