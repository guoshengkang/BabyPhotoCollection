#process the downloaded urls in photourls_two.txt and save to GoodUrls_two.txt
#the resulted urls have the format as: https://www.flickr.com/photos/draupp/albums
url_file=open('G:\\PythonCode\\photourls_two.txt','r')
lines=url_file.readlines()
url_file.close()
urls=[x.strip('\n') for x in lines]
print 'there are %d original urls!!!'%len(urls)

GoodFamilyUrls_file=open('G:\\PythonCode\\GoodUrls_two.txt','w')
names=[]
for url in urls: # https://www.flickr.com/photos/35832724@N02/albums/72157619330123564/
	split_url=url.split('/') #['https:', '', 'www.flickr.com', 'photos', '35832724@N02', 'albums', '72157619330123564', '']
	if url.startswith('https://www.flickr.com/photos/') \
	and 'tags' not in split_url \
	and split_url[4] not in names \
	and 'collections' not in split_url:
		names.append(split_url[4]) 
		newUrl='/'.join(split_url[:5]+['albums'])
		GoodFamilyUrls_file.write(newUrl+'\n')
		print newUrl
GoodFamilyUrls_file.close()