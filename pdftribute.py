import tweetstream
import os
import pycurl

stream = tweetstream.FilterStream("username", "password", None, None, ["#pdftribute"])

class Extractor:
	def __init__(self) :
		# does the full link contain a pdf?
		self.has_full_link = False
		self.full_link = None

	def handle(self, buf) :
		if buf.startswith('Location:') :
			# print 'Expanding link'
			if ".pdf" in buf or ".PDF" in buf :
				self.has_full_link = True
				self.full_link = buf.replace("Location:", "").strip()

				#print 'Found pdf in expanded link ' + buf				

ext = Extractor()

def getFullLink(url) :
	ext.has_full_link = False
	ext.full_link = None
	
	conn = pycurl.Curl()
	conn.setopt(pycurl.URL, str(url))
	conn.setopt(pycurl.CUSTOMREQUEST, 'HEAD')
	conn.setopt(pycurl.NOBODY, True)
	conn.setopt(pycurl.HEADERFUNCTION, ext.handle)

	try :
		conn.perform()		
	finally :
		conn.close()

	return ext.has_full_link

def storeLink(url) :
	# replace with code to insert into a storage layer here
	print url

for tweet in stream :
	if tweet.has_key('entities') :
		entities = tweet['entities']

		if entities.has_key('urls') :
			urls = entities['urls']

			for url in urls :
				try :
					# if either the link contains a pdf or it's expanded version does, download (wget will follow a 301 or 302 redirect)
					if url['expanded_url'].endswith('.pdf') or url['expanded_url'].endswith('.PDF') :
						storeLink(url['expanded_url'])
					elif getFullLink(url['expanded_url']) :
						storeLink(ext.full_link)
				except :
					continue




