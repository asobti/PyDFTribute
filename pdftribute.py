import tweetstream
import os
import pycurl

stream = tweetstream.FilterStream("username", "password", None, None, ["#pdftribute"])

class Extractor:
	def __init__(self) :
		# does the full link contain a pdf?
		self.full_link = False

	def handle(self, buf) :
		if buf.startswith('Location:') :
			# print 'Expanding link'
			if ".pdf" in buf or ".PDF" in buf :
				self.full_link = True
				print 'Found pdf in expanded link ' + buf				

def getFullLink(url) :

	ext = Extractor()

	conn = pycurl.Curl()
	conn.setopt(pycurl.URL, str(url))
	conn.setopt(pycurl.CUSTOMREQUEST, 'HEAD')
	conn.setopt(pycurl.NOBODY, True)
	conn.setopt(pycurl.HEADERFUNCTION, ext.handle)

	try :
		conn.perform()		
	finally :
		conn.close()

	return ext.full_link

for tweet in stream :
	if tweet.has_key('entities') :
		entities = tweet['entities']

		if entities.has_key('urls') :
			urls = entities['urls']

			for url in urls :
				try :
					# if either the link contains a pdf or it's expanded version does, download (wget will follow a 301 or 302 redirect)
					if url['expanded_url'].endswith('.pdf') or url['expanded_url'].endswith('.PDF') or getFullLink(url['expanded_url']) :
						print 'Downloading ' + url['expanded_url']
						os.system("wget -P downloads/ " + url['expanded_url'])
					else :
						print 'Skipping ' + url['expanded_url']
				except :
					continue




