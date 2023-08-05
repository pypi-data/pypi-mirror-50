#!/usr/bin/env python3
# v2019.08.01

import os
import platform
import datetime
import random
import hashlib
import base64

debug=False

def gen():
	# datos
	dt = datetime.datetime.utcnow()
	fulltime="%.9f"%dt.timestamp()
	randbyte = random.randint(0,255)
	hostname = platform.node()
	domainname = os.environ.get('userdomain') # solo windows
	if domainname == None: domainname=hostname

	# debug, debe de dar FVS5IKAR3NOMXL33
	#fulltime="1564639517.744651687"
	#randbyte=123
	#domainname="alien"
	#hostname="alien"

	if debug: print("data "+domainname+" "+hostname+" "+fulltime+" "+str(randbyte))

	# 1.5 bytes hid
	hidstr=(domainname+"/"+hostname).upper()
	hidhex = hashlib.sha1(hidstr.encode('utf-8')).hexdigest()[:3].upper()
	if debug: print("hid  "+hidhex+"      "+hidstr)

	# 4 bytes unixtime
	unixtime=int(fulltime[0:10])
	htime=dt.strftime("%Y-%m-%d %H:%M:%S UTC")
	sechex=str.format('{:08X}', unixtime)
	if debug: print("time "+sechex+" "+str(unixtime)+" "+htime)

	# 2.5 bytes msec
	msec=int(fulltime[11:17])
	msechex = str.format('{:05X}', msec)
	if debug: print("msec "+msechex+"    "+str(msec))

	# 1 byte nanosec
	ns=int(fulltime[17:20])
	nanobyte=int(ns*256/1000)
	nanohex = str.format('{:02X}', nanobyte)
	if debug: print("nano "+nanohex+"       "+str(nanobyte))

	# 1 byte rand
	randhex = str.format('{:02X}',randbyte)
	if debug: print("rand "+randhex+"       "+str(randbyte))

	hexstr = hidhex+sechex+msechex+nanohex+randhex
	if debug: print("hex  "+hexstr)
	muidnum = bytearray.fromhex(hexstr)
	muid = base64.b32encode(muidnum).decode('utf-8')
	if debug: print(muid)
	return muid

if(__name__=="__main__"):
	#debug=True
	print(gen())
