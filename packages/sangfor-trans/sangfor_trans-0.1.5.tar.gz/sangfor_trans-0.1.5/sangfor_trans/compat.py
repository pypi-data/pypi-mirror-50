# -*- coding: utf-8 -*-
import sys
try:
    # Python3  
    from urllib.parse import quote
    from http.client import HTTPConnection
    # from hashlib import md5
except ImportError: 
    # Python2 
    from urllib import quote
    from httplib import HTTPConnection
    # import md5

# Python2和Python3兼容
PY3 = sys.version_info > (3, )

unicode_str = str if PY3 else unicode
