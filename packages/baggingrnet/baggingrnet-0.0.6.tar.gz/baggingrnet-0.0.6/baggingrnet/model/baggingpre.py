# -*- coding: utf-8 -*-
"""
Package for the major class of making ensemble predictions using multiple trained models

Author: Lianfa Li
Date: 2019-08-01

"""


import os
import multiprocessing
from multiprocessing import Process, Manager
import pickle
import math

import pandas as pd
import numpy as np
from keras.models import model_from_json
from baggingrnet.util.pmetrics import r2K,r2KAuto,r2np,rmse2np

class ensPrediction:
    """
          Major class of making ensebmle predictions using trained bagging models

         # Examples

         ```python
            # import the major prediction class
           from baggingrnet.model.baggingpre import ensPrediction
           inPath='covs_test.csv'  # The path to the test CSV dataset ;
           gindex='gindex'  # Unique identifier to merging the predictions from multiple models;
           feasList = ['lat', 'lon', 'ele', 'prs'] # List of the name of the predictors to be used in the models;
           target='pm25_avg_log' # Name of the target variable (dependent test)
           bagpath='/testpath/baggingrnet' # The bagging path used to store training results in bagging;
           prepath="/testpath/bagprediction1" # The path to save the results of prediction ;
           mbagpre=ensPrediction(bagpath,prepath) # The instance of the class ensPrediction with the arguments, bagpath,prepath;
           mbagpre.getInputSample(inPath, feasList,gindex) # Load the test datatset
           mbagpre.startMProcess(10) # Start the prediction process using 10 core for parallel predicting;
           mbagpre.aggPredict(isval=True,tfld='pm25_davg') # Get the ensemble predictions from the predictions of multiple models.
          ```
          # Arguments
             :param baggingpath: the root path for multple models，,same as in the bagging class;
             :param targetpath: the target path to save the predictions of multiple models and the ensembled predictions;
             :param maxlimit: Threshold for the extreme values of the predictions, default: 750.
        """
    def __init__(self,baggingpath,targetpath,maxlimit=750):
        tfl = baggingpath + "/tasks.pkl"
        with open(tfl, 'rb') as handle:
            self.tasks = pickle.load(handle)
        self.maxlimit=maxlimit
        self.targetpath=targetpath
        normPath = baggingpath + "/wholesc.pkl"
        with open(normPath, 'rb') as handle:
            self.scX = pickle.load(handle)
            self.scy = pickle.load(handle)

    def getInputSample(self,input, feasList,gindex):
        """
         Function to read the test CSV file
           :param input: Path of the CSV data file (with header available) or the dataframe object;
           :param feasList: List of the names of predictors to be used in the models ;
           :param gindex: Name of unique identifier for each record (item), used later for aggregating;
        """
        if type(input)==str and input!='':
            sampledt = pd.read_csv(input)
        elif type(input)==pd.DataFrame:
            sampledt=input
        else:
            print("Please enter the data file path or original Data Frame of the input! ")
            return
        self.gindexFld=gindex
        self.tcols =feasList
        self.sampledt=sampledt
        X = sampledt[self.tcols]
        self.Xn = self.scX.transform(X)

    def DModelPredict(self,imodel,modelpath,feaIndex,islog=True):
        """
         Function to making the predictions for a model.
           :param imodel: Model unique identifier  ;
           :param modelpath: The path of the trained model  ;
           :param feaIndex: Index of the predictors (features) used in the models;
           :return: the output layer saved in the corresponding path.
        """
        structureFl =  modelpath +'/mframe.json'
        json_file = open(structureFl, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        weiFl = modelpath  +'/weights.hd5'
        loaded_model.load_weights(weiFl)
        loaded_model.compile(optimizer="adam", loss='mean_squared_error',
                             metrics=['mean_squared_error', r2K, r2KAuto])
        Xns=self.Xn[:,feaIndex]
        pre0 = loaded_model.predict(Xns)
        pre = self.scy.inverse_transform(pre0)
        if islog:
            pre = np.exp(pre)
        pre=pre.reshape((pre.shape[0],))
        pre[pre > self.maxlimit] = self.maxlimit
        self.sampledt['pre'] = pre
        tfl = self.targetpath + '/m' + str(imodel) + '_tpre.csv'
        self.sampledt[[self.gindexFld,'pre']].to_csv(tfl, index=False)

    def subPredict(self, istart, iend):
        """
         Function to initiate a process to make predictions for one or multiple trained models.
           :param istart: Staring model identifier;
           :param iend: Ending model identifier;
        """
        p = multiprocessing.current_process()
        print("Starting process " + p.name + ", pid=" + str(p.pid) + " ... ...")
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = ''
        klist = list(self.tasks.keys())
        klist.sort()
        for i in range(istart, iend):
            mkey=klist[i]
            aTask = self.tasks[mkey]
            imodel = aTask['name']
            feaIndex = aTask['feaIndex']
            modelpath = aTask['taskPath']
            islog = aTask['islog']
            self.DModelPredict(imodel,modelpath,feaIndex,islog)
        print("Done with " + p.name + ", pid=" + str(p.pid) + "!")

    def startMProcess(self, ncore):
        """
         Function to initiate multiple process to make the predictions for multiple models.
           :param ncore: Number of cores to be used in parallel predictions;
        """
        n = len(self.tasks)
        nTime = int(math.ceil(n / ncore))
        print(str(ncore) + " cores for " + str(n) + " duties; each core has about " + str(nTime) + " duties")
        for t in range(0, nTime):
            istart = t * ncore
            iend = (t + 1) * ncore
            if t == (nTime - 1):
                iend = n
            processes = []
            for k in range(istart, iend):
                p = Process(name=str(t), target=self.subPredict, args=(k, k + 1,))
                p.daemon = True
                p.start()
                processes.append(p)
            for p in processes:
                p.join()

    def aggPredict(self,isval=False,tfld=None):
        """
         Function to obtain the ensemble predicitons from the outputs of multiple models and evaluation (optional).
           :param isval: False, no evaluation for the ensemble predictions; True, evaluation for the ensemble predictions. Default: False;
           :param tfld: Name of the target variable of ground truth onlu work when isval is True.
           :return:The ensemble predictions to be saved on the aggpreds_eval.csv file of the prediction path;
                   print the evaluation's results if isval is True.
        """
        klist = list(self.tasks.keys())
        klist.sort()
        allpreds=[]
        for i in range(len(klist)):
            mkey = klist[i]
            aTask = self.tasks[mkey]
            imodel = aTask['name']
            tfl = self.targetpath + '/m' + str(imodel) + '_tpre.csv'
            apredictions= pd.read_csv(tfl)
            allpreds.append(apredictions)
        allpreds=pd.concat(allpreds)
        grouped = allpreds['pre'].groupby(allpreds['gindex'])
        gmeann=grouped.mean().to_frame('mean')
        gstd=grouped.std().to_frame('std')
        mergedPre=pd.merge(gmeann, gstd, left_index=True, right_index=True)
        mergedPre.to_csv(self.targetpath+'/aggpreds.csv')
        if not isval:
            return
        evalPre = pd.merge(mergedPre, self.sampledt[['gindex',tfld]],
                             left_index=True, right_on='gindex')
        r2 = r2np(evalPre['mean'], evalPre[tfld])
        rmse = rmse2np(evalPre['mean'], evalPre[tfld])
        evalPre.to_csv(self.targetpath + '/aggpreds_eval.csv')
        print("Independent test r2=",r2,"; rmse=",rmse)