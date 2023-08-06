from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_bruteforce')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_bruteforce'))

	def crackZip(self, zipPathName):
		password = None
		unzipper = ht.getModule('ht_unzip')
		while not password:
			password = unzipper.extractFile(zipPathName, Utils.randomText())
		print(password)
		return password