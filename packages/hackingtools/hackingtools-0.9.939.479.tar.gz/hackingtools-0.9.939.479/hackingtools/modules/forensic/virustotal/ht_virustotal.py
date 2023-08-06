from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_virustotal')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_virustotal'))

	def isBadFile(self, filename):
		try:
			API_KEY = "9334cb7d7d9807f2c508a0eb025c9e2fdaa6c9ce907ccf7326a93bee5fbef172"
			api = PublicApi(API_KEY)
			with open(filename, "rb") as f:
				file_hash = md5(f.read()).hexdigest()
			response = api.get_file_report(file_hash)
			if response["response_code"] == 200:
				if response["results"]["positives"] > 0:
					return True
			return False
		except Exception as e:
			Logger.printMessage(message="isBadFile", description=e, is_error=True)