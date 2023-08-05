#_*_ coding:UTF-8 _*_
import requests
import json
import sys
import time
import threading
import os
from aip import AipSpeech
import RPi.GPIO as GPIO
from pirc522 import RFID

GPIO.setmode(GPIO.BOARD)

class UltrasonicSensor:
    def __init__(self,trig,echo):
        self.GPIO_TRIGGER = trig
        self.GPIO_ECHO = echo
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
    def distance(self):
        # 发送高电平信号到 Trig 引脚
        GPIO.output(self.GPIO_TRIGGER, True)
        # 持续 10 us 
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
        start_time = time.time()
        stop_time = time.time()
        # 记录发送超声波的时刻1
        while GPIO.input(self.GPIO_ECHO) == 0:
            start_time = time.time()
        # 记录接收到返回超声波的时刻2
        while GPIO.input(self.GPIO_ECHO) == 1:
            stop_time = time.time()
        # 计算超声波的往返时间 = 时刻2 - 时刻1
        time_elapsed = stop_time - start_time
        # 声波的速度为 343m/s， 转化为 34300cm/s。
        distance = (time_elapsed * 34300) / 2
        return distance
        
        
class ColorSensor:
    count = 0
    def _my_callback(self, channel):
        self.count += 1
	
	
    def rgb2hsv(self, r, g, b):
      mx = max(r, g, b)
      mn = min(r, g, b)
      df = mx-mn
      if mx == mn:
	  h = 0
      elif mx == r:
	  h = (60 * ((g-b)/df) + 360) % 360
      elif mx == g:
	  h = (60 * ((b-r)/df) + 120) % 360
      elif mx == b:
	  h = (60 * ((r-g)/df) + 240) % 360
      if mx == 0:
	  s = 0
      else:
	  s = df/mx
      v = mx
      print(h, s, v)
      return h, s, v
    
    
    def __init__(self,S0,S1,S2,S3,OUT):
        self.S0 = S0
        self.S1 = S1
        self.S2 = S2
        self.S3 = S3
        self.OUT = OUT
        
        GPIO.setup(36, GPIO.IN)
        
        GPIO.setup(self.S0, GPIO.OUT)
        GPIO.setup(self.S1, GPIO.OUT)
        GPIO.setup(self.S2, GPIO.OUT)
        GPIO.setup(self.S3, GPIO.OUT)
        GPIO.setup(self.OUT, GPIO.IN)
        GPIO.output(self.S0, GPIO.HIGH)
        GPIO.output(self.S1, GPIO.HIGH)
        GPIO.output(self.S2, GPIO.LOW)
        GPIO.output(self.S3, GPIO.LOW)
        GPIO.add_event_detect(self.OUT, GPIO.RISING, callback=self._my_callback)

    def read(self):
        self.count = 0
        GPIO.output(self.S2, GPIO.LOW)
        GPIO.output(self.S3, GPIO.LOW)
        time.sleep(0.1)
        red = self.count
        self.count = 0
        GPIO.output(self.S2, GPIO.HIGH)
        GPIO.output(self.S3, GPIO.HIGH)
        time.sleep(0.1)
        green = 1.3 * self.count
        self.count = 0
        GPIO.output(self.S2, GPIO.LOW)
        GPIO.output(self.S3, GPIO.HIGH)
        time.sleep(0.1)
        blue = 1.14 * self.count
        self.count = 0
        # ~ print('RED:',red,'GREEN:',green,'BLUE:',blue)
        cmax = max(red,green,blue)
	h,s,v = self.rgb2hsv(r/cmax,g/cmax,b/cmax)
	if s >= 43 and s <=255 and v >= 46 and v <= 255:
	    if ((h>0 and h<10) or (h>156 and h<180)):
		print('red\n')
		return 3
	    elif h >=35 and h <=77:
		print('green\n')
		return 1
	    elif h >=100 and h <=124:
		print('blue\n')
		return 2
	    else:
		print('others\n')
		return -1
	elif h >=0 and h <= 180:
	    print('gray\n')
	    return 4
	else:
	    print('others\n')
	    return -1
	    

        # ~ r = red /cmax
        # ~ g = green /cmax
        # ~ b = blue /cmax
        # ~ print('r:',r,',g:',g,',b:',b)
        
        
class CardReader:
  uid = [0,0,0,0,0,]
  flag = 0
  score = 0
  data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
  rdr = RFID()
  
  
  def __init__(self):
    RFID_timer = threading.Timer(0.1,self._callback)
    RFID_timer.start()
    
    
  def read(self):
    return self.score
  
  
  def write(self,score):
    self.score = score
    for i in range(15):
      self.data[i] = int(score & 0xff)
      score = score >> 8
    self.flag = 2
  
  
  def wait_for_swipe(self):
    while self.flag != 1:
      pass
    self.flag = 0
    
  
  def wait_for_tag(self):
    self.rdr.wait_for_tag()
    
    
  def get_uid(self):
    return self.uid
  
  def _transfer(self,data):
    S = 0
    for i in range(15):
      S += data[i]*256**i
    return S
    
    
  def _callback(self):
    self.rdr.wait_for_tag()
    (error, tag_type) = self.rdr.request()
    if not error:
      # ~ print("Tag detected")
      (error, self.uid) = self.rdr.anticoll()
      if not error:
        # ~ print("UID: " + str(self.uid))
        # Select Tag is required before Auth
        if not self.rdr.select_tag(self.uid):
          if not self.rdr.card_auth(self.rdr.auth_a, 8, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], self.uid):
            if self.flag == 0:
            # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
              error,self.data = self.rdr.read(8)
              self.score = self._transfer(self.data)
              self.flag = 1
              # ~ print('Read:'+str(self.data))
              print('Score:'+str(self.score))
            elif self.flag == 2:
              self.rdr.write(8,self.data)
              print('Write:'+str(self.data))
              # ~ print('Score:'+str(self.score))
              self.flag = 0
              self.score = 0
            # Always stop crypto1 when done working
            self.rdr.stop_crypto()
            RFID_timer = threading.Timer(0.1,self._callback)
            RFID_timer.start()


class Servo:

	def __init__(self,num,angle):
		GPIO.setup(num,GPIO.OUT)
		self.p=GPIO.PWM(num,50)
		self.p.start(self._transfer(angle))
		
		
	def _transfer(self,t):
		d=round(t*10.0/180.0+2.5,1)
		return d
		
		
	def set(self,angle):
		if angle<0 or angle>180:
			self.p.stop()
		else:
			self.p.ChangeDutyCycle(self._transfer(angle))


class Key:
	def __init__(self,num):
		self.key = num
		GPIO.setup(self.key, GPIO.IN)
		
		
	def wait_for_press(self):
		GPIO.wait_for_edge(self.key,GPIO.RISING)
	
	
	def read(self):
		return GPIO.read(self.key)
		
		
class QiQi:
	# ~ 你的APPID AK SK  参数在申请的百度云语音服务
	APP_ID = '15033863'
	API_KEY = 'rtNzpQWEnIIrA2sGdxzFdQ5a'
	SECRET_KEY = '8V1P7lGEQ03HVAuNQNhcNOgEqiAeU9NG'
	# ~ http://www.emotibot.com/
	key = "488b046dd31262f22244aa4c5a97b631"
	url = "http://idc.emotibot.com/api/ApiKey/openapi.php"
	userid ='0EE4B632A2C4FA33803D65BA81E8776D9'

	# 新建一个AipSpeech
	client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	
	
	def __init__(self):
		payload = {"cmd" : "register","appid" : self.key}
		r = requests.post(self.url, data=payload)
		if r:
		# ~ print(r.content)
			date = json.loads(r.content)
			# ~ print(date["data"][0]["value"])
			self.userid = date["data"][0]["value"]
		else:
			self.userid = None
	# 读取文件
	def get_file_content(self,filePath):   #filePath  待读取文件名
		with open(filePath, 'rb') as fp:
			return fp.read()


	def stt(self,filename): # 语音识别
		# 识别本地文件
		result = self.client.asr(self.get_file_content(filename),'wav',16000,{'dev_pid': 1536,})  # dev_pid参数表示识别的语言类型 1536表示普通话
		print(result)
		# 解析返回值，打印语音识别的结果
		if result['err_msg']=='success.':
			word = result['result'][0].encode('utf-8')   # utf-8编码
			if word!='':
			   return word
			else:
				print("音频文件不存在或格式错误")
				return None
		else:
			print("错误")
			return None


	# 将文本进行语音合成
	def tts(self,command):
		if len(command) != 0:
			word = command
			result  = self.client.synthesis(word,'zh',1, {'vol': 6,'per':4, 'pit':6,})
		# 合成正确返回audio.mp3，错误则返回dict 
		if not isinstance(result, dict):
			with open('audio.mp3', 'wb') as f:
				f.write(result)
			f.close()
			# print ('tts successful')


	def emotibot(self,words):

		register_data = {"cmd" : "chat","appid" : self.key,"userid" : self.userid,"text" : words,"iformat" : "text","oformat" : "voice"}
		r = requests.post(self.url, params=register_data)
		if r:
			# ~ print(r.content)
			return r.content
		else:
			return None
	def response(self,t):
		os.popen('mpg123 deng.mp3')
		os.system('sudo arecord -D "plughw:1" -f S16_LE -r 16000 -d %s voice.wav'%str(t))
		os.popen('mpg123 wait.mp3')
		#os.system('ffmpeg -y  -i audio.mp3  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm')
		os.system('ffmpeg -y  -i voice.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm')
		words = self.stt('16k.pcm')
		if not words == None:
			result = json.loads(self.emotibot(words))
			if result["return"] == 0 and result["data"][0]["cmd"] == "":
				url_file = result["data"][1]["value"]
				info = result["data"][0]["value"]
				print(info)
				self.speak(url_file)
				return info
	def speak(self,audio_file):
		p = os.popen('mpg123 %s'%audio_file)
		tmp = p.read()
		p.close()
