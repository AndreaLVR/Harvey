from header import *
import whois
from ipwhois import IPWhois


def clean_print_info(info):
	# TODO
	print info


def domain_whois(domain):
	info = whois.query(domain)
	clean_print_info(str(info.__dict__))
	return info


