 # Get the first 1000 hits by Google search and save the returned urls to .txt
from google import search
url_file=open('G:\\PythonCode\\photourls_two.txt','r')
keywords="'two years old' baby site:flickr.com"
for url in search(keywords, tld='es', lang='es', stop=500):
    url_file.write(url+'\n')