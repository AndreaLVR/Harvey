# -*- coding: utf-8 -*- 
from header import *

def wp_joomla_checkIntro(url):
	myurl = url
	if("http" not in url):
		url = "http://%s" %url
	t = 0
	for x in range(0,len(url)):
		if(url[x] == '/'):
			t += 1
	if(t == 2 and chk_fileformat(url)):
		myurl = "%s/" %url

	return url


def check_joomla(url):
	rand = randint(0,9)
	headers = {'User-Agent':agents[rand%len(agents)]}
	tmp = ""
	n = 2
	t = 0
	url = wp_joomla_checkIntro(url)

	for x in range(0,len(url)):
		if(url[x] == '/'):
			t += 1
		tmp += url[x]
		test = ""
		if(t > n and url[x] == '/'):
			test = "%sadministrator" %tmp
			print "[*] Checking '%s'" %test

			try:
				r = requests.get(test, timeout=7, headers=headers)
				res = r.text
				ofile = codecs.open('out.html','w+',encoding='utf-8')
				ofile.write(res)
				ofile.close()
				# and "<a href=\"http://www.joomla.org\"" in res
				joomla_keystr = "<meta name=\"generator\" content=\"Joomla!"
				if(r.status_code == 200 and (joomla_keystr in res or "Joomla!" in res or "joomla.png" in res) and "username" in res and "password" in res):
					# look for v 1.5
					strchk = "- Open Source Content Management"
					jchk = """content="Joomla!"""
					ind = 0
					ok = True
					ver = ""
					stop = False
					if(strchk in res and jchk in res):
						z = 0
						for k in range(0,len(res)-(len(jchk)+len(strchk))):
							if(stop is True):
								break
							ok = True
							l = k
							for z in range(0,len(jchk)):
								if(res[l] != jchk[z]):
									ok = False
								l += 1
							if(ok): 
								j = l+1
								while(isNumberOrPoint(res[j])):
									ver += res[j]
									j += 1
								j += 1
								ok1 = True
								for f in range(0,len(strchk)):
									if(res[j] != strchk[f]):
										ok1 = False
										break
									j += 1
								if(ok1):
									stop = True
									myPrint("\n[Joomla!] %s   (v %s)\n" %(tmp,ver), "green")
					if(stop is False):
						myPrint("\n[Joomla!] %s\n" %tmp, "green")
					return
			except Exception as e:
				pass


def wordpress_version(url, headers):
	myurl = "%sreadme.html" %url
	print myurl
	is_wordpress = False
	version = ""

	try:
		r = requests.get(myurl, timeout=7, headers=headers)
		resp = r.text

		if(r.status_code == 200 and ("<title>WordPress" in resp and "ReadMe</title>" in resp)):
			is_wordpress = True
			if("Version" in resp):
				for x in range(0,len(resp)-7):
					if(resp[x] == 'V' and resp[x+1] == 'e' and resp[x+2] == 'r' and resp[x+3] == 's' and resp[x+4] == 'i' and resp[x+5] == 'o' 
						and resp[x+6] == 'n'):
						k = x+8
						break

				version = ""
				for x in range(k,len(resp)):
					if(isNumberOrPoint(resp[x]) is False):
						break
					version = version + resp[x]
	except:
		pass

	return is_wordpress,version


def check_wordpress(url):
	wp_checked = []
	rand = randint(0,9)
	headers = {'User-Agent':agents[rand%len(agents)]}
	tmp = ""
	n = 2
	t = 0
	url = wp_joomla_checkIntro(url)

	for x in range(0,len(url)):
		if(url[x] == '/'):
			t += 1
		tmp += url[x]
		test = ""

		if(t > n and url[x] == '/'):
			is_wordpress,ver = wordpress_version(tmp,headers)
			if(is_wordpress):
				if(len(ver) > 0):
					myPrint("\n[Wordpress] %s 	(v %s)" %(tmp,ver), "green")
					return
				else:
					myPrint("\n[Wordpress] %s" %tmp, "green")
					return

			test = "%swp-login.php" %tmp
			if(test not in wp_checked):
				wp_checked.append(test)
				try:
					r = requests.get(test, timeout=7, headers=headers)
					if(r.status_code == 200 and "/wp-admin" in r.text and "wordpress.org" in r.text and "loginform" in r.text 
					and "wp-login.php?action=lostpassword" in r.text):
						myPrint("\n[Wordpress] %s" %tmp, "green")
						return
				except:
					pass 


				