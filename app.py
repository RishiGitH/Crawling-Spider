from flask import Flask, request, render_template,redirect ,url_for,session
import test2
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
from urllib.parse import urlparse
from random import randint
import re
app = Flask(__name__, template_folder='website')
app.secret_key = "5H473893939$385H"


@app.route('/')
def my_form():
	return render_template('url1.html')

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['url']
	session['processed_text'] = text
	session['val']=0
	
	return redirect(url_for('data'))

@app.route('/data')
def data():
	if(session.get('val', None)==0):
		data=test2.data(session.get('processed_text', None))
	else:
		data=test2.loop()
	session['val']=1


	return render_template('url2.html',data=data)



if __name__ == "__main__":
	app.run(debug=True)
