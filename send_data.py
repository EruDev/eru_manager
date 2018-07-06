import time
from datetime import datetime
import urllib
import urllib3
import requests
import psutil


url = 'http://192.168.76.42:8000/manager/save_data/'
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
}

while True:
	data = {
		"data": psutil.cpu_times().system,
		"time": datetime.now()
	}

	response = requests.post(url=url, data=data)
	print(response.text)
	time.sleep(1)
	# r = requests.post(url, data=data, headers=headers)
	# print(r.text)