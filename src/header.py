# -*- coding: utf-8 -*- 
import socket
import time
import urllib2
import urllib
import sys
import requests
import codecs
import os
import threading
from termcolor import colored
from random import randint

numpages = 10
log_file = open("harvey_rev.log","w+")
allowed_web_extensions = [".html",".xml",".php",".txt",".config",".cfm",".cfml",".cfc",".css",".xhtml",".asp",".aspx",".sql",".psql",".cfg",".jsp"]
notvalid = [' ','<','>','{','}','[',']','(',')',';',':','"','\n','\r','\t','&','\'','\\','/','?','=']
agents   = ["Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
		    "IBM WebExplorer /v0.94","Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13",
		    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"]


def myPrint(s,color):
	global log_file

	s1 = "%s\n" %s
	log_file.write(s1)

	if(color == None):
		print s 
	else:
		print colored(s, color)


def isNumberOrPoint(n):
	if(n == "1" or n == "2" or n == "3" or n == "4" or n == "5" or n == "6" or n == "7" or n == "8" or n == "9" or n == "0" or n == "."):
		return True
	return False


def chk_fileformat(s):
	n = 0

	for x in range(0,len(s)):
		if(s[x] == '/'):
			n += 1

	if("." in s[-7:] and n >= 3):
		s = s[-7:]
		for k in range(0,len(s)):
			ind = 0
			if(s[k] == '.'):
				ind = k
		for z in range(ind,len(s)):
			if(s[z] == '/'):
				return True
		for x in range(0,len(allowed_web_extensions)):
			t = allow[x]
			if(t in s[(-len(t)):]):
  				return True

		print "[ERROR] chk_fileformat not passed."
		return False
	else:
		return True