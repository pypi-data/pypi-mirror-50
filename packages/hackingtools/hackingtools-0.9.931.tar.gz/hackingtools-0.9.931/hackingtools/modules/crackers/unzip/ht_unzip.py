from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

import zipfile

config = Config.getConfig(parentKey='modules', key='ht_unzip')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_unzip'))

	def extractFile(self, zipPathName, password):
		try:
			zFile = zipfile.ZipFile(zipPathName)
			return zFile.extractall(pwd=password)
		except:
			return None