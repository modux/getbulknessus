#!/usr/bin/env python
# by Konrads Smelkovs <konrads.smelkovs@kpmg.co.uk>
# Licence - CC-BY, else do whatever you want with this

import cookielib, urllib2,json, time
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



url="http://localhost:8834"
login="user"
password = "pass"
scanfolder="My Scans"
SLEEP=2

data=json.dumps({'username': login, 'password':password})
request=urllib2.Request(url+"/session",data,{'Content-Type': 'application/json; charset=UTF-8',
											  })
# opener.open(request,context=ctx)
f=urllib2.urlopen(request,context=ctx)
token=json.loads(f.read())['token']

print "[D] Logged on, token is %s" % token

request=urllib2.Request(url+"/folders",headers={'X-Cookie': 'token=' + str(token)})
f=urllib2.urlopen(request,context=ctx)
folders=json.loads(f.read())
folderid=filter(lambda y: y['name']==scanfolder,folders['folders'])[0]['id']


scans_by_folder=urllib2.Request(url+"/scans?folder_id=%i" % folderid,headers={'X-Cookie': 'token=' + str(token)})
f=urllib2.urlopen(scans_by_folder,context=ctx)
scans=json.loads(f.read())["scans"]
print "[D] Got %i scans in folder %i" % (len(scans),folderid)

for s in scans:
	print "[D] Exporting %s" % s['name']
	data=json.dumps({'format': 'csv'})
	request=urllib2.Request(url+"/scans/%i/export" % s["id"],data,
		{'Content-Type': 'application/json', 
		'X-Cookie': 'token=' + str(token)})
	f=urllib2.urlopen(request,context=ctx)
	fileref=scans=json.loads(f.read())["file"]
	print "[D] Got export file reference %s" % fileref
	attempt=0
	while True:
		attempt+=1
		print "[D] Reqesting scan status for fileref %s, attempt %i" % (fileref,attempt)
		status_for_file=urllib2.Request(url+"/scans/%s/export/%s/status" % (s["id"],fileref)
			,headers={'X-Cookie': 'token=' + str(token)})
		f=urllib2.urlopen(status_for_file,context=ctx)
		status=json.loads(f.read())["status"]
		if status=="ready":
			download=urllib2.Request(url+"/scans/%s/export/%s/download?token=%s" % (s["id"],fileref,token),
				headers={'X-Cookie': 'token=' + str(token)})
			f=urllib2.urlopen(download,context=ctx)
			print "[D] Downloaded report for %s" % s["name"]
			with  open("%s.csv" % s["name"],"wb") as rep:
				rep.write(f.read())
			break
		else:
			print "[D] Sleeping for %i seconds..." % SLEEP
			time.sleep(SLEEP)




