#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""
@File    : rfid_v2.py
@Time    : 2020/5/9 下午 3:38
@Author  : wgx
@Email   : heero@ust.hk
@Software: PyCharm
"""
import threading
import EPC_C1G2
from general import *
from define import *


def get_rfid_info():
	"""
	:definition: 从json配置文件获取RFID信息
	:return: 返回所有RFID的id, ip, port
	"""
	f = open('rfid_info.json', encoding='utf-8')
	rfid_json = json.load(f)
	return rfid_json


def get_server_info():
	"""
	:definition: 从json配置文件获取服务器信息
	:return: 返回服务器ip, port
	"""
	f = open('server_info.json', encoding='utf-8')
	server_json = json.load(f)
	return server_json


def rfid_start(rfid):
	"""
	:definition: 初始化所有rfid设备，使用网络接口通信
	:param rfid: rfid设备信息
	:return: 返回已成功连接的socket
	"""
	msg = dict()
	for i in rfid:
		dist = rfid[i]
		msg[i] = dict()
		for j in dist:
			ip = dist[j]['ip']
			port = dist[j]['port']
			msg[i]['ID'] = j
			msg[i]['sock'] = open_net_port(ip, port)
	return msg


def rfid_work_thread(msg, dist, server):
	sock = msg['sock']
	rfid_ID = msg['ID']
	server_host = server['ip']
	server_port = server['port']
	epc = EPC_C1G2.EPC()
	
	# 设置为主动模式
	status_active_epc = set_work_mode(sock, PARA_ACTIVE_MODE_EPC_MEM)
	print('status_active_epc = 0x%x' % status_active_epc)
	time.sleep(0.05)
	
	last_active_data = dict()
	district = DistrictInfo()
	
	while True:
		try:
			active_data = recv_data(sock)
			if active_data not in last_active_data.keys():
				print_test('active data', active_data)
				print('not exist')
				last_active_data[active_data] = time.time()
			else:
				print('exist')
				current_time = time.time()
				print(current_time - last_active_data[active_data])
				# 判断时间间隔
				if current_time - last_active_data[active_data] <= IDENTICAL_INTERVAL:
					print('continue')
					continue
				else:
					last_active_data[active_data] = time.time()
					print('new active data')
		except socket.error as err:
			print(err)
			break
			
		if active_data is not None:
			# 设置为应答模式
			status_answer_user = set_work_mode(sock, PARA_ANSWER_MODE_USER_MEM)
			print('status_answer_user = 0x%x' % status_answer_user)
			time.sleep(0.05)
			
			# 读取标签卡数据
			status_read_data, card_data, card_data_len = epc.read_data(sock, active_data)
			print('********************** card data = ', card_data)
			if status_read_data == 0:
				write_data = list(card_data)
				if card_data[0] == district.inner or card_data[0] == district.init:
					write_data[0] = district.outer
				elif card_data[0] == district.outer:
					write_data[0] = district.inner
				else:
					write_data[0] = district.init
				print('********************** write data = ', write_data)
				
				# 写数据进入标签卡
				status_write_data = epc.write_data(sock, active_data, write_data, card_data_len)
				print('status write data = 0x%x' % status_write_data)
				if status_write_data == 0:
					upload_data = pack_data(dist, rfid_ID, True, get_epc_num(active_data), write_data)
					# print('upload data = \n%s' % upload_data)
					print(server_host, server_port)
					send_data(server_host, server_port, upload_data)
			
			# 重新设置为主动模式
			status_active_epc = set_work_mode(sock, PARA_ACTIVE_MODE_EPC_MEM)
			print('status_active_epc = 0x%x' % status_active_epc)
			time.sleep(0.05)
	
	rfid_stop(sock)


def rfid_work(msg):
	server = get_server_info()
	for i in msg:
		threading.Thread(target=rfid_work_thread, args=(msg[i], i, server)).start()
	return


def rfid_stop(sock):
	"""
	:definition: 停止所有rfid设备，关闭网络接口
	:param sock: 所有rfid设备的socket
	:return:
	"""
	close_net_port(sock)
	sock.clear()


def run():
	"""
	
	:return:
	"""
	all_rfid = get_rfid_info()
	all_rfid_msg = rfid_start(all_rfid)
	print(all_rfid_msg)
	rfid_work(all_rfid_msg)
	

if __name__ == '__main__':
	run()
