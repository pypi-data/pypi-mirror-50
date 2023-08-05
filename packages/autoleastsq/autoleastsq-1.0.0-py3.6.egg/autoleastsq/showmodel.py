# -*- coding: utf-8 -*-  


############# 显示模型所代表的的公式

"""
入参:  高次到低次、逐个变量排列的系数，幂次数,  系数的小数精度（默认4）, 归一化参数

"""


def model_str(arg_lists, pows, decimals=4, normal_taglist=None,normal_taglist_result=None):


	##### 根据幂次和变量个数生成脚本公式

	strs=""
	now=0

	arg_num= int( (len(arg_lists)-1)/pows ) # 变量个数

	for i in range(arg_num):

		for ii in range(pows,0,-1):

			if round (arg_lists[now],decimals)!=0:  ## 参数不为0

				if ii==1:	## 幂次为1
					strs=strs+ "x" + str(i+1)  + " *" + str( round (arg_lists[now],decimals) )   
				else:
					strs=strs+ "x" + str(i+1)  + "^" + str(ii) + " *" + str( round (arg_lists[now],decimals) ) 


				if ii>0:
					strs=strs+ " + "

			now=now+1



	strs=strs + str( round (arg_lists[now],decimals) )


	##### 涉及归一化的变形  这里使用了统一的  [-3,3] 区间的归一化

	if normal_taglist is not None:

		for i in range(arg_num):

			mx,mn=normal_taglist[i]

			replace_str="((((x" + str(i+1) + "-" + str(mn) + ")/"+ str(mx-mn) + ")-0.5)*6)"

			strs=strs.replace("x"+str(i+1), replace_str)

	if normal_taglist_result is not None:

		mx,mn=normal_taglist_result[0]

		strs="(" +  strs + ") /6 +0.5" 

		strs="(" +  strs + ") * "  +  str(float(mx-mn))  + " + " + str(mn)


	#######

	strs="y= " +strs


	return strs

