# -*- coding: utf-8 -*-  


import numpy as np  # pip install numpy

import scipy
from scipy.optimize import leastsq

import datetime

from autoleastsq.data2list_sqlite3 import * 
from autoleastsq.showmodel import *


########################   本脚本使用 scipy 最小二乘法拟合  -规整次幂方法 

"""
评价：
1  速度较高
2  准确

改进效果：
1  自动适应因子数量  
2  根据精准度要求，自动匹配最合适的幂次; 也可以设定起始拟合幂次


"""

# 自定义异常  抛出建议的容错值和幂次
class leastsq_Exception(Exception):
	def __init__(self, sugguest_loss, suggest_power):
		self.sugguest_loss = sugguest_loss
		self.suggest_power = suggest_power



class leastsq_mult(): 

	args=None		# 多项式的参数列表
	var_num=None	# 因子、变量个数
	pows=None		# 多项式 幂次
	func=None		## 显示模型所代表的多项式 


	# 这里次幂定义可以是规整的整数, 准确率也还算可以

	## 根据参数数量和次幂，动态生成公式模型用于拟合
	def __make_func_str(self,var_num, pow_num):   # 参数数量，最高次幂

		"""
		# 例如 2元3次   注意是局部变量
		# pow(x[0],3)*a1 + pow(x[0],2)*a2 + x[0]*a3 + pow(x[1],3)*a4 + pow(x[1],2)*a5 + x[1]*a6 + a7
		# pow(x[0],3)*loc['a1'] + pow(x[0],2)*loc['a2'] + x[0]*loc['a3'] + pow(x[1],3)*loc['a4'] + pow(x[1],2)*loc['a5'] + x[1]*loc['a6'] + loc['a7']

		这样可以适应  loc = locals()  后  exec 动态的参数数量变化

		"""

		a_num=1
		func_str=""

		for i in range(var_num):  # 参数

			for ii in range(pow_num,0,-1):  # 次幂

				temp="pow(x[" + str(i) + "]," + str(ii) + ")*loc['a" + str(a_num) + "']"   

				func_str= func_str + temp+ " + "

				a_num=a_num+1

		func_str = func_str + "loc['a" + str(a_num) + "']"  

		#print(func_str)

		return func_str


	#动态生成变量名字符串  'a1,a2,a3,xxxx'
	def __make_args_name(self,arg_num):

		arg_str=""
		for i in range(arg_num):
			arg_str=arg_str+ "a" + str(i+1) 

			if i!=arg_num-1:
				arg_str=arg_str+","


		return arg_str


	######################################## scipy.optimize   leastsq 	

	# 标准拟合多项式公式模型动态生成
	def __func_leastsq(self,x, p, pows):

		########## 动态产生参数名

		## 注意局部使用动态 exec 的方法, 函数中默认赋值是存入局部变量的，需要再提取出来, 直接赋值无效
		loc = locals()

		# 动态生成变量名串 'a1,a2,xxxxx'
		arg_str=self.__make_args_name(len(x)*pows+1)  # 数量：变量数量*次幂数量+1

		"""
		#a, b, c, d , e, f, g=p
		#exec('a1, a2, a3, a4 , a5, a6, a7=p') 
		"""
		exec(arg_str+"=p")  ##  这样就可动态产生多项式需要的参数了，使用时使用  loc['a1']


		########## 动态产生公式并返回

		arg_num=len(x)
		ret_func=self.__make_func_str(arg_num, pows)  ## 得到具体公式写法

		"""
		#return pow(x[0],3)*a + pow(x[0],2)*b + x[0]*c + pow(x[1],3)*d + pow(x[1],2)*e + f*x[1] + g
		#return pow(x[0],3)*loc['a1'] + pow(x[0],2)*loc['a2'] + x[0]*loc['a3'] + pow(x[1],3)*loc['a4'] + pow(x[1],2)*loc['a5'] + x[1]*loc['a6'] + loc['a7']
		"""
		return eval(ret_func)


	def __error(self,p,x,y,s,pows):

	    return self.__func_leastsq(x, p, pows)-y      #x、y都是列表，故返回值也是个列表


	 #### 入口函数    x 二维列表 y 一维列表 , 	 pows_start 起始拟合的幂次(默认为1), loss_min 误差率要求（达到即拟合结束）
	def __init__(self,x,y,pows_start=1,loss_min=0.01):

		print("Start!")  
		timestart = datetime.datetime.now()	  ## 用于统计效率

		######## 进行拟合  逐渐增高幂次，直到达到准确率要求

		pows=pows_start

		# 非零化处理 如果为零就等于最低准确率
		for i in range(len(y)):
			if y[i]==0:
				y[i]=loss_min


		###### 幂次增加进行拟合

		loss_min_now=loss_min

		while True:

			print("loss_min:",loss_min_now)

			try:
				self.__power_add(x,y,pows,loss_min_now)
				break
			except leastsq_Exception as e:
				print("Suggest Loss_min:",e.sugguest_loss, "Possible Power:",e.suggest_power)

				## 如果指定误差内拟合失败，就自动放大误差率

				adds=min([e.sugguest_loss/10,loss_min])
				loss_min_now=e.sugguest_loss + adds 

		#######

		timeend = datetime.datetime.now()
		rettime=str(round((timeend-timestart).total_seconds(),2))
		print("Use:",rettime,"s")


	#幂次递增
	def __power_add(self,x,y,pows,loss_min):

		loss_list=[]
	
		while True:

			nums=len(x) * pows +1  # 参数数量

			# 参数的初始值，影响拟合效率
			p0=np.ones(nums).tolist()

			x = scipy.array(x)
			y = scipy.array(y)

			s="leastsq"

			Para=leastsq(self.__error, p0, args=(x,y,s,pows))   #把error函数中除了p以外的参数打包到args中


			####### 得到拟合后错误率

			loss=self.__loss_get(Para[0],pows,x.T.tolist(),y.tolist())

			loss_list.append(loss)

			print("pow:",pows," loss:",loss)  # 建议输出供观察

			### 误差率出现上升，就停止拟合，并记录误差率 
			if loss>min(loss_list):
				raise leastsq_Exception(min(loss_list),pows-1) 
		
			if loss<loss_min:

				print("Complete!")

				break

			### 升高幂次 继续循环  

			pows=pows+1


		#######

		self.args=Para[0]   # 多项式的参数列表
		self.var_num=len(x)		# 变量数量
		self.pows=pows  	# 多项式 幂次
		self.func=model_str(self.args,self.pows)   ## 显示模型所代表的多项式

		

	#公式的样本损失率计算		factor_list 为二元list, 一级每个对应一个 result值
	def __loss_get(self,args,pows,factor_list,result_list):

		# 因子数
		var_num=len(factor_list[0])

		## 每个因子逐个代入求损失率

		loss=0
		for i in range(len(factor_list)):

			factor=factor_list[i]

			self.args=args
			self.var_num=var_num
			self.pows=pows

			result=self.leastsq_result(factor)

			the_loss=abs(abs(result-result_list[i])/result_list[i])

			loss=loss+the_loss

		loss=loss/len(factor_list)

		return loss



	######################################## 根据拟合后的多项式求值

	# 测试值列表（按当时拟合时的次序）

	def leastsq_result(self,x):

		if self.var_num!=len(x):
			print("Error: Model factor size ", self.var_num," but ", len(x))
			return None
		if type(x)!=type([0]):
			print("Error: factor not list") 
			return None				

		###########

		args=self.args
		var_num=self.var_num
		pows=self.pows

		########## 动态产生公式并返回

		ret_func=self.__make_func_str(var_num, pows)  ## 得到具体公式写法

		# 替换指定参数

		for i in range(len(args)):

			ret_func=ret_func.replace("loc['a" + str(i+1) + "']" , str(args[i])) 

		#print(ret_func)

		########## 动态执行多项式

		## 注意局部使用动态 exec 的方法, 函数中默认赋值是存入局部变量的，需要再提取出来, 直接赋值无效
		loc = locals()

		exec("ret=" + ret_func)  ##  这样就可动态产生多项式需要的参数了，使用时使用  loc['ret']	

		ret=loc['ret']

		return(ret)



##############################################
##############################################  使用


if __name__ == "__main__":

	### 获取数据到 list

	filename="./test.xlsx"
	lists=excel_col2list(filename,["a","b","result"])


	################# 多元多项式回归样例

	# 挑选所需要的因子  注意append 因子次序决定了拟合的公式，和后续使用时的入口次序, append 几个因子多项式就有几元，可灵活使用

	factor=[]  # factor自由多个因子的二维list
	factor.append(lists[0])
	factor.append(lists[1])
	y = lists[2]

	##################### 拟合得到多项式模型

	# 返回：多项式的参数列表、 幂次，并可根据新输入的因子list 进行预测

	"""
	支持的参数：
	pows_start=1	# pows_start 起始拟合的幂次(默认为1)
	loss_min=0.01		# loss 起始误差率要求（默认0.01, 达到即拟合结束）, 过程中会自动判断最可能的误差率
	leastsq_mult(factor,y,pows_start,loss_min)
	"""

	model=leastsq_mult(factor,y)

	print(model.args,model.pows)  ## 最终的多项式参数 按高次向低次逐个因子排列 ; 最终的多项式参数最高幂次
	print(model.func)  ##  模型公式

	################# 根据拟合后结果多项式，按顺序输入得到结果

	factor=[29,101]

	result=model.leastsq_result(factor)

	print(result)





