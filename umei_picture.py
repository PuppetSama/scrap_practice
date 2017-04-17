#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import os


class MMPicture(object):
	"""docstring for MMPicture"""
	def __init__(self):
		self.url = 'http://www.umei.cc/meinvtupian/'
		self.user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'
		self.headers = { 'User-Agent': self.user_agent}

	def getContentIndex(self, url):
		request = urllib2.Request(url, headers = self.headers)
		response = urllib2.urlopen(request)
		content = response.read().decode('utf-8', 'ignore')
		return content

	def getImageInfo(self):
		content = self.getContentIndex(self.url)
		pattern = re.compile('<li>.*?<a href="(.*?)".*?ListTit.*?>(.*?)<', re.S)
		items = re.findall(pattern, content)
		ImageInfo = []
		for item in items:
			ImageInfo.append([item[0].strip(), item[1].strip()])
		return ImageInfo

	def getImageUrls(self, ImageUrl, ImageNum):
		ImageInfo = self.getImageInfo()
		ImageUrls = []
		for i in range(1, int(ImageNum) + 1):
			ImageUrlStr = ''.join(ImageUrl)
			ImageUrlStrRe = ImageUrlStr.replace('.htm', '_' + str(i) + '.htm', 1)
			print(ImageUrlStrRe)
			ImageUrls.append(ImageUrlStrRe)
		return ImageUrls

	def getImageNum(self, ImageUrl):
		ImageContent = self.getContentIndex(ImageUrl)
		pattern = re.compile('<li><a>.(.*?)...</a></li>', re.S)
		ImageNums = re.findall(pattern, ImageContent)
		for ImageNum in ImageNums:
			return ImageNum


	def getDownloadImageUrl(self, ImageUrl):
		ImageContent = self.getContentIndex(ImageUrl)
		pattern = re.compile('ImageBody.*?<img.*?src="(.*?)"', re.S)
		ImageDownloadUrls = []
		ImageDownloadUrl = re.findall(pattern, ImageContent)
		print(ImageDownloadUrl)
		return ImageDownloadUrl

	def DownloadImage(self, ImageDownloadUrl, fileName):
		u = urllib.urlopen(ImageDownloadUrl)
		data = u.read()
		f = open(fileName, 'wb')
		f.write(data)
		f.close()
		print('die die die')

	def PictureMkdir(self, path):
		path = path.strip()
		isExists = os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			return True
		else:
			return False

if __name__ == '__main__':
	spider = MMPicture()
	for [ImageUrl, path] in spider.getImageInfo():
		if spider.PictureMkdir(path):
			ImageNum = spider.getImageNum(ImageUrl)
			ImageUrls = spider.getImageUrls(ImageUrl, ImageNum)
			i = 0
			for AllImageUrl in ImageUrls:
				ImageDownloadUrls = spdier.getDownloadImageUrl(AllImageUrl)
				for ImageDownloadUrl in ImageDownloadUrls:
					print(ImageDownloadUrl)
					i += 1
					spider.DownloadImage(ImageDownloadUrl, path + '\\' + str(i) + '.jpg')


	print('done')



		





