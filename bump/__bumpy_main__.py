import bumpy as b, os, shutil, sys
import db

try:
	from compytition import app
except:
	pass

@b.task
def setup():
	'''Run standard setup tasks'''
	b.shell('git submodule init')
	b.shell('git submodule update')

@b.task
def config():
	'''Create the default config file and open it with $EDITOR'''
	config_ex = os.path.join('compytition', 'config.py.example')
	config = os.path.join('compytition', 'config.py')
	if not os.path.exists(config):
		print "Copying example config..."
		shutil.copyfile(config_ex, config)

	# can't use b.shell because that redirects output!
	os.system('{} "{}"'.format(os.getenv('EDITOR', 'nano'), config))

@b.task(reqs=db.check)
def run():
	'''Run the production server'''
	app.run(host='0.0.0.0')

@b.task(reqs=db.check)
def debug():
	'''Run the debug server'''
	app.run(host='0.0.0.0', debug=True)
