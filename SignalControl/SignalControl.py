from Mailer import SEND
from Mailer import RECEIVE
from WebReader import WebRead
#SEND('hi')
#print('RECEIVE IS: \n',RECEIVE())
WebRead()

import requests
USERNAME = "hohla@yandex.ru"
PASSWORD = "Hohla2010"

LOGINURL = 'https://skladchik.com/login/'
URL = 'https://skladchik.com/conversations/2o4Jv6Z1mZjt5WsTZmpMj8XpLecseBQ6nC4S2MddorqGMiHTHXnX1NcvHrPpuGFw37WzXdtpC.848928/page-5'



#######################################################################################################
s = requests.session()
#req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {'login': USERNAME,  'password': PASSWORD}

# Authenticate
r = s.post(URL, data=data)





print ("headers: ", r.headers)
print ("status:",   r.status_code)
print ("text: ",    r.text)
print ("ALL: ",r)

# Read data
r2 = session.get(DATAURL)
print ("___________DATA____________")
print (r2.headers)
print (r2.status_code)
print (r2.text)













