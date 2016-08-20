# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pickle
import os
from shutil import copy
from sklearn.cluster import DBSCAN

DataRootPath='C:\\results_BabyPhotoDataset' #dataPath
ResultRootPath='D:\\clusteringResults'
os.mkdir(ResultRootPath+'\\DBSCANCluster') #create folder: DBCSANCluster
print '---------DBCSANClustering----------START'
DBSCANClusterLabels={}
ResultPath=ResultRootPath+'\\'+'DBSCAN.pkl'##clustering results will save to DBCSAN.pkl
for x in range(125): #test a then 125
    fileNum=x+1
    folderName='F'+str(fileNum)
    npyPath=DataRootPath+'\\'+folderName+'\\head_cacd_feat.npy'
    used_feature=np.load(npyPath) #numpy.ndarray
    pklPath=DataRootPath+'\\'+folderName+'\\roidb.pkl'
    pkl=pd.read_pickle(pklPath) #list
    size=len(used_feature)
    Distances=[]
    for f1 in used_feature:
        for f2 in used_feature:
            distance=np.sqrt(np.sum(np.square(f1-f2)))
            Distances.append(distance)
    Distances.sort()
    #radius=sum(Distances)/float(len(Distances))*0.9
    radius=Distances[int(0.3*len(Distances))] #take 30% quantile，detect a small number of outliers;take 10%detect a large number of outliers
    number=len(pkl)/3 #number reaches to 1/3
    db = DBSCAN(eps=radius, min_samples=number).fit(used_feature)
    db.fit_predict(used_feature)
    DBSCANClusterLabels[folderName]=db.labels_ #clustering label
    #print db.labels_
    num_cluster=max(db.labels_)+1
    print fileNum, num_cluster #print FamilyNumber, number of clusters
    facePath=ResultRootPath+'\\DBSCANCluster\\'+folderName
    os.mkdir(facePath) #create folders: Fx
    #for y in range(num_cluster):   
    #    os.mkdir(facePath+'\\C'+str(y+1)) #create folders: C1...Cn  
    if -1 in db.labels_:
        os.mkdir(facePath+'\\C0') #create folder: C0--the folder where outliers are in
    #for i,k in enumerate(db.labels_):
    #    copy('D:\\'+pkl[i]['face'],facePath+'\\C'+str(k+1))
    for i,k in enumerate(db.labels_):
        if k!=-1:
            copy('D:\\'+pkl[i]['face'],facePath) # BoundingBoxes folder is located in D:\\
        else:
            copy('D:\\'+pkl[i]['face'],facePath+'\\C'+str(k+1)) #k==-1, save photo to C0 folder
#write the clustering results to spectral.pkl file
output = open(ResultPath, 'wb') #will cover the file with the same name, if there is
pickle.dump(DBSCANClusterLabels, output)
output.close()
print '---------DBCSANClustering----------END'
# roidb.pkl is a list, an example of an element is as follows.
#{'boxes': array([ 307.47695923,   87.3265686 ,  420.39474487,  203.52502441], dtype=float32),
#  'face': 'BoundingBoxes\\F1\\1.png',
#  'image': 'BabyPhotoDataset/F1/F1_17.jpg'}
