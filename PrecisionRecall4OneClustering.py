# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlwt
from collections import defaultdict

def trueClassID(eyes,imageName,xy):
    (x,y,w,h)=xy
    (x,y,w,h)=(x+w/4.0,y+h/4.0,w/2.0,h/2.0)
    (X1,Y1,X2,Y2)=(x,y,x+w,y+h)
    imageNameCol=list(eyes[:,0])
    ix=imageNameCol.index(imageName)
    ct=imageNameCol.count(imageName)
    for i in range(ix,ix+ct):
        (x1,y1,x2,y2)=eyes[i,1:5]
        if x1>=X1 and x1<=X2 and \
           y1>=Y1 and y1<=Y2 and \
           x2>=X1 and x1<=X2 and \
           y1>=Y1 and y1<=Y2:
               return eyes[i,5]
    if i==ix+ct-1:
        return -1
        
def maxCount(L): #返回列表中出现次数最多的元素
    max=0
    e=-1
    for x in L:
        if L.count(x)>max:
            max=L.count(x)
            e=x
    return e

#configuring below
groundTruthPath='C:\\HP_Data\\4recall\\CMU_Complete\\GallagherDatasetGT.txt'
#clusterInfoPath='C:\\HP_Data\\4recall\\out\\cluster_info\\clusterInfo.txt'
clusterInfoPath='D:\\results++\\0.80_0.75\\part1\\cluster_info\\clusterInfo.txt'
resultPath='D:\\'
#configuring above                                                                
#read GroundTruth
text_file = open(groundTruthPath,'rb')
lines=text_file.readlines()
text_file.close()
NumberOfeyes=len(lines) #931行
eyes=np.zeros((NumberOfeyes,6)) #array ['imageName','x1','y1','x2','y2','class'] 
lineNum=0
for line in lines: #line is str
    temp=line.split()
    temp[0]=temp[0][-8:-4]
    eyes[lineNum]=temp
    lineNum+=1
eyes=eyes.astype(np.int64)
print 'there are %d pairs of'%(len(eyes))+' eyes'

#read ClusterInfo
text_file = open(clusterInfoPath,'rb')
lines=text_file.readlines()
text_file.close()
NumberOffaces=len(lines) #931行
faces=np.zeros((NumberOffaces,7)) #array ['imageName','num','x1','y1','w','h','class'] 
lineNum=0
for line in lines: #line is str
    temp=line.split()
    temp[0]=temp[0][-8:-4]
    faces[lineNum]=temp
    lineNum+=1
faces=faces.astype(np.int64)
print 'there are %d'%(len(faces))+' faces'

labels=list(eyes[:,5])
counts=defaultdict(int)
for x in labels: #统计各个类别的大小
    counts[x]+=1 #共32个类别

clustering=[]
(row, col)=faces.shape
flag=faces[0,6]
tempList=[]
for i in range(row):
    class_num=faces[i,6]
    ID=trueClassID(eyes,faces[i,0],faces[i,2:6])
    if class_num==flag:
        tempList.append(ID)
    else:
        flag=class_num
        clustering.append(tempList)
        tempList=[]
        tempList.append(ID)
clustering.append(tempList)

precision=[]
recall=[]
for x in clustering:
    id=maxCount(x)
    if id!=-1:
        p=x.count(id)/float((len(x)-x.count(-1)))
        r=x.count(id)/float(counts[id])
    else:
        p=0
        r=0
    precision.append(p)   
    recall.append(r)

print "there are %d clusters"%(len(clustering)) 
print "the average precision of Top5 clusters is %f"%(sum(precision[:5])/5.0) #前5个类的平均precision
print "the average recall of Top5 clusters is %f"%(sum(recall[:5])/5.0) #前5个类的平均recall

countFaces=[len(x)-x.count(-1)for x in clustering]
print countFaces

#write precision and recall to EXCEL
file=xlwt.Workbook()
table=file.add_sheet('precisionAndRecall')
table.write(0,0,'cluster_id')
table.write(0,1,'size of cluster')
table.write(0,2,'precision')
table.write(0,3,'recall')
for ix,num in enumerate(countFaces):
    table.write(ix+1,0,ix)
    table.write(ix+1,1,num)
    table.write(ix+1,2,precision[ix])
    table.write(ix+1,3,recall[ix])
file.save(resultPath+'PrecisionRecalls.xls')

fig,axes=plt.subplots(2,2)
axes[0,0].plot(precision,label='precision')
axes[0,0].plot(recall,label='recall')
#axes[0,0].set_title("precision VS recall",fontsize=10)
axes[0,0].set_xlabel('clusters')
axes[0,0].set_ylabel('precision/recall')
axes[0,0].legend(loc='best')
axes[1,0].plot(countFaces,color='r',label='numberOfBoundingboxes')
#axes[1,0].set_title("Number of boundingboxes",fontsize=10)
axes[1,0].set_xlabel('clusters')
axes[1,0].set_ylabel('number')
axes[1,0].legend(loc='best')
topN=10
if len(precision)<topN:
    topN=len(precision)
axes[0,1].plot(precision[:topN],label='precision')
axes[0,1].plot(recall[:topN],label='recall')
#axes[0,1].set_title("precision VS recall",fontsize=10)
axes[0,1].set_xlabel('top%d clusters'%(topN))
axes[0,1].set_ylabel('precision/recall')
axes[0,1].legend(loc='best')
axes[1,1].plot(countFaces[:topN],color='r',label='numberOfBoundingboxes')
#axes[1,1].set_title("Number of boundingboxes",fontsize=10)
axes[1,1].set_xlabel('top%d clusters'%(topN))
axes[1,1].set_ylabel('number')
axes[1,1].legend(loc='best')

plt.show() #plt.show()显示出创建的所有绘图对象。