# versionchecker

Check for outdated packages installed on your system and get the latest version number

### Installation
 `pip install versionchecker`

### Usage
The package list should be in the format  {package_name: online_name}

>	from versionchecker import check_packages
	packages = {
		'urllib3': 'urllib3',
		'bs4': 'beautifulsoup4'
	}
    results, latest_version = check_packages(packages)
    print(results)
    print(latest_version)


    {'urllib3': True, 'bs4': False}
    {bs4': '4.8.0'}



License
----
MIT
