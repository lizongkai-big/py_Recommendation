from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash,Blueprint
import random
import urllib.request
import json
class movie(object):
	def __init__(self, m_id=None,name=None):
		self.random_id=['143257','143882','142973','141688','142536','141472','142488','140820','140715']
		if name==None:
			if m_id=='-1':
				self.id=self.random_id[random.randint(0,8)]
			else:
				self.id=m_id
			print(self.id)
			self.get_movie_name(self.id)
		else:
			self.get_movie_id(name)
			self.name=name
		self.get_movie_imdb_id(self.id)
	def get_movie_id(self,name):
		cur=g.db.cursor()
		cur.execute('select name from movie_id where movie_name=\'%s\''%name)
		cur.close()
		Name=cur.fetchall()
		self.id=Name[0][0]
	def get_movie_name(self,m_id):
		cur=g.db.cursor()
		cur.execute('select name from movie_name where movie_id=\'%s\''%m_id)
		cur.close()
		Name=cur.fetchall()
		self.name=Name[0][0]
	def get_movie_imdb_id(self,m_id):
		cur=g.db.cursor()
		cur.execute('select imdb_id from imdb_movies where movie_id=\'%s\''%m_id)
		cur.close()
		result=cur.fetchall()
		self.imdb_id=result[0][0]
	def fetch(self):
		url='http://www.omdbapi.com/?i=tt'+self.imdb_id+'&plot=short&r=json'
		page= urllib.request.urlopen(url)
		data=page.read()
		data= data.decode("utf8")
		dic=json.loads(data)
		return dic
class user(object):
	def __init__(self, name):
		self.username=name
		self.getuser_id(name)
		self.top_10=[]
		#print(self.id)
		self.get_user_intertests(self.id)
	def get_user_intertests(self,user_id):
		cur=g.db.cursor()
		cur.execute('select * from top_10 where id =\'%s\''%user_id)
		cur.close()
		temp=cur.fetchall()
		#print(temp)
		for i in range(1,11):
			self.top_10.append(movie(m_id=temp[0][i]))
	def getuser_id(self,username):
		cur=g.db.cursor()
		cur.execute('select id from user where username=\'%s\''  %username)
		cur.close()
		result =cur.fetchall()
		self.id=result[0][0]