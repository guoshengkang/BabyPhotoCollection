# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pickle
import os
from shutil import copy
from sklearn.cluster import SpectralClustering

DataRootPath='C:\\results_BabyPhotoDataset' # feature data: head_cacd_feat.npy and roidb.pkl
ResultRootPath='D:\\clusteringResults'
os.mkdir(ResultRootPath+'\\spectralCluster') #create folder: spectralCluster
print '---------SpectralClustering----------START'
spectralClusterLabels={}
ResultPath=ResultRootPath+'\\'+'spectral.pkl'#clustering results will save to spectral.pkl
num_cluster=2 #Number of clusters
for x in range(125):
    fileNum=x+1
    folderName='F'+str(fileNum)
    npyPath=DataRootPath+'\\'+folderName+'\\head_cacd_feat.npy'
    used_feature=np.load(npyPath) #numpy.ndarray
    pklPath=DataRootPath+'\\'+folderName+'\\roidb.pkl'
    pkl=pd.read_pickle(pklPath) #list
    size=len(used_feature)
    spectral = SpectralClustering(n_clusters=num_cluster, affinity='nearest_neighbors')
    spectral.fit_predict(used_feature)
    spectralClusterLabels[folderName]=spectral.labels_ #cluster label
    facePath=ResultRootPath+'\\spectralCluster\\'+folderName
    os.mkdir(facePath) #create folder Fx
    for y in range(num_cluster):   
        os.mkdir(facePath+'\\C'+str(y+1)) #create folders: C1...Cn  
    for i,k in enumerate(spectral.labels_):
        copy('D:\\'+pkl[i]['face'],facePath+'\\C'+str(k+1))
#write the clustering results to spectral.pkl file
output = open(ResultPath, 'wb') #will cover the file with the same name, if there is
pickle.dump(spectralClusterLabels, output)
output.close()
print '---------SpectralClustering----------END'
# roidb.pkl is a list, an example of an element is as follows.
#{'boxes': array([ 307.47695923,   87.3265686 ,  420.39474487,  203.52502441], dtype=float32),
#  'face': 'BoundingBoxes\\F1\\1.png',
#  'image': 'BabyPhotoDataset/F1/F1_17.jpg'},
