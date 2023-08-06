#_*_ coding:UTF-8 _*_
from __future__ import division	#导入 __future__ 文件的 division 功能函数(模块、变量名....)   #新的板库函数
import Adafruit_PCA9685 #导入Adafruit_PCA9685模块
import requests
import json
import sys
import time
import threading
import os
from aip import AipSpeech
import RPi.GPIO as GPIO
from pirc522 import RFID
import subprocess

GPIO.setmode(GPIO.BOARD)
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


class Servo:

	def __init__(self,channal,angle=90):
		self.channal = channal;
		self.angle = angle;
		self.set(self,angle)

	def set(self,angle):  # 输入角度转换成12^精度的数值
		date = int(4096 * ((angle * 11) + 500) / (20000) + 0.5)  # 进行四舍五入运算 date=int(4096*((angle*11)+500)/(20000)+0.5)
		pwm.set_pwm(self.channal, 0, date)


class RGB_LED:
	def __init__(self,pin_r,pin_g,pin_b,color='c'):
		self.pin_r = pin_r
		self.pin_g = pin_g
		self.pin_b = pin_b
		GPIO.setup(pin_r,GPIO.OUT)
		GPIO.setup(pin_g,GPIO.OUT)
		GPIO.setup(pin_b,GPIO.OUT)
		self.set(color)


	def set(self,color):
		if color == 'red' or color == 'r':
			GPIO.output(self.pin_r,GPIO.LOW)
			GPIO.output(self.pin_g,GPIO.HIGH)
			GPIO.output(self.pin_b,GPIO.HIGH)
		elif color == 'green' or color == 'g':
			GPIO.output(self.pin_r,GPIO.HIGH)
			GPIO.output(self.pin_g,GPIO.LOW)
			GPIO.output(self.pin_b,GPIO.HIGH)
		elif color == 'blue' or color == 'b':
			GPIO.output(self.pin_r,GPIO.HIGH)
			GPIO.output(self.pin_g,GPIO.HIGH)
			GPIO.output(self.pin_b,GPIO.LOW)
		elif color == 'white' or color == 'w':
			GPIO.output(self.pin_r,GPIO.LOW)
			GPIO.output(self.pin_g,GPIO.LOW)
			GPIO.output(self.pin_b,GPIO.LOW)
		elif color == 'purple' or color == 'p':
			GPIO.output(self.pin_r,GPIO.LOW)
			GPIO.output(self.pin_g,GPIO.HIGH)
			GPIO.output(self.pin_b,GPIO.LOW)
		elif color == 'yellow' or color == 'y':
			GPIO.output(self.pin_r,GPIO.LOW)
			GPIO.output(self.pin_g,GPIO.LOW)
			GPIO.output(self.pin_b,GPIO.HIGH)
		elif color == 'aquamarine' or color == 'a':
			GPIO.output(self.pin_r,GPIO.HIGH)
			GPIO.output(self.pin_g,GPIO.LOW)
			GPIO.output(self.pin_b,GPIO.LOW)
		else:
			GPIO.output(self.pin_r,GPIO.HIGH)
			GPIO.output(self.pin_g,GPIO.HIGH)
			GPIO.output(self.pin_b,GPIO.HIGH)
	def close(self):
		GPIO.output(self.pin_r,GPIO.HIGH)
		GPIO.output(self.pin_g,GPIO.HIGH)
		GPIO.output(self.pin_b,GPIO.HIGH)


class CardReader:
	__uid = [0,0,0,0,0,]
	__flag = 0
	__score = 0
	data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
	rdr = RFID()


	def __init__(self):
		RFID_timer = threading.Timer(0.1,self._callback)
		RFID_timer.start()


	def get_score(self):
		return self.__score


	def write(self,__score):
		self.__score = __score
		for i in range(15):
			self.data[i] = int(__score & 0xff)
			__score = __score >> 8
		# ~ print(self.data)
		self.__flag = 2


	def get_uid(self):
		return self.__uid


	def get_status(self):
		return self.__flag


	def _transfer(self,data):
		S = 0
		for i in range(15):
			S += data[i]*256**i
		return S


	def _callback(self):
		# ~ print('Finding')
		if not self.__flag == 2:
			self.__flag = 0
		self.rdr.wait_for_tag()
		(error, tag_type) = self.rdr.request()
		if not error:
			# ~ print("Tag detected")
			if not self.__flag == 2:
				self.__flag = 1
			(error, self.__uid) = self.rdr.anticoll()
			if not error:
			# ~ print("__uid: " + str(self.__uid))
			# Select Tag is required before Auth
				if not self.rdr.select_tag(self.__uid):
					if not self.rdr.card_auth(self.rdr.auth_a, 8, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], self.__uid):
						# This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
						if self.__flag == 1:
							error,self.data = self.rdr.read(8)
							if not error:
								self.__score = self._transfer(self.data)
								# print('Read:'+str(self.data))
								# print('Read Score:'+str(self.__score))
						elif self.__flag == 2:
							self.rdr.write(8,self.data)
							# ~ print('Write:'+str(self.data))
							# ~ print('Write Score:'+str(self.__score))
							self.__flag = 1
						self.rdr.stop_crypto()# Always stop crypto1 when done working			
		else:
			# ~ print('RFID Remove')
			self.__flag = 0
			self.__score = 0
		RFID_timer = threading.Timer(0.1,self._callback)
		RFID_timer.start()


class BaiduSpeech:	

	def __init__(self,APP_ID,API_KEY,SECRET_KEY):
		self.__client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


	# 读取文件
	def __get_file_content(self,filePath):   #filePath  待读取文件名
		with open(filePath, 'rb') as fp:
			return fp.read()


	def stt(self,filename): # 语音识别
		# 识别本地文件
		result = self.__client.asr(self.__get_file_content(filename),'wav',16000,{'dev_pid': 1536,})  # dev_pid参数表示识别的语言类型 1536表示普通话
		# ~ print(result)
		# 解析返回值，打印语音识别的结果
		if result['err_msg']=='success.':
			word = result['result'][0]
			if word!='':
				print(word)
				return word
			else:
				# ~ print("音频文件不存在或格式错误")
				return None
		else:
			# ~ print('错误')
			return None


	# 将文本进行语音合成
	def tts(self,words,file_name='audio.mp3'):
		if len(words) != 0:
			print(words)
			result  = self.__client.synthesis(words,'zh',1, {'vol': 6,'per':4, 'pit':6,})
		# 合成正确返回audio.mp3，错误则返回dict 
		if not isinstance(result, dict):
			with open('%s'%file_name, 'wb') as f:
				f.write(result)
			f.close()
			# print ('tts successful')
			return file_name


class QiQi:
	# ~ http://www.emotibot.com/
	__key = "488b046dd31262f22244aa4c5a97b631"
	__url = "http://idc.emotibot.com/api/ApiKey/openapi.php"
	__userid ='0EE4B632A2C4FA33803D65BA81E8776D9'


	def __init__(self):
		payload = {"cmd" : "register","appid" : self.__key}
		r = requests.post(self.__url, data=payload)
		if r:
		# ~ print(r.content)
			date = json.loads(r.content)
			# ~ print(date["data"][0]["value"])
			self.userid = date["data"][0]["value"]
		else:
			self.userid = None


	def talk(self,words):
		register_data = {"cmd" : "chat","appid" : self.__key,"userid" : self.__userid,"text" : words,"iformat" : "text","oformat" : "text"}
		r = requests.post(self.__url, params=register_data)
		if r:
			# ~ print(r.content)
			if not words == None:
				result = json.loads(r.content)
				if result["return"] == 0 and result["data"][0]["cmd"] == "":
					# ~ url_file = result["data"][1]["value"]
					info = result["data"][0]["value"]
					# ~ print('奇奇：'+info)
					return info
				else:
					return None
			else:
				return None
		else:
			return None


def play(file_name,run_in_background=0):
	p = subprocess.Popen('mpg123 %s'%file_name,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if run_in_background == 1:
		print('后台播放:%s'%file_name)
	else:
		print('播放:%s'%file_name+'\n等待播放结束...')
		sout = p.stdout.readlines()
	return 0


def record(t,file_name):
	p = subprocess.Popen('sudo arecord -q -D "plughw:1" -f S16_LE -r 16000 -c 1 -d %s %s'%(str(t),file_name),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print('录音中，%s秒...'%str(t))
	sout = p.stdout.readlines()
	print('录音完成，文件名为：%s'%file_name)
	return file_name
