PyDFTribute
------------

A Python script that monitors #pdftribute on Twitter in realtime and downloads all .pdf files linked.

PDFs are downloaded to a the directory 'downloads'.

Replace 'username' and 'password', with your Twitter credentials.

Dependencies / Requirements
---------------------------

- anyjson (http://pypi.python.org/pypi/anyjson)
- tweetstream (http://pypi.python.org/pypi/tweetstream/)
- pycurl
- wget

To install AnyJSON and TweetStream, first install 'python-setuptools'

```
sudo apt-get install python-setuptools
```

Then, download the two packages and run

```
sudo python setup.py install
```

For pycurl, follow instructions from here: http://pycurl.sourceforge.net/
