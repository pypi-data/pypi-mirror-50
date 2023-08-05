# -*- coding: utf-8 -*-  


############# 本文件用于excel 数据提取并转为 list  使用自带的 sqlite3 ,  只支持  python3 , 只取 Sheet1 名的 Sheet



import sys,os

import sqlite3  # 不需要单独安装

import datetime,time

import xlrd  # pip install -U xlrd
import csv

import platform

import numpy as np


from io import open


########################## excel 数据到 list

"""

excel 要求格式：
列名1	列名2   xxxx 
数据		数据		数据


colname_list 可以是一个动态的列名 list ， 返回时时是按对应顺序返回 一个二维 list 

filename="./test.xlsx"
lists=excel_col2list(filename,["a","b","result"])

lists[0] 对应表头为 a 的数据


"""

def excel_col2list(filename,colname_list):   


	sql=""
	sql_null=""

	for i in range(len(colname_list)):

		sql=sql+colname_list[i]
		sql_null=sql_null+  "length(" +   colname_list[i]  + ")>0"

		if i<len(colname_list)-1:
			sql=sql+","
			sql_null=sql_null+" and "

	#sql="select " + sql + " from excel"
	sql="select " + sql + " from excel where " + sql_null  # 不为不完整或空行   （sqlite 没有  ISNUMERIC） 

	ret_list=excelsql_sqlite_xls(filename,sql,outputfilename="temp.csv")   ## 临时文件

	## 基础数据过滤  例如非数字
	ret_list=due_list(ret_list)

	## x y 转置 供处理
	ret_list=xtoy_list(ret_list)


	## 转为数字 供运算
	ret_list=str2num(ret_list)

	return ret_list


###############   二维list 的 xy 转置

def xtoy_list(the_lists):

	#转换为矩阵

	x=[]
	for i in range(len(the_lists)):
		x.append(the_lists[i])

	m = np.array(x).T   ## .T 是xy转换

	xtoy_list=m.tolist()
	return xtoy_list 


###############  数据基础过滤

def due_list(the_lists):

	## 是否全部为数字

	ret=[]

	for i in range(len(the_lists)):

		isNum=True
		for w in range(len(the_lists[i])):
			if the_lists[i][w].replace(".","").isdigit()==False:
				isNum=False
				break

		if isNum==True:
			ret.append(the_lists[i])


	return ret


###############   二维list全部转为 整型 用于运算 (sqlite3查询全部为字符串)

def str2num(the_lists):

	for i in range(len(the_lists)):

		for ii in range(len(the_lists[i])):

			the_lists[i][ii]=float(the_lists[i][ii])


	return the_lists


###################################################


### xls xlsx 转为 csv

def csv_from_excel(filename,outputfilename):


	### 删除之前的文件
	if os.path.exists(outputfilename):
		os.remove(outputfilename)

	wb = xlrd.open_workbook(filename)
	sh = wb.sheet_by_name('Sheet1')

	csv_file = open(outputfilename, 'w', encoding='utf-8', newline='')  
	wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

	for rownum in range(sh.nrows):

		writes=sh.row_values(rownum)		
		wr.writerow(writes)



	csv_file.close()


### 从xls查询

def excelsql_sqlite_xls(filename,sql,outputfilename="temp.csv"):  # 临时文件

	csv_from_excel(filename,outputfilename)

	ret=excelsql_sqlite_csv(outputfilename,sql)

	return ret


### 从csv 导入后查询

def excelsql_sqlite_csv(filename,sql):

	sqlitedb="data.db"


	### 删除之前的库
	if os.path.exists(sqlitedb):
		os.remove(sqlitedb)

	### 从文件导入  到表 excel   注意分隔符,  data.db 中已经包含 excel 表名的表

	"""
	sysstr = platform.system()   ### 判断操作系统类型

	if sysstr == "Linux":  # 需要手动安装

		cmd="sqlite3 " + sqlitedb + " \".separator ','\" \".import " + filename + " excel\""

	if sysstr == "Windows":  # 自带
	
		cmd="sqlite3.exe " + sqlitedb + " \".separator ','\" \".import " + filename + " excel\""
	"""

	cmd="sqlite3 " + sqlitedb + " \".separator ','\" \".import " + filename + " excel\""

	try:
		os.system(cmd) 
	except:
		print("没有安装 sqlite3 或版本可能较低 <3.18  不能自动创建表，不能直接支持命令行")
		exit(0)

	conn = sqlite3.connect('data.db')
	cur = conn.cursor()

	# 查看表名 PRAGMA table_info([excel])

	ret=cur.execute(sql).fetchall() 


	return ret


##############################################  使用


if __name__ == "__main__":

	### 获取数据到 list

	filename=r"./test.xlsx"
	lists=excel_col2list(filename,["a","b","reg_3"])

	print(lists[0])

	
