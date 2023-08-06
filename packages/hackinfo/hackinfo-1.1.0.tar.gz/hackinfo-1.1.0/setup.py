# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['hackinfo']
setup_kwargs = {
    'name': 'hackinfo',
    'version': '1.1.0',
    'description': 'web application Hejab Zaeri',
    'long_description': '# Library install hackinfo:\n```bash\nsudo python3 setup.py install \npip3 install hackinfo\n```\n\n\n```python\n\nfrom hackinfo import hackinfo \nhackinfo.nmap("www.google.com")\n\n[+] <-- Running Nmap....[www.google.com] -->\nStarting Nmap 7.70 ( https://nmap.org ) at 2019-08-15 17:12 UTC\nNmap scan report for www.google.com (172.217.3.100)\nHost is up (0.0023s latency).\nOther addresses for www.google.com (not scanned): 2607:f8b0:4006:801::2004\nrDNS record for 172.217.3.100: lga34s18-in-f4.1e100.net\n\nPORT     STATE    SERVICE\n21/tcp   filtered ftp\n22/tcp   filtered ssh\n23/tcp   filtered telnet\n80/tcp   open     http\n110/tcp  filtered pop3\n143/tcp  filtered imap\n443/tcp  open     https\n3389/tcp filtered ms-wbt-server\n\nNmap done: 1 IP address (1 host up) scanned in 1.25 seconds\n```\n```python\n\nhackinfo.reverseiplookup("www.facebook.com")\n[+] <-- Running Reverseiplookup ....[www.facebook.com] -->\nedge-star-mini-shv-01-sjc3.facebook.com\nfacebook.com\nfbdogfoodbeta.com\nmobileironbackup.com\npurpletiesupport.com\nstar-mini.c10r.facebook.com\n```\n\n\n![Library_install_hackinfo](https://www.upload.ee/image/10356700/hejab_Library_install_hackinfo.png)\n\n',
    'author': 'Hejab Zaeri',
    'author_email': None,
    'url': 'https://github.com/Matrix07ksa/HackerInfo',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
