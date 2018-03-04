# Android environment
import pytest
from appium import webdriver
import os
import time

# 아래 필요한 정보들을 기입해 줍니다.
# 안드로이드 버전은 5.1로 하였습니다.
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1'
desired_caps['deviceName'] = 'Android Emulator'
# 아래 테스트하고자 하는 app의 apk경로를 넣어줍니다.
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../app/debug/app-debug.apk')
desired_caps['app'] = filename

# appium이 돌아가고 있는 서버의 http 주소를 입력해줍니다.
# 현재를 local에서 실행하고 있기 때문에 아래처럼 작성하였습니다.
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# 웹뷰를 가져옵니다.
driver.switch_to.context('WEBVIEW')

def test_mainpage_has_text():
	time.sleep(15)

	# 첫 페이지에 들어갔을 때
	# '지금 한강은'이라는게 화면에 나와있고
	assert '지금 한강은' in driver.page_source

	# 온도를 봤는데 요청한 값과 같게 나온다.
	import urllib.request
	request = urllib.request.Request('https://undang.twpower.me/temperatures')
	response = urllib.request.urlopen(request)
	import json
	result_in_json = json.loads(response.read().decode('utf-8'))
	api_temperature = result_in_json['구리']

	html_temperature = driver.find_element_by_id('temperature').text
	print("\n\n\n" + html_temperature + "\n\n\n")

	assert api_temperature == html_temperature

	driver.close_app();