from header import *
from threading_support import Barrier

urls_index = 0
barrier = None
write_lock  = threading.Lock()
print_lock  = threading.Lock()
insert_lock = threading.Lock()
get_lock    = threading.Lock()
invalid_url_extensions = [".css",".png",".jpg",".mp4",".avi",".mp3",".mkv",".pdf",".txt",".xml",".js",".exe",".dmg",".bash",".sh",".bmp",".xls",".doc",
						  ".ppt",".bat",".m4a",".docx",".dll"]

def substr_find(resp,toFind,brk):
	if(len(toFind) > len(resp)):
		return []

	found = False
	indexes = []

	for x in range(0,(len(resp)-len(toFind))+1):
		if(ord(resp[x]) == ord(toFind[0])):
			found = True
			for i in range(0,len(toFind)):
				if(ord(resp[x+i]) != ord(toFind[i])):
					found = False
					break
		if(found):
			indexes.append(x)
			if(brk):
				break
			found = False
			x += len(toFind)

	return indexes


def extract_specific(content,after,stop):
	res = ""
	get = False

	for c in content:
		if c == stop and get:
			break
		if get and c != stop:
			res += c
		if c == after:
			get = True

	return res


def check_href(url,website):
	#print "controllo %s" %url
	if(len(url) == 0):
		return None

	invalid_str = ["javascript","mailto:"]
	
	for string in invalid_str:
		if(url[:len(string)] == string):
			return None

	valid_url = url
	if(url[:len("http")] != "http"):
		if(url[0] != "/"):
			url = "/"+url
		valid_url = website+url
	else:
		if(website not in url[:len(website)]):
			#print "Escludo %s" %url
			return None

	return valid_url.strip()


def insert_url(url,urls):
	insert_lock.acquire()
	if(url not in urls):
		urls.append(url)
	insert_lock.release()


def get_urls_index():
	global urls_index

	urls_index += 1
	return urls_index-1


def conc_print(s):
	print_lock.acquire()
	print "%s" %s
	print_lock.release()


def write_to_file(s,ofile):
	write_lock.acquire()
	ofile.write(s)
	write_lock.release()


def crawl(urls,website,ofile,barrier):
	while(urls_index < len(urls)):
		get_lock.acquire()
		url_index = get_urls_index()
		url = urls[url_index]
		get_lock.release()
		conc_print("[# %s] = %s" %(url_index+1,url))
		rand = randint(0,9)
		headers = {'User-Agent':agents[rand%len(agents)]}
		r = requests.get(url,headers=headers)

		#print r.status_code
		if(r.status_code == 200):
			resp = r.text
			#print resp
			href_indices = substr_find(resp,"href=\"",False)
			#print href_indices
			for href_index in href_indices:
				content = resp[(href_index+len("href=\"")-1):]
				href_url = extract_specific(content,"\"","\"")
				valid_url = check_href(href_url,website)
				#print "valid_url = %s" %valid_url
				if(valid_url is not None and valid_url not in urls):
					write_to_file(valid_url+"\n",ofile)
					to_insert = True
					for invalid_ext in invalid_url_extensions:
						if(valid_url[-len(invalid_ext):] == invalid_ext):
							to_insert = False
					if(to_insert and "/sitemap" not in valid_url):
						insert_url(valid_url,urls)
		
	print "un thread arriva alla barriera..."		
	barrier.wait()


def multithread_crawl(start_url):
	global urls_index
	global barrier

	barrier = Barrier(5) 
	ofile = codecs.open("output.txt","w",encoding="utf-8")
	if(start_url[:len("http")] != "http"):
		start_url = "http://%s" %start_url
	start_url_split = start_url.split("/")
	website = start_url_split[0]+"//"+start_url_split[2]
	print "start_url = %s" %start_url
	print "website = %s" %website

	urls = [start_url]
	threads = []

	for i in range(0,4):
		try:
			thread = threading.Thread(target=crawl, args=(urls,website,ofile,barrier))
			threads.append(thread)
			thread.start()
			time.sleep(2)
		except Exception as e:
			print "Error: Unable to start thread\n%s" %e
			pass

	print "il thread principale arriva alla barriera..."
	barrier.wait()
	print "supero la barriera.."
	ofile.close()


#multithread_crawl("https://whatismyipaddress.com")





