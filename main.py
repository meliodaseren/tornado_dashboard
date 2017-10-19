import os.path
import datetime
# import pymysql
# from pymongo import MongoClient
from tornado.options import define, options
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web

define("port", default=7777, help="Run on the given port", type=int)

class index(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

class login(tornado.web.RequestHandler):
    def post(self):
        user_name = self.get_argument("username")
        user_email = self.get_argument("email")
        user_website = self.get_argument("website")
        user_language = self.get_argument("language")
        self.render("auth.html",
                    username=user_name,
                    email=user_email,
                    website=user_website,
                    language=user_language)

class line(tornado.web.RequestHandler):
    def get(self):
        self.render("line.html")

class model(tornado.web.RequestHandler):
    def get(self):
        self.render("model.html")

class power(tornado.web.RequestHandler):
    def get(self):
        self.render("power.html")   

class bars(tornado.web.RequestHandler):
    def get(self):
        self.render("bars.html")       


class table(tornado.web.RequestHandler):
    def get(self):
        # self.render("table.html") 
        conn = pymysql.connect(host='localhost', port=3306,
                               user='hive', passwd='123456', db='test')
        cur = conn.cursor()
        cur.execute("SELECT * FROM shop LIMIT 1000")
        # cur.execute("SELECT typeid,lat,lng FROM test WHERE typeid='102' LIMIT 10")   
        rows = cur.fetchall()
        self.render("table.html",dbrow=rows)

        
class test(tornado.web.RequestHandler):
    def get(self):
        client = MongoClient("localhost",27777)
        db = client.test
        db.authenticate("test","",source="admin")
        mdb = db.my_collection.find({})
            
        self.render('test.html',
                    header_text="OOOO1",
                    footer_text=mdb[0])
    
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS") 

        client = MongoClient("localhost",27777)
        db = client.test
        db.authenticate("test", "", source="admin")
		
        username = self.get_argument("username")
        password = self.get_argument("password")
        imei = self.get_argument("imei")
        lat = self.get_argument("lat")
        lon = self.get_argument("lon")
        alt = self.get_argument("alt")

        db.test.insert({"thisTime":str(datetime.datetime.utcnow()),
                        "username":username,
                        "password":password,
                        "imei":imei,
                        "lat":lat,
                        "lon":lon,
                        "alt":alt})

        self.write(username + "<br/>" + password + "<br/>" +
                   imei + "<br/>" + lat + "<br/>" + lon + "<br/>" + alt)


class countMember(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

        client = MongoClient("localhost",27777)
        db = client.test
        db.authenticate("test", "", source="admin")
        members = str(db.test.find({}).count())
        self.write(members)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [(r'/', index),
                   (r'/login',login),
                   (r'/test',test),
                   (r'/line',line),
		           (r'/countMember',countMember),
                   (r'/power',power),
                   (r'/bars',bars),
                   (r'/table',table)
                   ],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
