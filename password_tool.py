import os,sys,secrets,sqlite3
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64 , pyperclip

scriptDir=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(scriptDir,"lib"))

def getkey(PIN):
  SaltFile=os.path.join(scriptDir,"salt.bin")
  if not os.path.exists(SaltFile):
    salt=secrets.token_bytes(16)
    with open(SaltFile,"wb") as f:f.write(salt)
  else:
    with open(SaltFile,"rb")as f:salt=f.read()
  Kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000)
  KEY=base64.urlsafe_b64encode(Kdf.derive(PIN.encode()))
  return KEY

def GenPass():
  chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
  passwd=""
  for i in range(64):passwd+=secrets.choice(chars)
  return passwd

def storePass(SERV,PASS,pin):
  key=getkey(pin)
  f=Fernet(key)
  encpass=f.encrypt(PASS.encode())
  db=os.path.join(scriptDir,"passwords.db")
  Conn=sqlite3.connect(db)
  CURSOR=Conn.cursor()
  CURSOR.execute("CREATE TABLE IF NOT EXISTS passwords (service TEXT PRIMARY KEY, password BLOB)")
  CURSOR.execute("INSERT OR REPLACE INTO passwords (service,password) VALUES (?,?)",(SERV,encpass))
  Conn.commit()
  Conn.close()

def getPass(service,pin):
  attemptsfile=os.path.join(scriptDir,"attempts.txt")
  if os.path.exists(attemptsfile):
    with open(attemptsfile,"r")as f:attempts=int(f.read())
    if attempts>=5:
      os.remove(os.path.join(scriptDir,"passwords.db"))
      os.remove(attemptsfile)
      return "too many tries wiped it all!"
  else:attempts=0
  KEY=getkey(pin)
  fernet=Fernet(KEY)
  DBpath=os.path.join(scriptDir,"passwords.db")
  conn=sqlite3.connect(DBpath)
  cursor=conn.cursor()
  cursor.execute("SELECT password FROM passwords WHERE service=?",(service,))
  Result=cursor.fetchone()
  conn.close()
  if Result:
    encPass=Result[0]
    try:
      return fernet.decrypt(encPass).decode()
    except:
      attempts+=1
      with open(attemptsfile,"w")as f:f.write(str(attempts))
      return "wrong pin or bad data!"
  return "service not found!"

def Main():
  while 1:
    print("\nusb password tool")
    print("1 generate n store passwd")
    print("2 get passwd")
    print("3 exit")
    Choice=input("pick: ")
    if Choice=="1":
      serv=input("service name (like gmail):")
      Pin=input("ur pin:")
      password=GenPass()
      storePass(serv,password,Pin)
      print("ur passwd:",password)
      pyperclip.copy(password)
      print("copied to clip!")
    elif Choice=="2":
      SERV=input("service name:")
      pin=input("ur pin:")
      Passwd=getPass(SERV,pin)
      print("passwd:",Passwd)
      if "wrong" not in Passwd and "not found" not in Passwd:
        pyperclip.copy(Passwd)
        print("copied to clip!")
    elif Choice=="3":break
    else:print("bad choice!")

if __name__=="__main__":
  Main()