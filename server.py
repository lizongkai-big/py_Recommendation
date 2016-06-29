from apscheduler.schedulers.background import BackgroundScheduler
import time, sys, cherrypy, os
from paste.translogger import TransLogger
from mywork import create_app
#from pyspark import SparkContext, SparkConf
from update import top10_update
#def update_mysql(sc):

#def get_new_rating():
			
 
def run_server(app):
 
    app_logged = TransLogger(app)
 
    cherrypy.tree.graft(app_logged, '/')
 
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '0.0.0.0'
    })
 
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
 
if __name__ == "__main__":
    dataset_path = os.path.join('datasets', 'ml-latest')
    app = create_app()
    scheduler = BackgroundScheduler()
    scheduler.add_job(top10_update, 'interval', seconds=60)  
    scheduler.start() 
    run_server(app)