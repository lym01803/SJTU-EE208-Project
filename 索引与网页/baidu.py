from aip import AipOcr
class baiduApi:
	def __init__(self, APP_ID, API_KEY, SECRET_KEY):
		self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	def get_file_content(self, imageFile):
		with open(imageFile, 'rb') as fp:
			return fp.read()

	def getWordFromImage(self, imageFile):
		#Simple 
		image = self.get_file_content(imageFile)
		result = self.client.basicGeneral(image)
		return result

	def getWordFromImage2(self, imageFile):
		#with options
		options = {}
		options["language_type"] = "CHN_ENG"
		options["detect_direction"] = "true"
		options["detect_language"] = "true"
		options["probability"] = "true"
		image = self.get_file_content(imageFile)
		result = self.client.basicAccurate(image, options)
		return result

	def getWordFromByte(self, byteimg):
		result = self.client.basicGeneral(byteimg)
		return result

	def getWordFromByte2(self, byteimg):
		options = {}
		options["language_type"] = "CHN_ENG"
		options["detect_direction"] = "true"
		options["detect_language"] = "true"
		options["probability"] = "false"
		result = self.client.basicAccurate(byteimg, options)
		return result

if __name__ == "__main__":
	APP_ID = '18241180'
	API_KEY = 'bMy96yjZgd60hlxy18RK1IxU'
	SECRET_KEY = 'VF945GTaYuHLgc0lWOfIuToVGF2vWXt7'
	obj = baiduApi(APP_ID, API_KEY, SECRET_KEY)
	print obj.getWordFromImage('sony2.jpg')
	print obj.getWordFromImage2('sony2.jpg')