#!/usr/bin/env python3
from gophish import Gophish
from gophish.models import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import sys,requests,json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


API_KEY = "ENTER API KEY HERE"
SERVER = "ENTER SERVER NAME OR IP HERE"
PORT = "3333"
GOPHISH_URL = "https://" + SERVER  + ":" + PORT

def connect_to_gophish(API_KEY,GOPHISH_URL):
	print("[+] Connecting...")
	api = Gophish(API_KEY,GOPHISH_URL, verify=False)
	rid = input("[?] Enter RID to report: ")
	lookup_rid(api,GOPHISH_URL,rid)

def lookup_rid(api,GOPHISH_URL,rid):
	print("[+] Locating the campaign for {0}...".format(rid))
	campaigns = api.campaigns.get()
	for campaign in campaigns:
		campaign_id = campaign.id
		current_campaign = api.campaigns.get(campaign_id=campaign_id)
		for result in current_campaign.results:
			if result.id == rid:
				print("[+] Found RID in Campaign #{0}...".format(campaign_id))
				url = current_campaign.url
				email = result.email
				report_phish(api,GOPHISH_URL,rid,url,email)

def report_phish(api,GOPHISH_URL,rid,url,email):
	report_url = url + "/report?rid=" + rid
	try:
		r = requests.get(report_url, verify=False)
		if r.status_code == 204:
			print("[+] {0} reported {1} as a phishing email!".format(email,rid))
	except:
		print("[!] Couldn't report {0}. Check the RID and URL.".format(rid))

connect_to_gophish(API_KEY,GOPHISH_URL)
