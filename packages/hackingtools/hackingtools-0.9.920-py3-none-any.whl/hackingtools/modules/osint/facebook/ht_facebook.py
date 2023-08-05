from hackingtools.core import Logger, Utils, Config
import hackingtools as ht

config = Config.getConfig(parentKey='modules', key='ht_facebook')

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_facebook loaded', debug_module=True)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_facebook'))