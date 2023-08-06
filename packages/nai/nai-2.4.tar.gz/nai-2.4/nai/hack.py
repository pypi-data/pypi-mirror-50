from requests import *
from bs4 import *
from bs4 import BeautifulSoup as bs
from colours import *
import json

def phonesearch(numb):
   num = str(numb)
   if len(num) != 10:
    if "0" in num:
     num = num[1:]
    elif "+92" in num:
     num = num.split("+92")[1]
   url = "https://simdatabaseonline.com/tele/search.php?num={}"
   try:
     html = BeautifulSoup(get(url.format(num)).content,"html.parser")
     data = html.find("table")
     print(W+"-"*3+Y+"NEXDataBase-Records"+W+"-"*3)
     for x in data.find_all("tr"):
       try:
         print(G+x.get_text())
       except: pass
     print(W+"-"*10)
   except:
     if data != None:
      print(R+"ERROR : Network Error !")
     elif data == None:
      print(R+"ERROR : NOT FOUND !")



def capt(pt):
	if pt[1] == '+':
		return int(pt[0]) + int(pt[2])
	elif pt[1] == '-':
		return int(pt[0]) - int(pt[2])
	elif pt[1] == '*':
		return int(pt[0]) * int(pt[2])
	else:
		return int(pt[0]) / int(pt[2])



def roll(num):
    dx = {}
    s = Session();url = 'https://result.bisemdn.edu.pk'
    r = s.get(url+'/hssc/').text
    b = bs(r,'html.parser')
    token = b.find('input',{'name':'csrf-token'}).get('value')
    captcha = capt(b.find('input',{'name':'captcha'}).get('placeholder').split())
    data = {
	'std_rno':str(num), # roll number input
	'captcha':str(captcha), # captcha
	'csrf-token':token, # csrf token
	'pvt-login-submit':'Submit'
	}
	
	# send data
    r = s.post(url+'/incl/istd_login.php',data=data,timeout=10000).text
    if 'success' in r:
        r = s.get(url+'/hssc/student').text
        b = bs(r,'html.parser')
        table = b.find('table',{'id':'info-table'})
        for i in table.find_all('tr'):
            #print(i.find('th').text+' : '+i.find('td').text)
            dx[i.find('th').text] = i.find('td').text
    return dx


def jwrite(dic):
  with open('/sdcard/result.json','a') as jw:
    jw.write(json.dumps(dic)+'\n')

def simplewrite(dic):
  with open('/sdcard/result.text','a') as sw:
   for x in dic.keys():
     sw.write('{} : {} \n'.format(x,dic[x]))
   sw.write("\n------------------------------")