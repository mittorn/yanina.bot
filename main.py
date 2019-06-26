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