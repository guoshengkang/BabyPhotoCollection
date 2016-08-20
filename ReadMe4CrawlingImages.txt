This ReadMe file for BabyPhotoDataset includes the following files:
ReadMe.txt	
125 folders		Photos from 125 families
Accounts.txt		125 accounts from Flickr which corresponds to the 125 families
BabyPhotoUrls.txt	The URLs used for crawling. One URL corresponds an album of an account
Statistics.txt		Statistics for the number of files for each folder

This BabyPhotoDataset collects albums of 125 accounts from https://www.flickr.com/. Totally there are 6833 photos. Most of photos are about babies, also some adult photos are collected by group photos.

Collecting method:
Step1: Find the links related to baby in Flickr by google search engine, and save the links.
the used key words for Google search are as follows:
six months old baby site:flickr.com
one year old baby site:flickr.com
two year old baby site:flickr.com
four year old baby site:flickr.com
toddler year old baby site:flickr.com
Python API for Google search could be downloaded from: https://pypi.python.org/pypi/google

Step2: Find accounts from links and delete the repeated accounts.
For example, for link: https://www.flickr.com/photos/smileygoldfish/3037348974/in/album-72157606866526249/
We abstract the string "smileygoldfish" which corresponds an account. And then see whether it is a repeated one. If yes, delete the link, else save it.

Step3: Deal with the links to make them have the format as follows:
https://www.flickr.com/photos/smileygoldfish/albums
You will see all the corresponding album list of a Flickr account, when you open the link with browser. 

Step4: Open the albums which may be related to babies by the album names within the account, then view the album. If it is truly related to babies, then save the album link.

For example, we may choose to open the albums with names like the following.
My son
One Month
babyName year
My first grandchild
......

Step5: Download the images from the album links saved in step4 with the tool BID (Bulk Image Downloader, download from: http://bulkphotodownloader.com/£©.) Some of the photos in an album may not be downloaded by the tool due to the authority or network reasons, but you can manually download them by opening the HTML document and find the corresponding photo link.

Step5: Delete the unrelated photos, including the following situations.
C1: landscape photos
C2: photos without (clear) faces
C3: photos without babies
C4: composite photos with the photos which belong to one baby

After following these steps, we save the photos belonging to one account in one folder. The photos in one folder may include the following situations:
S1: Photos about one baby but in different time or age
S2: Group photos with their family members or friends

Note: These photos are mainly life photos, even some of them may look like artistic photos. Actually, they also belongs to life photos. They are just processed with simple tools. Especially, in present, there are many friendly-used tools or Apps. People may tend to choose to beautify their photos by these tools.

Any comments are welcome.
Contact: guoshengkang@gmail.com
QQ:275145504
Tel:18202105624
