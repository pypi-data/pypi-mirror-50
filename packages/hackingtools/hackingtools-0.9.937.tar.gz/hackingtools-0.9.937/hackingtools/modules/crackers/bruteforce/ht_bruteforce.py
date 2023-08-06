from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

import progressbar

config = Config.getConfig(parentKey='modules', key='ht_bruteforce')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		Utils.emptyDirectory(output_dir)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_bruteforce'))

	def crackZip(self, zipPathName, alphabet='lalpha', log=False):
		unzipper = ht.getModule('ht_unzip')
		tested = []
		if log:
			Logger.setDebugCore(True)
		texts = Utils.getDict(length=4, alphabet=alphabet, consecutive=True)
		while True:
			for text in texts:
				if not text in tested:
					tested.append(text)
					if unzipper.extractFile(zipPathName, text):
						Logger.setDebugCore(False)
						return text
			return None
		return None