import urllib.request
import json
def fetch(id):
	url='http://www.omdbapi.com/?i=tt'+id+'&plot=short&r=json'
	page= urllib.request.urlopen(url)
	data=page.read()
	data= data.decode("utf8")
	dic=json.loads(data)
	return dic
print(fetch('3849692'))
		