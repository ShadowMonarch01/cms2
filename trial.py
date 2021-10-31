#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps
from sqlalchemy import create_engine,Column,Integer,String,Boolean,TEXT,FLOAT,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("mysql+pymysql://sql5447520:nwy2VMhGQW@sql5.freesqldatabase.com/sql5447520")
engine.connect()

Session = sessionmaker(bind=engine)

sesion = Session()

Base = declarative_base()
meta = MetaData()
class User(Base):
    __tablename__ = 'user'

    id=Column( Integer, primary_key=True)
    Email=Column( String(66), unique=True)
    Password=Column( String(20))
    Adm=Column( Boolean(1), default=0)
    FullName=Column( String(200)),
    DateOfBirth=Column( String(20))
    Picture=Column( String(20))
    SchoolStartYear=Column(String(20))
    MajorFieldOfStudy=Column( String(100))
    MinorFieldOfStudy=Column( String(100))
    Courses=Column( TEXT)
    AdCourses=Column( TEXT)
    Average=Column( FLOAT(8))
    Comments=Column( TEXT)
    Suspended=Column( Boolean, default=0)
    Remark=Column( TEXT)

#Base.metadata.create_all(engine)

""" The HTTP request handler """
class RequestHandler(BaseHTTPRequestHandler):

  def _send_cors_headers(self):
      """ Sets headers required for CORS """
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

  def send_dict_response(self, d):
      """ Sends a dictionary (JSON) back to the client """
      self.wfile.write(bytes(dumps(d), "utf8"))

  def do_OPTIONS(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

  def do_GET(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

      response = {}
      response["status"] = "OK"
      self.send_dict_response(response)

  def do_POST(self):
    if self.path.endswith("/register"):
      self.send_response(200)
      self._send_cors_headers()
      self.send_header("Content-Type", "application/json")
      self.end_headers()

      dataLength = int(self.headers["Content-Length"])
      data = self.rfile.read(dataLength)

      data.strip()

      # convert from json
      y = json.loads(data)
      response = y
      if "email" in y:
          a = y["email"]
          b = y["password"]
          print(a)
          print(b)
      #user = sesion.quary(User).filter(User.Email==  %('um')s, {'unm': a})

      l1 = input(a)
      l2 = input(b)

      if user=q qsesion.quary(User).filter(User.Email== l1).True:
       print(user)



      print(data)

      response = ""+data+l1
      self.send_dict_response(response)
    if self.path.endswith("login"):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        dataLength = int(self.headers["Content-Length"])
        data = self.rfile.read(dataLength)

        data.strip()

        # convert from json
        y = json.loads(data)
        response = y
        if "email" in y:
            a = y["email"]
            b = y["password"]
            print(a)
            print(b)

        print(data)

        response = {}
        response["status"] = "OK"
        self.send_dict_response(response)


print("Starting server")
httpd = HTTPServer(("127.0.0.1", 8000), RequestHandler)
print("Hosting server on port 8000")
httpd.serve_forever()