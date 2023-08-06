from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

from zipfile import ZipFile
from rarfile import RarFile

config = Config.getConfig(parentKey='modules', key='ht_unzip')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_unzip'))

	def extractFile(self, zipPathName, password):
		#ZipFile only works with 7z with ZypCrypto encryption for setting the password
		try:
			if '.zip' in zipPathName[:4]:
				Logger.printMessage(message="extractFile", description='ZIP - {pwd}'.format(pwd=password), debug_core=True)
				with ZipFile(zipPathName) as zf:
					zf.extractall(pwd=str.encode(password))
			else:
				Logger.printMessage(message="extractFile", description='RAR - {pwd}'.format(pwd=password), debug_core=True)
				with RarFile(zipPathName) as rf:
					rf.extractall(pwd=str.encode(password))
			return password
		except Exception as e:
			return None