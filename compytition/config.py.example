import os
from compytition import app

app.config['SECRET_KEY'] = 'thiskeyneedstobesecret'
app.config['DATABASE'] = '/tmp/compytition.db'
app.config['SOLUTIONS_DIR'] = 'solutions'
app.config['QUESTION_DIR'] = 'questions'
app.config['QUESTIONS'] = []
for f in sorted(os.listdir(app.config['QUESTION_DIR'])):
	path = os.path.join(app.config['QUESTION_DIR'], f)
	question = {
		'base': f,
		'src': path,
		'content': open(path).read()
		}
	app.config['QUESTIONS'].append(question)
