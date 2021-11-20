# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:43:51 2021

@author: JOEL
"""
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from keras import backend as K
from keras.models import Model
import pickle
import os

def mri_predict(axial,coronal,sagittal):
    axial = axial.reshape(16,256,256,1)
    coronal = coronal.reshape(16,256,256,1)
    sagittal = sagittal.reshape(16,256,256,1)
    axial_cnn = keras.models.load_model(os.path.join("signin","axcnn_new"+".h5"))
    coronal_cnn = keras.models.load_model(os.path.join("signin","corcnn_new"+".h5"))
    sagittal_cnn = keras.models.load_model(os.path.join("signin","sagcnn_new"+".h5"))
    filename = os.path.join("signin","softmax_reg_new"+".sav")
    s_model = pickle.load(open(filename, 'rb')) 
    ax_prediction = 0
    cor_prediction = 0
    sag_prediction = 0
    for i in range(16):
        axialtemp = axial[i,:,:,:]
        axialtemp = axialtemp.reshape(1,256,256,1)
        ax_predict = axial_cnn.predict(axialtemp)
        ax_prediction+=ax_predict 
        coronaltemp = coronal[i,:,:,:]
        coronaltemp = coronaltemp.reshape(1,256,256,1)
        cor_predict = coronal_cnn.predict(coronaltemp)
        cor_prediction+=cor_predict
        sagittaltemp = sagittal[i,:,:,:]
        sagittaltemp = sagittaltemp.reshape(1,256,256,1)
        sag_predict = sagittal_cnn.predict(sagittaltemp)
        sag_prediction+=sag_predict
    fp_sag = sag_prediction/16
    fp_ax = ax_prediction/16
    fp_cor = cor_prediction/16
    
    fp_ax = np.array(fp_ax)
    fp_cor = np.array(fp_cor)
    fp_sag = np.array(fp_sag)
    
    combined = np.concatenate((fp_ax,fp_cor,fp_sag),axis = 1)
    fp = int(s_model.predict(combined))
    perc = 0
    perc = (fp_ax[0,fp]+fp_cor[0,fp]+fp_sag[0,fp])/3
    return(fp,perc)
