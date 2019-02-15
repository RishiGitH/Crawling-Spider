from flask import Flask, request, render_template
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from urllib.parse import urlparse
from crawler import Crawler, CrawlerCache
import re
app = Flask(__name__, template_folder='website')


@app.route('/')
def my_form():
    return render_template('url1.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['url']
    processed_text = text
    
    return token(processed_text)

def token(data_text=''):
	
	'''
	One way to getting all url 
	connect to a URL
				website = urllib2.urlopen(x)
			
			    #read html code
				html = website.read()
			
				links = re.findall('"((http|ftp)s?://.*?)"', html)

				print (links)
	'''

	crawler = Crawler(CrawlerCache('crawler.db'),depth=1500)
	crawler.crawl(data_text,no_cache=re.compile('^/$').match)
	# displays the urls
	data_text=data_text[8:-1]
	print(crawler.content[data_text].keys())
	return(data_text)

url1=app.route('/', methods=['POST'])
print(url1)


if __name__ == "__main__":
    app.run(debug=True)