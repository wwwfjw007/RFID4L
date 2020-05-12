#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""
@File    : EPC_C1G2.py
@Time    : 2020/5/9 下午 5:52
@Author  : wgx
@Email   : heero@ust.hk
@Software: PyCharm
"""
from general import send_command
from general import get_epc_num
from define import ERROR_CODE_OF_COMUICATION
from define import EPC_NUM_BYTES


class EPC:
	"""
	epc标签读写接口
	"""
	def __init__(self):
		self.EPC_NUM_WORDS = EPC_NUM_BYTES // 2  # EPC号字长度，1个字=2个字节
		self.passwd = [0, 0, 0, 0]
	
	def read_data(self, sock, info):
		"""
		:definition: *读取标签数据*
		:param sock: socket
		:param info: 标签信息
		:return: 结果状态，EPC数据，数据长度
		"""
		addr = 0xff
		cmd = 0x02
		epc = get_epc_num(info)
		e_num = self.EPC_NUM_WORDS
		mem = 0x03
		word_ptr = 0x00
		num = 0x01
		mask_addr = 0x0
		mask_len = 0x0
		
		data = [e_num] + epc + [mem, word_ptr, num] + self.passwd + [mask_addr, mask_len]
		leng = len(data) + 4
		para_list = [leng, addr, cmd] + data  # 完整命令格式
		res, data = send_command(sock, para_list)
		epc_data_len = data[0] - 5
		epc_data = data[4:(4 + epc_data_len)]
		
		if not res:
			return ERROR_CODE_OF_COMUICATION
		else:
			status = data[3]
		return status, epc_data, epc_data_len
	
	def write_data(self, sock, info, wdata, write_data_len):
		"""
		:definition: *写入信息到标签*
		:param sock: socket
		:param info: 标签信息
		:param wdata: 写入信息
		:param write_data_len: 写入信息长度
		:return: 结果状态
		"""
		
		addr = 0xff
		cmd = 0x03
		EPC = get_epc_num(info)
		ENum = self.EPC_NUM_WORDS
		mem = 0x03
		word_ptr = 0x0
		mask_addr = 0x0
		mask_len = 0x0
		
		data = [write_data_len, ENum] + EPC + [mem, word_ptr] + wdata + self.passwd + [mask_addr, mask_len]
		leng = len(data) + 4
		para_list = [leng, addr, cmd] + data
		res, data = send_command(sock, para_list)
		
		if not res:
			return ERROR_CODE_OF_COMUICATION
		else:
			status = data[3]
		return status