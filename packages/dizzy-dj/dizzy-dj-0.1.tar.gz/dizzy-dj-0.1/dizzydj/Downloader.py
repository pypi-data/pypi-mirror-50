import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Downloader:
	"""Converts YouTube videos to mp3 and downloads them to the specified directory

		Args:
			email (str): Google email ID
			playlist (str): Playlist containing the videos that are converted to mp3
			driver_path (str): Path to chromedriver.exe Make sure to make it a raw string
			quality (str): Quality of downloaded mp3 in kbps. Valid values are-
				'320'
				'256'
				'192'
				'128'
	"""

	def __init__(self, email, playlist, driver_path, quality='320'):
		self.email = email
		self.password = getpass.getpass('Enter password: ')
		self.playlist = playlist
		self.driver_path = driver_path
		self.quality = quality

	def _chrome_driver(self):
		driver = webdriver.Chrome(self.driver_path)
		driver.get('https://www.youtube.com/')
		driver.maximize_window()

		return driver

	def download(self):
		driver = self._chrome_driver()
		driver.implicitly_wait(20)
		
		xp_sign = driver.find_elements_by_xpath('//*[@id="text"]')[1]
		xp_sign.click()

		xp_username = driver.find_element_by_xpath('//input[@type="email"]')
		xp_username.send_keys(self.email + Keys.RETURN)
		time.sleep(2)
		xp_password = driver.find_element_by_xpath('//input[@type="password"]')
		xp_password.send_keys(self.password + Keys.RETURN)

		xp_music = driver.find_element_by_xpath('//span[text()="{}"]'.format(self.playlist))
		xp_music.click()
		xp_links = driver.find_elements_by_xpath(
			'//a[@class="yt-simple-endpoint style-scope ytd-playlist-video-renderer"]')

		links = []
		for i in xp_links:
			links.append(i.get_attribute('href'))

		for i in links:
			driver.get('https://www.onlinevideoconverter.com/mp3-converter')
			time.sleep(1)

			xp_link = driver.find_element_by_xpath('//input[@name="texturl"]')
			xp_link.send_keys(i)
			xp_options = driver.find_element_by_xpath('//*[@id="advanced-options-link"]')
			xp_options.click()
			xp_bitrate = driver.find_element_by_xpath('//*[@id="audioBitrate"]')
			xp_bitrate.click()
			time.sleep(1)
			xp_320 = driver.find_element_by_xpath('//a[text()="{} kbps"]'.format(self.quality))
			xp_320.click()
			xp_start = driver.find_element_by_xpath('//a[@class="start-button"]')
			xp_start.click()
			time.sleep(1)

			if len(driver.window_handles) > 1:
				driver.switch_to.window(driver.window_handles[-1])
				driver.close()
				driver.switch_to.window(driver.window_handles[0])

			try:
				xp_download = driver.find_element_by_xpath('//a[@id="downloadq"]')
				xp_download.click()
			except:
				print('Unable to download {}'.format(i))
