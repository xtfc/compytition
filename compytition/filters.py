import time
from compytition import app

@app.template_filter('time')
def filter_time(seconds):
	if int(seconds) == 0:
		return '&#8210;'
	return time.strftime("%H:%M:%S", time.gmtime(float(seconds)))
