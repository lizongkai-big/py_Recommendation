from apscheduler.schedulers.background import BackgroundScheduler
from engine import RecommendationEngine
from paste.translogger import TransLogger
from pyspark import SparkContext, SparkConf
import csv
import pymysql
import os
conf = SparkConf().setAppName("movie_recommendation-server")
sc = SparkContext(conf=conf, pyFiles=['engine.py', 'update.py'])
dataset_path = os.path.join('ml', 'datasets')
d={}
f = open('movies.csv', "rt", encoding='utf-8')
reader=csv.reader(f,delimiter=',')
for row in reader:
	d[row[1]]=row[0]
recommendation_engine = RecommendationEngine(sc, dataset_path)
def find_add_rating(cur):
	cur.execute('select * from new_ratings')
	result=cur.fetchall()
	print('new_ratings')
	print(result)
	if result:
		recommendation_engine.add_ratings(result)
		cur.execute('delete from new_ratings')
		return 1
	else:
		return 0
def exist(i,cur): #exist return 1
	sql='select * from top_10 where id=%s'
	cur.execute(sql,i)
	if cur.fetchall():
		return 1
	else:
		return 0
def top10_update():
		db=pymysql.connect(host='localhost',user='hefeng',passwd='hf2010',db='mydb',charset='utf8' )
		cur=db.cursor()
		if find_add_rating(cur)==1:
			db.commit()
			for i in list(range(1,668)):#668
				l=[]
				rel=recommendation_engine.get_top_ratings(i,10)
				for j in range(0,10):
					if (d.get(rel[j][0],-1)==-1):
						l.append('-1')
					else:
						l.append(d[rel[j][0]])
				if exist(i,cur):
					sql='update top_10 SET movie_id1=%s,movie_id2=%s,movie_id3=%s,movie_id4=%s,movie_id5=%s,movie_id6=%s,movie_id7=%s,movie_id8=%s,movie_id9=%s,movie_id10=%s  where id=%s'
					try:
						cur.execute(sql,(''.join(l[0]),''.join(l[1]),''.join(l[2]),''.join(l[3]),''.join(l[4]),''.join(l[5]),''.join(l[6]),''.join(l[7]),''.join(l[8]),''.join(l[9]),i))
					except:
						break
				else:
					sql='insert into top_10 (id,movie_id1,movie_id2,movie_id3,movie_id4,movie_id5,movie_id6,movie_id7,movie_id8,movie_id9,movie_id10) value(%s,\
						%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
					try:
						cur.execute(sql,(i,''.join(l[0]),''.join(l[1]),''.join(l[2]),''.join(l[3]),''.join(l[4]),''.join(l[5]),''.join(l[6]),''.join(l[7]),''.join(l[8]),''.join(l[9])))
					except:
						break
				db.commit()
		cur.close()
		db.close()
