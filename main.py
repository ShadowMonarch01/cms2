import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from json import dumps
import mysql.connector
from sqlalchemy import create_engine, MetaData,Table,Column,Integer,Boolean,String,TEXT,FLOAT
from sqlalchemy.orm import declarative_base,sessionmaker


mydb = mysql.connector.connect(host='localhost',user='root',password='1234567890',database='backstress')

engine = create_engine("mysql+pymysql://root:1234567890@localhost/backstress")

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

      if self.path.endswith('/admsearch'):
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

          ob = ["id","Email","Password","Adm","FullName","DateOfBirth","Picture","SchoolStartYear","MajorFieldOfStudy","MinorFieldOfStudy","Courses","AdCourses","Average","Comments","Suspended","Remark"]
          counter = 0
          fndcount=[]

          if "search" in y:
              a = y["search"]

              t = str(a)

              query = "SELECT * FROM users WHERE FullName LIKE %s"
              name = ("%"+t+"%",)
              #name = ("%W%",)
              myc.execute(query, name)

              check= myc.fetchall()


              for res in check:

                  print(res)
                  sndcount = []
                  obj = {}
                  for pl in res:
                      obj[ob[counter]] = pl

                      counter = counter + 1


                  # sndcount.append({ob[counter]:pl})

                  fndcount.append(obj)
                  counter = 0

                  response = {}
                  response["userinfo"] = f"{fndcount}"
          self.wfile.write(bytes(dumps(response), "utf8"))

# UPDATING THE STUDENT PROFILE REQUIRES THE Email OF THE ADMIN THATS UPDATING THE STATUS AS(admemail) THEN ALL THE STUDENT INFO
# THE COURSES AND ADDITIONAL COURSES SHOULD BE IN ARRAY FORMAT

      if self.path.endswith('/updatestudentinfo'):
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

          if "admemail" in y:
              admcheck = y["admemail"]
              a = y["email"]
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
              n = y["id"]
              o = ','.join(y["Courses"])

              tid = int(n)

          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})


          check= myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')
                      myc.execute('UPDATE users SET Email = %s ,FullName = %s ,DateOfBirth = %s ,Picture = %s ,SchoolStartYear = %s ,MajorFieldOfStudy = %s ,MinorFieldOfStudy = %s,Courses=%s ,AdCourses = %s ,Average = %s ,Comments = %s ,Remark = %s WHERE id = %s ',(a,d, e, f, g,h,i,o,j,k,l,m,tid))
                      mydb.commit()
                  else:
                      print("Admin stats false")

          print(check)

 # STUDENT UPDATES HIS ADDITIONAL COURSES REQUIRES THE ADDITIONAL COURSES IN AN ARRAY AND HIS EMAIL
      if self.path.endswith('/updteadcourses'):
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

          if "adcourses" in y:
              courses = ','.join(y["AdCourses"])
              a = y["email"]

          myc.execute('UPDATE users SET AdCourses = %s WHERE Email = %s ',(courses,a))
          mydb.commit()

# SUSPENDING THE STUDENT REQUIRES THE ADMIN Email AS(admemail) THEN THE STUDENT EMAIL AND A STRING OF "1" OR "0" FOR THE BOOLIAN STATUS
      if self.path.endswith('/suspendstudent'):
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

          if "admemail" in y:
              admcheck = y["admemail"]
              a = y["email"]
              b = y["stats"]

              tid = int(b)

          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})

          check = myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')
                      myc.execute('UPDATE users SET Suspended = %s WHERE Email = %s ',(tid, a))
                      mydb.commit()
                  else:
                      print("Admin stats false")


# MAKING A NEW ADMIN REQUIRES THE ADMIN Email AS(admemail) THEN THE OTHER EMAIL AND A STRING OF "1" OR "0" FOR THE BOOLIAN STATUS
      if self.path.endswith('/mknewadmin'):
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

          if "admemail" in y:
              admcheck = y["admemail"]
              a = y["email"]
              b = y["stats"]

              tid = int(b)

          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})

          check = myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')
                      myc.execute('UPDATE users SET Adm = %s WHERE Email = %s ', (tid, a))
                      mydb.commit()
                  else:
                      print("Admin stats false")


#  RETURNS ALL USERS REQUIRES THE ADMIN EMAIL AS INPUT FOR VERIFICATION
      if self.path.endswith('/getalluser'):
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

          if "admemail" in y:
              admcheck = y["admemail"]


          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})

          check = myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')

                      ob = ["id", "Email", "Password", "Adm", "FullName", "DateOfBirth", "Picture", "SchoolStartYear",
                            "MajorFieldOfStudy", "MinorFieldOfStudy", "Courses", "AdCourses", "Average", "Comments",
                            "Suspended", "Remark"]
                      counter = 0
                      fndcount = []

                      myc.execute('SELECT * FROM users WHERE Adm = %s', (0,))

                      check = myc.fetchall()

                      for res in check:

                          print(res)
                          sndcount = []
                          obj = {}
                          for pl in res:
                              obj[ob[counter]] = pl

                              counter = counter + 1

                          # sndcount.append({ob[counter]:pl})

                          fndcount.append(obj)
                          counter = 0

                          response = {}
                          response["userinfo"] = f"{fndcount}"
                      self.wfile.write(bytes(dumps(response), "utf8"))
                  else:
                      print("Admin stats false")


# RETURNS THE STUDENTS INFO REQUIRES THE STUDENT EMAIL AS INPUT
      if self.path.endswith('/getstudentinfo'):
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

          if "email" in y:
              a = y["email"]

          myc.execute('SELECT * FROM users WHERE Email= %s', (a,))

          check = myc.fetchall()

          ob = ["id", "Email", "Password", "Adm", "FullName", "DateOfBirth", "Picture", "SchoolStartYear",
                "MajorFieldOfStudy", "MinorFieldOfStudy", "Courses", "AdCourses", "Average", "Comments",
                "Suspended", "Remark"]
          counter = 0
          fndcount = []



          for res in check:

              print(res)
              sndcount = []
              obj = {}
              for pl in res:
                  obj[ob[counter]] = pl

                  counter = counter + 1

              # sndcount.append({ob[counter]:pl})

              fndcount.append(obj)
              counter = 0

              response = {}
              response["userinfo"] = f"{fndcount}"
          self.wfile.write(bytes(dumps(response), "utf8"))








print("Starting server")
httpd = HTTPServer(("127.0.0.1", 8000), RequestHandler)
print("Hosting server on port 8000")
httpd.serve_forever()