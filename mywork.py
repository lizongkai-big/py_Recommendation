from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash,Blueprint
import pymysql
import random
from my_class import user,movie
main = Blueprint('main', __name__)
SECRET_KEY = 'development key'
def  connect_db():
	return pymysql.connect(host='localhost',user='hefeng',passwd='hf2010',db='mydb')
def get_random_movie(l):
	cur=g.db.cursor()
	cur.execute('SELECT movie_id FROM imdb_movies ORDER BY RAND() LIMIT 10')
	re=cur.fetchall()
	for i in range(10):
		l.append(movie(re[i][0]))
def insert_new_rating(user_id,movie_id,rating):
	cur=g.db.cursor()
	cur.execute('select * from new_ratings where id=%s and movid_id=%s',(user_id,movie_id))
	if cur.fetchall():
		cur.execute('update new_ratings SET rating=%s where id =%s and movid_id=%s',(rating,user_id,movie_id))
	else:
		cur.execute('insert into new_ratings(id,movid_id,rating) values(%s,%s,%s)',(user_id,movie_id,rating))
	cur.close()
	g.db.commit()
@main.route('/<int:m_id>',methods=['POST','GET'])
def movie_information(m_id):
	if request.method=='GET':
		l=[]
		con_movie=movie(m_id=m_id)
		while len(con_movie.imdb_id)<7:
			con_movie.imdb_id='0'+con_movie.imdb_id
		print(con_movie.imdb_id)
		information=con_movie.fetch()
		print(information)
		get_random_movie(l)
		return render_template('movie.html', information=information,l=l,id=m_id)
	else:
		insert_new_rating(session['id'],m_id,request.form['points'])
		return redirect(url_for('main.movie_information',m_id=m_id))
@main.route('/')
def index():
	if session.get('logged_in')==True:
		con_user=user(session['username'])
		session['id']=con_user.id
		return render_template('index.html', movies=con_user.top_10)
	else:
		return redirect(url_for('main.login'))
def check_user(username,password,mode):  #0 is log in 1 is register 2 is insert
	cur=g.db.cursor()
	if mode==0:
		cur.execute('select * from user where username=\'%s\' AND password=\'%s\' '%(username,password))
	elif mode==1:
		cur.execute('select * from user where username=\'%s\''  %username)
	elif mode==2:
		cur.execute('insert into user (username,password) values(\'%s\',\'%s\')' %(username,password))
	g.db.commit()
	cur.close()
	return cur.fetchall()
@main.before_request
def before_request():
    g.db=connect_db()
@main.teardown_request
def teardown_request(exception):
    db=getattr(g,'db',None)
#   db=g.db
    if db is not None:
        db.close() 
@main.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username',None)
	session.pop('id',None)
	#session.pop('id',None)
	flash('You were logged out')
	return redirect(url_for('main.login'))
@main.route('/register',methods=['POST','GET'])
def resister():
	error=None
	if request.method=='POST':
		if len(request.form['password'])<8:
			error='The length of Password must be more than 8'
		elif len(request.form['username'])>20:
			error='The length of username is too long!'
		elif len(request.form['password'])>20:
			erroe='The length of password is too long!'
		elif check_user(request.form['username'], request.form['password'], 1) :
				error='User are already exist'
		else:
			check_user(request.form['username'], request.form['password'],2)
			session['logged_in']=True
			session['username']=request.form['username']
			return redirect(url_for('main.index'))
	return render_template('register.html',error=error)

@main.route('/login',methods=['POST','GET'])
def login():
	error=None
	if session.get('logged_in'):
		return redirect(url_for('main.index'))
	else:
		if request.method=='POST':
			if not check_user(request.form['username'],request.form['password'],0):
				error='Invalid username or password!'
			else:
				session['logged_in']=True
				session['username']=request.form['username']
				return redirect(url_for('main.index'))
	return render_template('login.html',error=error)
@main.route('/movies/<name>')
def movies(name=None):
	if name is not None:
		return render_template('movies.html',get_topten_cov(),get_introduce())
	else:
		abort(404)
def create_app(): 
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.register_blueprint(main)
    return app 