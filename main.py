import sys
print sys.getdefaultencoding()
def force_utf8():
	import imp
	_sys_org = imp.load_dynamic('_sys_org', 'sys')
	_sys_org.setdefaultencoding('utf-8')
	del _sys_org

force_utf8()
print sys.getdefaultencoding()

from handler import *
from hybrid import *
import os

load_commands()
try:
	mon_start()
	handler_start()
	mon_page()
except KeyboardInterrupt:
	os._exit(0)