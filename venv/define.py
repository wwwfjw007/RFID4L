#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# definition of constant variables

"""
@File    : define.py
@Time    : 2020/5/9 下午 2:29
@Author  : wgx
@Email   : heero@ust.hk
@Software: PyCharm
"""

ERROR_CODE_OF_COMUICATION = 0x30
EPC_NUM_BYTES = 12
"""
根据6个字节参数设定模式
byte0 : read_mode, 工作模式, 0x0 表示应答模式, 0x1 表示主动模式
byte1 : mode_state, 0x2 表示开蜂鸣器、rs232/rs485输出, 0x6 表示关蜂鸣器、rs232/rs485输出
byte2 : mem_inven, 读取区域, 0x1 表示EPC存储器, 0x3 表示用户存储器
byte3 : first_adr, 指定要读取的起始地址, 0x0 表示从第0个字开始读取, 0x2表示从第4个字开始读取
byte4 : word_num, 读取的字的个数
byte5 : tag_time, 主动模式下单张标签操作间隔时间(秒), 对同一张标签在间隔时间内只操作一次
"""
IDENTICAL_INTERVAL = 0x3

PARA_ACTIVE_MODE_EPC_MEM = [0x1, 0x6, 0x1, 0x2, 0x6, IDENTICAL_INTERVAL]  # 主动模式的6个字节参数
PARA_ANSWER_MODE_USER_MEM = [0x0, 0x6, 0x3, 0x0, 0x0, IDENTICAL_INTERVAL]  # 应答模式的6个字节参数


class DistrictInfo:
	"""
	
	"""
	def __init__(self):
		self.init = 0
		self.inner = 1
		self.outer = 2
