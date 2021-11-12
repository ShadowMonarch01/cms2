import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from json import dumps
import mysql.connector
from sqlalchemy import create_engine, MetaData,Table,Column,Integer,Boolean,String,TEXT,FLOAT
from sqlalchemy.orm import declarative_base,sessionmaker

mydb = mysql.connector.connect(host='sql4.freemysqlhosting.net',user='sql4450350',password='L1lMFEHWxj',database='sql4450350')

engine = create_engine("mysql+pymysql://sql4450350:L1lMFEHWxj@sql4.freemysqlhosting.net/sql4450350")

engine.connect()

meta = MetaData()

users = Table(
    'users', meta,
    Column('1d', Integer, primary_key= True),
    Column('Email', String(66), unique=True),
    Column('Password', String(20)),
    Column('Adm', Boolean, default=0),
    Column('FullName' ,String(200)),
    Column('DateOfBirth', String(20)),
    Column('Picture', String(20)),
    Column('SchoolStartYear', String(20)),
    Column('MajorFieldOfStudy', String(100)),
    Column('MinorFieldOfStudy', String(100)),
    Column('Courses', TEXT),
    Column('AdCourses',TEXT),
    Column('Average', FLOAT(8)),
    Column('Comments', TEXT),
    Column('Suspended', Boolean, default=0),
    Column('Remark', TEXT),
)
#meta.create_all(engine)
print(engine)

Session=sessionmaker()
myc = mydb.cursor(buffered=True)
#DO NOT RUN THIS LINE AGAIN THE DATABASE HAS BEEN CREATED EXCEPT YOU WANT TO CREATE ONE ON A NEW SERVER
#myc.execute('CREATE TABLE users(id INT AUTO_INCREMENT PRIMARY KEY, Email VARCHAR(66) UNIQUE, Password VARCHAR(20), Adm INT(1) DEFAULT 0, FullName VARCHAR(200), DateOfBirth VARCHAR(20), Picture VARCHAR(10), SchoolStartYear VARCHAR(50), MajorFieldOfStudy VARCHAR(100),MinorFieldOfStudy VARCHAR(100), Courses TEXT, AdCourses TEXT, Average FLOAT(8) , Comments TEXT, Suspended INT(1) DEFAULT 0, Remark TEXT)')


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
      response="WELCOME YOU DID NOT USE METHODS"
      self.send_dict_response(response)

  def do_POST(self):
      if self.path.endswith('/login'):
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

          myc.execute("SELECT * FROM users WHERE Email= %(unm)s", {'unm': a})

          for j in myc:
              print(j)

          mydb.commit()

          check = myc.execute("SELECT * FROM users WHERE Email= %(unm)s", {'unm': a})
          print(check)
          for i in myc:
              print(i)

              if i[2] == b:
                  k = "Password correct OK"
                  response = {}
                  response["status"] = f"{i[3]},{j},{k}"

                  res1 = {}
                  res1["Adm"] = f"{i[3]}"
                  res2 = {}
                  res2["Status"] = f"{k}"
                  res3 = {}
                  res3["Info"] = f"{j}"

                  el = [res1, res2, res3]

                  self.wfile.write(bytes(dumps(el), "utf8"))

                  check = True

                  # self.send_dict_response(response)

              else:
                  k = "Incorrect Password"
                  response = {}
                  response["status"] = f"{k}"

                  res4 = {}
                  res4["IncorrectPassword"] = f"{k}"

                  el2 = [res4]
                  self.wfile.write(bytes(dumps(el2), "utf8"))
                  check = True

          if not check:
              l = "Email Does not exist"
              response = {}
              response["status"] = f"{l}"

              res5 = {}
              res5["NoUserFound"] = f"{l}"

              el3 = [res5]
              self.wfile.write(bytes(dumps(el3), "utf8"))
              # self.send_dict_response(response)

          mydb.commit()

      if self.path.endswith('/register'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)
          response = y
          if "email" in y:
              a = y["email"]
              b = y["password"]

              print(a)
              print(b)

              # check = myc.execute("SELECT Email FROM users WHERE EMAIL= %(unm)s", {'unm':a})

              # new_user = users(email=a, password=b)

              ins = users.insert().values(Email=a, Password=b, FullName="")
              conn = engine.connect()
              conn.execute(ins)
              self.send_dict_response(response)

      if self.path.endswith('/admregister'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)
          response = y
          if "email" in y:
              a = y["email"]
              b = y["password"]
              c = y["Adm"]
              d = y["FullName"]
              e = y["DateOfBirth"]
              f = y["Picture"]
              g = y["SchoolStartYear"]
              h = y["MajorFieldOfStudy"]
              i = y["MinorFieldOfStudy"]
              j = ','.join(y["AdCourses"])
              k = y["Average"]
              l = y["Comments"]
              m = y["Remark"]
              #n = y["password"]
              print(a)
              print(b)
              print(j)

              # check = myc.execute("SELECT Email FROM users WHERE EMAIL= %(unm)s", {'unm':a})

              # new_user = users(email=a, password=b)

              ins = users.insert().values(Email=a, Password=b,Adm=bool(c), FullName=d,DateOfBirth=e,Picture=f,SchoolStartYear=g,MajorFieldOfStudy=h,MinorFieldOfStudy=i,AdCourses=j,Average=k,Comments=l,Remark=m)
              conn = engine.connect()
              conn.execute(ins)
      #self.send_dict_response(response)


print("Starting server")
httpd = HTTPServer(("127.0.0.1", 8000), RequestHandler)
print("Hosting server on port 8000")
httpd.serve_forever()