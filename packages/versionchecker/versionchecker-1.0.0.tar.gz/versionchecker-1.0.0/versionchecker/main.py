import urllib.request
import json
import importlib

results = {}
latest_version = {}


def check_packages(package_dict):
	for package_name, online_name in package_dict.items():
		mod = importlib.import_module(package_name)
		online_version = get_latest_version(online_name)
		try:
			current_version = mod.__version__
			if current_version != online_version:
				results[package_name] = False
				latest_version[package_name] = online_version
			else:
				results[package_name] = True
		except Exception as e:
			print('Error retrieving info on', package_name, 'Reason:', e,
			      '\nPlease fix the dictionary items or remove them.')
	return results, latest_version


def get_latest_version(online_name):
	data = urllib.request.urlopen("https://www.pypi.org/pypi/" + online_name + "/json").read()
	output = json.loads(data)
	version_no = output['info']['version']
	online_version = version_no[0:6]
	return online_version
