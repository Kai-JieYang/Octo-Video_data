# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:08:01 2021
​
@author: octolab
"""
import cv2   
import numpy as np 
import matplotlib.pyplot as plt  
from skimage.morphology import skeletonize
import glob
import pandas as pd

index = 1
video_direct = 'C:/Users/User/Downloads/drive-download-20220312T213128Z-001/'

save_direct = 'C:/Users/User/Desktop/drive-download-20220311T001757Z-001/'

video_file = glob.glob(video_direct + '*.avi')

for video in video_file:
    frame = []
    #read video file
    cap = cv2.VideoCapture(video)
    success, image = cap.read()
    count = 0
    ret = True
    while ret:
        ret, img = cap.read()
        if ret:
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             frame.append(gray)
    video = np.stack(frame, axis=0) 
    video = video.astype(np.int16)
    #invert video (arm is higher value)
    video_invert = 255-video
    background = video_invert[0]
    video_subtracted = video_invert - background
    video_to_threshold = video_subtracted.copy()

    video_to_threshold[video_to_threshold <= 20] = 0
    video_to_threshold[video_to_threshold > 20] = 1
    
    arm_length = []
    frame_track = []
    frame_num = 0
    for frame in video_to_threshold:
        skeleton = skeletonize(frame)
        count = np.count_nonzero(skeleton == 1)
        arm_length = np.append(arm_length, count)
        frame_track = np.append(frame_track, frame_num)
        frame_num = frame_num + 1
        
    maxi = []
    current = 0
    time = []
    checklist = 0
    for num in arm_length:
        if checklist == 0:
            current = num
            checklist = checklist + 1
        else:
            if num > current:
                maxi.append(num)
                current = num
                time.append(checklist)
                checklist = checklist + 1
        
    
    fig, (ax1) = plt.subplots()
    ax1.scatter(time, maxi)   
    df = pd.DataFrame(maxi)
    df.to_csv(save_direct + 'oct_length' + str(index) + '.csv')  
    index = index + 1        
                
    
    
    
    











