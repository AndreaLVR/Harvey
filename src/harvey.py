# -*- coding: utf-8 -*-
from header import *
from email_extractor import get_email_addresses_within_page
from domains_retriever import get_subdomains, get_samehost_domains
from webplatforms_analyzer import check_joomla, check_wordpress
from webvulns_analyzer import check_sql_vuln, check_lfi_vuln
from multithread_crawl import multithread_crawl
from whois_info import domain_whois

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)
    print ""


def banner():
	ban = """\n                                                                                                                                       
               i8Zk   NGE      70q:  .Gkq0Gq5i  MZ8i   .OEB .X52kkq0u  M8Z    F0M.                                                                    
               FB@B   B@B      @@@B  iB@B@B@B@B B@@@   ZB@B i@B@@@B@@r7@@@.   B@B                                                                     
               L@B@   @@@     PB@@@: ,@@@   @B@  B@B   B@Bv :@@B       v@BM  v@@k                                                                     
               YB@M   B@B     B@G@B@ .B@B   7@B: @B@j .@B@  :@BB        B@B. @B@                                                                      
               7@B@B@B@B@    P@B v@B. @B@.iS@B@  v@8F iB@E  iB@@@B@B,    B@BMB@                                                                       
                B@@@@@B@M:i. @B@  B@M:Z@B@B@Bq;   @@L M@Br .v@B@BEO@.    .B@BS                                                                        
                @BB   @@@  :@B@O..@B@MGBL 7B@B@   MBM @B@:  .B@Bv         @BX2:                                                                       
                @@B   @@B   B@B@B@B@BBB@,  NB@B   ,@B@B@@    @B@:         B@@X                                                                        
                @B@   @B@  P@Ni   2B@Z@@G   @BBi   B@B@B,    B@B@8B@U     @B@E                                                                        
                B@@   B@B j@B     2@BMB@B   B@@S   iB@B@     @@@B@B@j     S@BG        v1.0\n"""

	print colored(ban, "white")
	features = color.RED + "\n\t              |M|u|l|t|i|-|f|u|n|c|t|i|o|n|s| |H|a|r|v|e|s|t|e|r|    \n\n" + color.END
	#features = "\n\t                     -|   Multi-functions Harvester   |-\n\n"
	print features
	#author = "               i8Zk   NGE      70q:  .Gkq0Gq5i  MZ8i   .OEB .X52kkq0u  M8Z    F0M."
	sys.stdout.write("\t\t\t\t ")
	author = color.CYAN + "Developed by Andrea Olivari" + color.END
	delay_print(author)
	sys.stdout.write("\n\t\t     ")
	author = color.YELLOW + "olivariandrea91[at]gmail.com | github.com/AndreaLVR" + color.END
	delay_print(author)
	print ""


def show_menu():
	print """
		      ╔═══════════════════════════════════════════════╗
		      ║  Menu                                         ║
		      ║═══════════════════════════════════════════════║
		      ║  1- Crawl website (3 filters available)       ║
		      ║	 2- Find websites located in the same server  ║
		      ║  3- Find subdomains                           ║                      
		      ║  4- Extract email addresses from URL          ║
		      ║  5- Check for Wordpress                       ║
		      ║  6- Check for SQL vuln                        ║
		      ║  7- Check for LFI vuln                        ║
		      ║                                               ║
		      ║  8- Exit                                      ║
		      ╚═══════════════════════════════════════════════╝
	"""


def set_choice(choice):
	if(choice == "1"):
		# Crawling
		print color.UNDERLINE + color.PURPLE + "\n\n ---+ CRAWLING +--- \n\n" + color.END
	elif(choice == "2"):
		print color.UNDERLINE + color.PURPLE + "\n\n ---+ SAME SERVER WEBSITES FINDER +--- \n\n" + color.END
	elif(choice == "3"):
		print color.UNDERLINE + color.PURPLE + "\n\n ---+ SUBDOMAINS FINDER +--- \n\n" + color.END
	elif(choice == "4"):
		print color.UNDERLINE + color.PURPLE + "\n\n ---+ WEBPAGE EMAILS EXTRACTOR +--- \n\n" + color.END
	elif(choice == "5"):
		print color.UNDERLINE + color.PURPLE + "\n\n ---+ WORDPRESS CHECK +--- \n\n" + color.END
	elif(choice == "6"):
		print color.UNDERLINE + color.PURPLE + "\n\n ---+ SQL VULNERABILITY SCANNER +--- \n\n" + color.END
	elif(choice == "7"):
		print color.UNDERLINE + color.PURPLE + "\n\n ---+ LFI SCANNER +--- \n\n" + color.END
	elif(choice == "8"):
		print "\nBye :)\n"
		sys.exit(0)
	else:
		print "boh"



banner()
show_menu()
choice = raw_input(" -> ")
set_choice(choice)




#domain = sys.argv[1]
#get_samehost_domains(domain)
#get_subdomains(domain,"bing",15)
#get_email_addresses_within_page(domain,[""],"OR")
#check_joomla(domain)
#check_wordpress(domain)'''
#check_sql_vuln(domain)
#check_lfi_vuln(domain)
#multithread_crawl(domain)
#domain_whois("www.tutorialspoint.com")


