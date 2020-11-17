from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sqlite3 import connect
from time import sleep as _sleep
from random import random
from pyvirtualdisplay import Display

username = 'YOUR ACCOUNT USERNAME'
password = 'YOUR ACCOUNT PASSWORD'
login_url = 'https://poshmark.com/login'
closet = 'https://poshmark.com/closet/{}/?availability=available'.format(username)

# redefine the sleep function to add a second of randomness to fool bot detectors
def sleep(seconds):
	_sleep(seconds + random())

def login():
	print('Logging into: {}'.format(username))
	u,p = 'login_form_username_email','login_form_password'
	driver.get(login_url)
	sleep(4)
	user = driver.find_element_by_id(u)
	pword = driver.find_element_by_id(p)
	user.send_keys(username)
	pword.send_keys(password)
	pword.send_keys(Keys.RETURN)
	sleep(4)
	
def load_closet():
	print('Loading Closet')
	driver.get(closet)
	sleep(5)
	t = 0
	while True:
		c = driver.execute_script('return document.body.scrollHeight;')
		if c == t:
			break
		else:
			driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
			sleep(10)
			t = c
def share_closet():
	shares = driver.find_elements_by_class_name('share')
	print('There are {} listings in your closet.'.format(len(shares)))
	sleep(5)
	shared = 0
	for e,item in enumerate(shares):
		#item.click() is not the best method, best to execute the script on the client side.
		driver.execute_script('arguments[0].click();',item)
		sleep(5)
		followers = driver.find_element_by_class_name('pm-followers-share-link')
		if followers.text == 'To My Followers':
			#followers.click()
			driver.execute_script('arguments[0].click();',followers)
			shared += 1
			print('Shared the {} item in your closet.'.format(shared))
			sleep(5)
	print('We shared {} items.'.format(shared))
	print('Now we will wait for 6 hours before we share again.')

if __name__ == '__main__':
	while True:
		display = Display(visible=0,size=(1024,768))
		display.start()
		sleep(10)
		driver = webdriver.Chrome()
		sleep(5)
		login()
		load_closet()
		share_closet()
		driver.close()
		display.stop()
		sleep(21600) # sleep for 6 hours i.e. 21600 seconds
