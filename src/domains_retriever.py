from header import *

def googlePrint():
	print "[+] Using Google search engine.\t\t"
	time.sleep(0.5)


def bingPrint():
	print "[+] Using Bing search engine.\t\t"
	time.sleep(0.5)


def bing_dork(bstring,bpages):
	bdata = ""
	bn = 1
	x = 1
	bfile = codecs.open('out.html', 'w+', encoding='utf-8')
	print ""

	while(bn < int(bpages)*10):
		burl = "https://www.bing.com/search?q=%s&first=%s" %(bstring,bn)
		rand = randint(0,9)
		headers = {'User-Agent':agents[rand%len(agents)]}
		r = requests.get(burl)
		b = "Bing request - %s/%s ==> %s" %(x,bpages,r.status_code)
		print colored("%s" %b, 'white')
		sys.stdout.write("\033[F")
		bdata += r.text
		x = x+1
		bn += 10
		bfile.write(bdata)

	bfile.close()
	return bdata


def bingextract(s,urls):
	tmp = ""
	sl = 0

	for i in range(0,len(s)-8):
		sl = 0
		if((s[i] == 'h' and s[i+1] == 't' and s[i+2] == 't' and s[i+3] == 'p' and s[i+4] == ':' and s[i+5] == '/'
			and s[i+6] == '/') or (s[i] == 'h' and s[i+1] == 't' and s[i+2] == 't' and s[i+3] == 'p' and s[i+4] == 's' and s[i+5] == ':'
			and s[i+6] == '/' and s[i+7] == '/')):
			while(sl < 3):
				if(s[i] == '%' or s[i] == '<' or s[i] == '>' or s[i] == '"' or s[i] == '\'' or s[i] == ';' or s[i] == '{' or s[i] == '}'):
					break
				if(s[i] == '/'):
					sl = sl+1
				if(sl < 3):
					tmp += s[i]
					i += 1
			urls.append(tmp)
			tmp = ""
			sl = 0


def clean_urls(urls):
	for x in range(0,len(urls)):
		if("?http://" in urls[x] or "?https://" in urls[x]):
			tmp = ""
			copy = False
			for j in range(0, len(urls[x])):
				if(copy):
					tmp += (urls[x])[j]
				if(j < len(urls[x])-2 and (urls[x])[j] == '?' and (urls[x])[j+1] == 'h' and (urls[x])[j+2] == 't'):
					copy = True
			urls[x] = tmp
		elif("/http://" in urls[x] or "/https://" in urls[x]):
			tmp = ""
			copy = False
			for j in range(0, len(urls[x])):
				if(copy):
					tmp += (urls[x])[j]
				if(j < len(urls[x])-2 and (urls[x])[j] == '/' and (urls[x])[j+1] == 'h' and (urls[x])[j+2] == 't'):
					copy = True
			urls[x] = tmp

	breakpoint = 0
	for x in range(0,len(urls)):
		tmp = ""
		n = 0
		if("/" in urls[x]):
			if("http://" in urls[x] or "https://" in urls[x]):
				breakpoint = 3
			else:
				breakpoint = 1
			for j in range(0, len(urls[x])):
				if((urls[x]))[j] == '/':
					n = n+1
				if(n == breakpoint):
					break
				else:
					tmp += (urls[x])[j]	
			urls[x] = tmp


def splitHttp(url):
	tmp = ""
	start = False
	n = 0
	if("http://" in url or "https://" in url):
		for x in range(0,len(url)):
			if(start):
				tmp += url[x]
			if(url[x] == '/'):
				n += 1
			if(n == 2):
				start = True
	else:
		tmp = url

	return tmp


def bing_unique(urls,final):
	ips = []

	for x in range(0,len(urls)):
		if(urls[x] not in final and ("http://"+urls[x]) not in final and ("https://"+urls[x] not in final) and splitHttp(urls[x]) not in final):
			final.append(urls[x])
			if("http://" in urls[x]):
				host = (urls[x])[7:]
			elif("https://" in urls[x]):
				host = (urls[x])[8:]
			else:
				host = urls[x]
			try:
				ip = socket.gethostbyname(host)
			except:
				ip = "unknown"

			ips.append(ip)

	return ips


def generic_unique(web,urls,final,ips): # unique
	for x in range(0,len(urls)):
		if(urls[x] not in final and ("."+web) in urls[x] and ("http://"+urls[x]) not in final and ("https://"+urls[x] not in final) and splitHttp(urls[x]) not in final):
			final.append(urls[x])
			if("http://" in urls[x]):
				host = (urls[x])[7:]
			elif("https://" in urls[x]):
				host = (urls[x])[8:]
			else:
				host = urls[x]
			try:
				ip = socket.gethostbyname(host)
			except:
				ip = "unknown"

			ips.append(ip)


def get_samehost_domains(domain):
	urls  = []
	final = []	

	bingPrint()
	ip   = socket.gethostbyname(domain)
	init = "[+] %s has IP address %s" %(domain,ip)
	myPrint("\n%s" %init, "yellow")
	origweb = domain
	web = domain
	web = web[::-1]
	domain = "ip:%s" %ip
	bdata  = bing_dork(domain,numpages)
	bdata  = bdata.replace('\n','')
	bingextract(bdata,urls)
	clean_urls(urls)
	ips = bing_unique(urls,final)

	bdata = ""; np = 0; c = 0

	for x in range(0,len(web)):
		if(np == 2):
			break
		else:
			if(web[x] == '.'):
				np += 1
			c += 1

	web = (web[:c])[::-1]
	if(web[0] == '.'):
		web = web[1:]

	time.sleep(2)
	bdata = bing_dork(web,numpages)
	bdata = bdata.replace('\n','')
	bingextract(bdata,urls)
	clean_urls(urls)
	generic_unique(web,urls,final,ips)

	sameip = []
	for x in range(0,len(ips)):
		if(ips[x] == ip):
			sameip.append(final[x])

	found_string = "\n\n[+] Found %s websites" %len(sameip)
	if not(origweb[0] == 'w' and origweb[1] == 'w' and origweb[2] == 'w'):
		found_string += ", in addition to '%s'," %origweb

	found_string += " located into %s:\n" %ip
	myPrint("%s" %found_string, "red")

	for x in range(0,len(sameip)):
		print sameip[x]
	print ""


def google_dork(string,pages):
	max_retries = 10
	data = ""
	counter = 0
	ofile = codecs.open('out.html', 'w+', encoding='utf-8')
	error = False
	x = 1
	l = 0

	while(error is False and counter < int(pages)*10):
		url = "https://www.google.it/search?q=%s&start=%s" %(string,counter)
		rand = randint(0,9)
		headers = {'User-Agent':agents[rand%len(agents)]}

		try:
			r = requests.get(url,timeout=8)
			l += 1
			b = "Google request - %s/%s ==> %s" %(x,pages,r.status_code)
			print colored("%s" %b, 'green')
			sys.stdout.write("\033[F")

			if(r.status_code != 200):
				error = True
				print colored("[WARNING] Google is blocking our requests.","green")
				time.sleep(1.3)
			else:	
				counter += 10
				x += 1
				data += r.text
				ofile.write(r.text)
		except:
			error = True

	if(counter < int(pages)*10):
		go = True
		retry = 0

		while(counter < int(pages)*10 and go):
			rand = randint(0,9)
			url  = "https://www.google.com/search?q=%s&start=%s" %(string,counter)
			headers = {'User-Agent':agents[rand%len(agents)]}

			try:
				r = requests.get(url,timeout=15)
				l += 1
				b = "Google request - %s/%s ==> %s" %(x,pages,r.status_code)
				print colored("%s" %b, 'green')
				sys.stdout.write("\033[F")

				if(r.status_code != 200):
					if(retry == max_retries):
						print colored("[TIMEOUT] Google keeps on blocking us. Aborting.","red")
						time.sleep(1)
						break

					out = "[WARNING] Google keeps on blocking us. Waiting a few seconds.." %(retry+1)
					print colored(out,"yellow")
					sys.stdout.write("\033[F")
					time.sleep(5)
					retry += 1
				else:
					counter += 10
					if(counter >= int(pages)*10):
						print "\n"

					x += 1
					data += r.text
					ofile.write(r.text)
			except:
				print colored("[ERROR] Google keeps on blocking us. Aborting.",'red')
				break

	ofile.close()
	return data


def google_extract(s,urls):
	tmp = ""
	for i in range(0,len(s)-6):
		if(s[i] == '<' and s[i+1] == 'c' and s[i+2] == 'i' and s[i+3] == 't' and s[i+4] == 'e' and s[i+5] == '>'):
			i = i+6
			while(s[i] != '<'):
				tmp += s[i]
				i += 1
			if tmp not in urls:
				urls.append(tmp)
			tmp = ""


def get_subdomains(url,engine,max_browser_pages):
	urls   = []
	final  = []
	ips    = []
	data   = ""
	domain = "site:\""+url+"\""

  	if(engine == "google" or engine == "union"):
  		googlePrint()
		google_dork(domain,max_browser_pages)
		data = data.replace('\n', '')
		google_extract(data,urls)

	if("\"" in domain):
		web = domain[6:]	
		web = web[:-1]
	else:
		web = domain[5:]

	if(engine == "bing" or engine == "union"):
		bingPrint()
		bdata = bing_dork(web,max_browser_pages)
		bdata = bdata.replace('\n','')
		bingextract(bdata,urls)

	clean_urls(urls)
	generic_unique(web,urls,final,ips)

	maxlen = 0
	for x in range(0,len(final)):
		if(maxlen == 0 or maxlen < len(final[x])):
			maxlen = len(final[x])

	found = "\n\n[+] Found %d subdomains of '%s': \n" %(len(final),web)
	myPrint(found,"red")

	for x in range(0,len(final)):
		sp = (maxlen+7)-len(final[x])
		s = "%s" %final[x]
		for i in range(0,sp):
			s = s+" "
		s = s+"%s" %ips[x]
		myPrint(s,None)

	print ""

