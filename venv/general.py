#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""
@File    : general.py
@Time    : 2020/5/9 上午 11:24
@Author  : wgx
@Email   : heero@ust.hk
@Software: PyCharm
"""
import socket
import time
import struct
import define
import json


def open_net_port(host, port):
	"""
	:definition: *打开网络接口*
	:return: socket
	"""
	sock = socket.socket()
	print(host, port)
	while True:
		try:
			sock.connect((host, port))
			break
		except socket.error as err:
			print(err)
			time.sleep(5)
	return sock


def close_net_port(sock):
	"""
	:definition: *关闭网络接口*
	:param sock: socket
	:return:
	"""
	sock.close()
	
	
def crc16(data, num, inverse):
	"""
	:definition: *CRC校验*
	:param data: 待校验数据
	:param num: 数据个数
	:param inverse: 输出是否反转，True:反转，False:不反转
	:return: crc校验值
	"""
	PRESETVALUE = 0xFFFF
	POLYNOMIAL = 0x8408
	crcValue = PRESETVALUE
	
	for i in range(num):
		crcValue ^= data[i]
		for j in range(8):
			if (crcValue & 0x0001) != 0:
				crcValue = (crcValue >> 1) ^ POLYNOMIAL
			else:
				crcValue = (crcValue >> 1)
	
	if inverse:
		crcLSB = crcValue & 0xFF
		crcMSB = (crcValue >> 8) & 0xFF
	else:
		crcLSB = (crcValue >> 8) & 0xFF
		crcMSB = crcValue & 0xFF
	
	return crcLSB, crcMSB
	
	
def set_work_mode(sock, para):
	"""
	:definition: *设置工作模式*
	:param sock: socket
	:param para: 设置参数
	:return:
	"""
	leng = 0x0a
	addr = 0xff
	comd = 0x35
	paralist = [leng, addr, comd] + para
	res, data = send_command(sock, paralist)
	
	if not res:
		return define.ERROR_CODE_OF_COMUICATION
	else:
		status = data[3]
	return status


def get_epc_num(info):
	"""
	:definition: *获取EPC标签号*
	:param info: 标签信息
	:return: EPC号
	"""
	epc_num = list()
	for i in range(define.EPC_NUM_BYTES):
		epc_num.append(info[i + 4])
	return epc_num
	
	
def send_command(sock, para):
	"""
	:definition: *发送指令*
	:param sock: socket
	:param para: 参数
	:return: 响应数据
	"""
	crcL, crcM = crc16(para, len(para), True)
	para.append(crcL)
	para.append(crcM)
	numBytes = len(para)
	cmd = struct.pack('B' * numBytes, *para)

	try:
		sock.send(cmd)
		try:
			recvData = sock.recv(1024)
		except socket.error as err:
			print(err)
			return False, None
	except socket.error as err:
		print(err)
		return False, None

	return True, recvData


def recv_data(sock):
	"""
	:definition: *主动模式下，读取读写器识别标签后的响应数据*
	:param sock: socket
	:return: 响应数据
	"""
	try:
		data = sock.recv(1024)
	except socket.error as err:
		print(err)
		return None
	return data


def pack_header(rfid_id, save_flag):
	"""
	:definition: *打包数据头*
	:param save_flag: 保存标识，True:保存，False:不保存
	:return: 数据头
	"""
	header = 'action:' + '/actualdata' + '\n'
	header = header + 'mac:' + rfid_id + '\n'
	if save_flag:
		header = header + 'Saved:' + 'true' + '\n'
	header = header + '\n'
	return header


def pack_data(rfid_dist, rfid_id, save_flag, tag_id, write_data):
	"""
	:definition: *打包数据包*
	:param rfid_dist: rfid区域
	:param rfid_id: rfid编号
	:param save_flag: 保存标识
	:param tag_id: 标签编号
	:param write_data: 数据
	:return: 数据包
	"""
	idNum = ''
	data = dict()
	
	for i in range(define.EPC_NUM_BYTES):
		hexnum = hex(tag_id[i])
		hexnum = hexnum[2:]
		idNum = idNum + hexnum.zfill(2)
	
	data['rfid_dist'] = rfid_dist
	data['rfid_id'] = rfid_id
	data['tag_id'] = idNum
	data['tag_info'] = write_data[0]
	
	header = pack_header(rfid_id, save_flag)
	json_data = json.dumps(data)
	total_data = header + json_data
	
	return total_data


def send_data(host, port, data):
	"""
	:definition: *上传数据*
	:param data: 数据包
	:return:
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			sock.connect((host, port))
			break
		except socket.error as err:
			print(err)
			time.sleep(3)

	while True:
		try:
			res = sock.send(data.encode())
			break
		except socket.error as err:
			print(err)
			time.sleep(3)
	sock.close()
	print('send data res =', res)
	print(data)
	print(sock)
	return res


def print_test(name, data):
	print('**********', name, '**********')
	for i in data:
		print(hex(i), ' ', end='')
	print('')
