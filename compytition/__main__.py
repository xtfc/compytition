import sys
if '.' not in sys.path:
	sys.path.append('.')
from compytition import app

app.run(host='0.0.0.0', debug=True)
