import re
import csv
from bs4 import BeautifulSoup
import urllib
import requests
import time
import pymysql
from tqdm import tqdm
db=pymysql.connect(host='localhost',user='hefeng',passwd='hf2010',db='mydb')
pattern='\"https://movie.douban.com/subject/(.*)/\"'
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36',
'Referer':'https://movie.douban.com/','Host':'movie.douban.com'}
f = open('movies.csv', "rt", encoding='utf-8')
reader=csv.reader(f,delimiter=',')
arr=[]
def insert(a,b,c):
	cur=db.cursor()
	sql='insert into movie (movie_id,movie_name,movie_id_douban) values(%s,%s,%s)'
	try:
		cur.execute(sql,(a,b,c))
	except:
		pass
	db.commit()
	cur.close()
for row in reader:
	single=[]
	temp=row[1].split('(')
	temp[0]=temp[0].strip()
	single.append(row[0])
	single.append(temp[0])     
	arr.append(single)
	#print(temp[0])
for movie_name in tqdm(arr):
	print('')
	print(''.join(movie_name[1]))
	flag=0
	result={'search_text':''.join(movie_name[1])}
	search_name=urllib.parse.urlencode(result)
	r=requests.get('https://movie.douban.com/subject_search?%s&cat=1002'%search_name,headers=headers)
	soup = BeautifulSoup(r.text,'lxml')
	for i in soup.find_all('a'):
		if 'mv_subject_search' in str(i):
			single_str=str(i)
			flag=1
			break
	if flag:
		str_r=re.findall(pattern,single_str)
		if str_r:
			print(str_r)
			insert(''.join(movie_name[0]),''.join(movie_name[1]),''.join(re.findall(pattern,single_str)))
	else:
		#print('Not found')
		insert(''.join(movie_name[0]),''.join(movie_name[1]),-1)
	time.sleep(1.5)
	#print(movie_name)
db.close()
#print(arr)