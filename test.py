import pymysql
db=pymysql.connect(host='localhost',user='hefeng',passwd='hf2010',db='mydb')
cur=db.cursor()
cur.execute('SELECT movie_id FROM imdb_movies ORDER BY RAND() LIMIT 10')
re=cur.fetchall()
print(re)
print(re[9][0])