import os
from importlib import reload

def reload_pyppeteer():	
	os.putenv("PYPPETEER_CHROMIUM_REVISION", "1230501")
	import pyppeteer.chromium_downloader as pyppeteer_downloader
	reload(pyppeteer_downloader)