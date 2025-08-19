import os
import sys
from importlib import reload
from site import getusersitepackages

def reload_pyppeteer():	
	os.putenv("PYPPETEER_CHROMIUM_REVISION", "1230501")
	try:
		import pyppeteer.chromium_downloader as pyppeteer_downloader
		reload(pyppeteer_downloader)
	except:
		pass

def get_user_site_packages() -> str:
	return str(getusersitepackages())

def add_user_site_packages():
	site_packages = get_user_site_packages()
	if site_packages not in sys.path:
		sys.path.append(site_packages)