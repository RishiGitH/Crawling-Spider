from flask import Flask, request, render_template,redirect ,url_for,session
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
import time
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

y=[]
x=[]


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
		data,c=test2.data(session.get('processed_text', None))
	else:
		data,c=test2.loop()
	y.append(c)
	x.append(data)
	session['val']=1
	my_plot_div = plot([Scatter(x=y,y=x)], output_type='div')
	print(data)


	return render_template('url2.html',data=Markup(my_plot_div))



if __name__ == "__main__":
	app.run(debug=True)
