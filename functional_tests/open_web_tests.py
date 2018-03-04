import pytest
from appium import webdriver
import os
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1'
desired_caps['deviceName'] = 'Android Emulator'

# app path setting
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../app/build/outputs/apk/debug/app-debug.apk')
desired_caps['app'] = filename


def test_mainpage_has_text():
	time.sleep(15)

	# 태우가 앱을 실행했을 때
	driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

	# 웹뷰 화면이 나왔다.
	driver.switch_to.context('WEBVIEW')

	# '지금 한강은'이라는게 화면에 나와있었고
	assert '지금 한강은' in driver.page_source

	# 그 아래에서 온도를 확인할 수 있었다.
	import urllib.request
	request = urllib.request.Request('https://undang.twpower.me/temperatures')
	response = urllib.request.urlopen(request)
	import json
	result_in_json = json.loads(response.read().decode('utf-8'))
	api_temperature = result_in_json['구리']

	html_temperature = driver.find_element_by_id('temperature').text
	print("\n\n\n" + html_temperature + "\n\n\n")

	assert api_temperature == html_temperature

	# 온도를 확인하고 앱을 종료하였다.
	driver.close_app();