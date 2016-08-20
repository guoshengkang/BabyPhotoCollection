# -*- coding: utf-8 -*-
#calulate precision and recall for multiple clustering results
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import xlwt

def writePRtoExcel(fileName,countFaces,precision,recall): #write the precision and recall to EXCEL
    table=file.add_sheet(fileName)
    table.write(0,0,'cluster_id')
    table.write(0,1,'sizeOfCluster')
    table.write(0,2,'precision')
    table.write(0,3,'recall')
    for ix,num in enumerate(countFaces):
        table.write(ix+1,0,ix)
        table.write(ix+1,1,num)
        table.write(ix+1,2,precision[ix])
        table.write(ix+1,3,recall[ix])

def mean(numbers): #return the mean of a list
    return float(sum(numbers))/max(len(numbers), 1)

def trueClassID(eyes,imageName,xy): #find the cluster id of a boundingBox by imageName
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
        
def maxCount(L): #return the element which appears most frequently
    max=0
    e=-1
    for x in L:
        if L.count(x)>max:
            max=L.count(x)
            e=x
    return e
 
def precision_recall(groundTruthPath,clusterInfoPath):   # computer precision and recall              
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
        eyes[lineNum]=temp #revise ecah row, i.e., revise the 1st column, then save to eyes
        lineNum+=1
    eyes=eyes.astype(np.int64)
    #print 'there are %d pairs of'%(len(eyes))+' eyes'

    #read ClusterInfo
    text_file = open(clusterInfoPath,'rb')
    lines=text_file.readlines()
    text_file.close()
    NumberOffaces=len(lines) #count the number of lines, i.e., number of boundingboxes
    faces=np.zeros((NumberOffaces,7)) #array ['imageName','num','x1','y1','w','h','class'] 
    lineNum=0
    for line in lines: #line is str
        temp=line.split()
        temp[0]=temp[0][-8:-4] #abstract the id of image that BB belongs to
        faces[lineNum]=temp
        lineNum+=1
    faces=faces.astype(np.int64)
    #print 'there are %d'%(len(faces))+' faces'

    labels=list(eyes[:,5]) #abstract the 5th column
    counts=defaultdict(int)
    for x in labels: #calculate the size of each cluster in groundTruth
        counts[x]+=1 #there are 32 clusters in total in groundTruth

    clustering=[]
    (row, col)=faces.shape #831*7
    try:
        flag=faces[0,6]
    except:
        print 'there may be an empty file:'+clusterInfoPath
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
    clustering.append(tempList) # add the last cluster
    countFaces=[len(x)-x.count(-1)for x in clustering]
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
    return (countFaces,precision,recall)

groundTruthPath='C:\\HP_Data\\4recall\\CMU_Complete\\GallagherDatasetGT.txt' #the path of groundTruth
rootPath='D:\\PFAP_results\\' # e.g., D:\PFAP_results\0.60_0.45,0.60_0.50,...\clusterInfo.txt
endPath='\\clusterInfo.txt'
resultPath='D:\\performance\\' #set the path where the output files are saved
aggSure=[0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]
aggStop=[0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]

parameters=[]
averagePrecision=[]
averageRecall=[]
numOfClusters=[]
file=xlwt.Workbook()
for parameter1 in aggSure:
    for parameter2 in aggStop:
        middlePath="%.2f"%(parameter1)+'_'+"%.2f"%(parameter2) 
        parameters.append(middlePath)
        clusterInfoPath=rootPath+middlePath+endPath
        (c,p,r)=precision_recall(groundTruthPath,clusterInfoPath)
        writePRtoExcel(middlePath,c,p,r)
        numOfClusters.append(len(c))
        averagePrecision.append(mean(p)) #add the average precision
        averageRecall.append(mean(r)) #add the average recall
NumOfCombinations=str(len(aggSure)*len(aggStop))
file.save(resultPath+'PrecisionRecallsFor'+NumOfCombinations+'ParameterCombinations.xls')


#write average precision and recall to EXCEL
file=xlwt.Workbook()
table=file.add_sheet('PrecisionAndRecall')
table.write(0,0,'weights')
table.write(0,1,'numberOfClusters')
table.write(0,2,'averagePrecision')
table.write(0,3,'averageRecall')
for ix,p in enumerate(parameters): 
        table.write(ix+1,0,p)
        table.write(ix+1,1,numOfClusters[ix])
        table.write(ix+1,2,averagePrecision[ix])
        table.write(ix+1,3,averageRecall[ix])
file.save(resultPath+'AveragePrecisionRecalls.xls')
 
print 'parameters  AvePrecision    AveRecall'
for i in range(len(parameters)): #print all precision and recall
    print parameters[i],averagePrecision[i],averageRecall[i]

max_p=max(averagePrecision)
ix_p=averagePrecision.index(max_p)
max_r=max(averageRecall)
ix_r=averageRecall.index(max_r)
pr=list((np.array(averagePrecision)+np.array(averageRecall))/2.0) # list to array to list
max_pr=max(pr)
ix_pr=pr.index(max_pr)

optimizedResults=open(resultPath+'optimizedResults.txt','w')
optimizedResults.write('Parameters %s'%(parameters[ix_p])+' has the maximum average precision: %f'%(averagePrecision[ix_p])+'\n')
optimizedResults.write('Parameters %s'%(parameters[ix_r])+' has the maximum average recall: %f'%(averageRecall[ix_r])+'\n')
optimizedResults.write('Parameters %s'%(parameters[ix_pr])+' has the maximum average (precision+recall)/2.0: %f'%(pr[ix_pr]))
optimizedResults.close()