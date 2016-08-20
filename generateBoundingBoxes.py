# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import pickle
import cv2
import matplotlib.pyplot as plt

rootPath='D:\\BoundingBoxes'
os.mkdir(rootPath) #create folder:BoundingBoxes

imageRootPath='C:\\results_BabyPhotoDataset' #dataPath

for i in range(125): #traverse 125 folders
    folderNum=i+1
    folderName='F'+str(folderNum) 
    os.mkdir(rootPath+'\\'+folderName) #create folders: F1...F125
    pklPath=imageRootPath+'\\'+folderName+'\\roidb.pkl'
    pkl=pd.read_pickle(pklPath) #list
    print folderName
    for k,element in enumerate(pkl):
        fileNum=k+1
        fileName=str(fileNum)+'.png'# do not support .jpg foramt
        element['face']='BoundingBoxes'+'\\'+folderName+'\\'+fileName
        imageName=element['image']
        box=element['boxes']
        im = cv2.imread('C:\\'+imageName) #read image, C disk is where BabyPhotoDataset locates
        im = im[:, :, (2, 1, 0)]
        crop = im[box[1]: box[3], box[0]: box[2], :]#cut boundingBox
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.imshow(crop)
        plt.savefig(rootPath+'\\'+folderName+'\\'+fileName)#save the iamge of the BoundingBoxe
        plt.close()
    #save the revised roidb.pkl file
    os.remove(pklPath) #delete the file, avoid rename error
    output = open(pklPath, 'wb')
    pickle.dump(pkl, output)
    output.close()

#ValueError: Format "jpg" is not supported.
#Supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz. 
#{'image': 'BabyPhotoDataset/F1/F1_1.jpg',
# 'boxes': array([ 366.55511475,  111.8168869 ,  557.08569336,  346.55059814], dtype=float32)}