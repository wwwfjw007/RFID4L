#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# 定义一个常量类实现常量的功能
#
# 该类定义了一个方法__setattr()__,和一个异常ConstError, ConstError类继承
# 自类TypeError. 通过调用类自带的字典__dict__, 判断定义的常量是否包含在字典
# 中。如果字典中包含此变量，将抛出异常，否则，给新创建的常量赋值。
# 最后两行代码的作用是把const类注册到sys.modules这个全局字典中。

"""
@File    : constant.py
@Time    : 2020/5/9 上午 11:31
@Author  : wgx
@Email   : heero@ust.hk
@Software: PyCharm
"""
import sys


class Const:
	class ConstError(TypeError):
		pass
	
	class ConstCaseError(ConstError):
		pass
	
	def __setattr__(self, name, value):
		if name in self.__dict__:
			raise self.ConstError("Can't rebind const (%s)" % name)
		if not name.isupper():
			raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
		self.__dict__[name] = value


sys.modules[__name__] = Const()
