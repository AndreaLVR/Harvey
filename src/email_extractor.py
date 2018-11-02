from header import *


def email_ctrl(email,email_filters,logic_operator):
	if(email_filters is None or len(email_filters) == 0):
		return True

	filters_num = len(email_filters)

	if(logic_operator == "OR"):
		for x in range(0,filters_num):
			if(email_filters[x] in email):
				return True
		return False
	elif(logic_operator == "AND"):
		for x in range(0,filters_num):	
			if(email_filters[x] not in email):
				return False
	else: # NOT case
		for x in range(0,filters_num):
			if(email_filters[x] in email):
				return False
	return True 


def enumMails(url,email_filters,logic_operator):
	emails = []

	if("http" not in url):
		url = "http://%s" %url

	if(chk_fileformat(url)):
		rand = randint(0,9)
		headers = {'User-Agent':agents[rand%len(agents)]}
		r = requests.get(url,headers=headers)
		maildata = r.text
		maildata.replace('\n','')
		print "[*] Searching e-mail addresses in '%s'" %url

		if("@" in maildata or "%40" in maildata or "mailto:" in maildata):
			ofile = codecs.open('out.html','w+',encoding='utf-8')
			ofile.write(maildata)
			ofile.close()

			for x in range(0,len(maildata)):
				s1 = ""
				s2 = ""
				if(maildata[x] == '@' and x > 0 and x < len(maildata)-1):
					k = x-1
					while(x >= 0 and maildata[k] not in notvalid):
						s1 += maildata[k]
						k = k-1
					k = x+1
					while(k <= len(maildata)-1 and maildata[k] not in notvalid):
						s2 += maildata[k]
						k = k+1
					s3 = s1[::-1]+"@"+s2
					try:
						s3 = s3.encode("ascii","ignore")
						if(email_ctrl(s3,email_filters,logic_operator) and s3 not in emails and "." in s2):
							emails.append(s3)	
					except:
						pass

					if(s3 not in emails and "." in s2 and email_ctrl(s3,email_filters,logic_operator)):
						emails.append(s3)

					if(x < len(maildata)-3 and maildata[x] == '%' and maildata[x+1] == '4' and maildata[x+2] == '0'):
						s1 = ""
						s2 = ""
						k = w-1
						while(k >= 0 and maildata[k] not in notvalid):
							s1 += maildata[k]
							k = k-1
						k = x+1
						while(k <= len(maildata)-1 and maildata[k] not in notvalid):
							s2 += maildata[k]
							k = k+1		
						s3 = s1[::-1]+"@"+s2
						try:
							s3 = s3.encode("ascii","ignore")
							if(email_ctrl(s3,email_filters,logic_operator) and s3 not in emails and "." in s2):
								emails.append(s3)
						except:
							pass

	return emails


def cleanEmailAddresses(found_email_addresses,final_email_addresses):
    for x in range(0, len(found_email_addresses)):
        if("%" in found_email_addresses[x]):
        	try:
        		s = urllib.unquote(found_email_addresses[x]).decode('utf8')
        	except:
        		s = found_email_addresses[x]	
        else:
        	s = found_email_addresses[x]

        if(s[len(s)-1] == '.' or s[len(s)-1] == ',' or s[len(s)-1] in notvalid):
        	s = s[:-1]
        if(s[0] != '@' and s[len(s)-1] != '@' and s not in final_email_addresses):
            final_email_addresses.append(s)


def get_email_addresses_within_page(url,email_filters,logic_operator):
	print colored("\n[*] Looking for email addresses within '%s'" %url,"white")
	found_email_addresses = []
	final_email_addresses = []
	found_email_addresses = enumMails(url,email_filters,logic_operator)
	cleanEmailAddresses(found_email_addresses,final_email_addresses)

	myPrint("\n[+] Found %s e-mail address at '%s':" %(len(final_email_addresses),url), "red")
	for x in range(0, len(final_email_addresses)):
		myPrint(final_email_addresses[x],None) 
	print ""

