# imports
import tweetstream
import os
import pycurl

class PyDFTribute :
	def __init__(self, username, password, filters) :
		# self.ext = Extractor()
		self.filters = filters
		self.username = username
		self.password = password

		self.has_full_link = False
		self.full_link = None

	def begin(self) :		
		stream = tweetstream.FilterStream(self.username, self.password, None, None, self.filters)

		for tweet in stream :			
			if tweet.has_key('entities') :
				entities = tweet['entities']

				if entities.has_key('urls') :
					urls = entities['urls']

					self.handle_urls(urls)

	def handle_urls(self, urls) :
		for url in urls :
			full_url = url['expanded_url']
			
			# reset state
			self.has_full_link = False
			self.full_link = None

			try :
				if full_url.endswith('.pdf') or full_url.endswith('.PDF') :
					self.storeLink(full_url)
				elif self.getFullLink(full_url) :
					self.storeLink(self.full_link)				
			except :
				print 'Exception encountered'
				continue

	def getFullLink(self, url) :
		conn = pycurl.Curl()
		conn.setopt(pycurl.URL, str(url))
		conn.setopt(pycurl.CUSTOMREQUEST, 'HEAD')
		conn.setopt(pycurl.NOBODY, True)
		conn.setopt(pycurl.HEADERFUNCTION, self.handle_headers)

		try :
			conn.perform()
		finally :
			conn.close()
		return self.has_full_link
	
	def storeLink(self, url) :
		# replace with code to insert into a storage layer
		print 'Found PDF: ' + url
		self.download_file(url)

	def download_file(self, url) :
		print 'Downloading ' + str(url)
		os.system("wget -P downloads/ " + str(url))

	def handle_headers(self, buf) :
		if buf.startswith('Location:') :			
			if ".pdf" in buf or ".PDF" in buf :
				self.has_full_link = True
				self.full_link = buf.replace("Location:", "").strip()

twitter = {
	'username' : 'username',
	'password' : 'password',
	'filters' : ['#pdftribute']
}

# entry point
if __name__ == "__main__" :
	pydf = PyDFTribute(twitter['username'], twitter['password'], twitter['filters'])
	pydf.begin()