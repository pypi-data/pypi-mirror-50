# -*- coding: utf-8 -*-
"""
Package for the major class of bagging of deep residual network

Author: Lianfa Li
Date: 2019-08-01

"""

import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import pandas as pd
import pickle

import math
import multiprocessing
from multiprocessing import Process, Manager

import os
import shutil
from keras.callbacks import EarlyStopping, ReduceLROnPlateau,ModelCheckpoint

from baggingrnet.model.resnet import resAutoencoder
#from baggingrnet.util.pmetrics import r2K,r2KAuto,rmse,r2np,rmse2np
from baggingrnet.util.pmetrics import r2K,r2KAuto,r2np,rmse2np
import matplotlib.pyplot as plt


class multBagging:
    """
          Major class of Bagging of Deep Residual Networks (MLP)
          This class provides bagging framework for deep residual networks

         # Examples

         ```python
             # import the class from the library  :
            from baggingrnet.model.bagging import  multBagging
            inPath='traindata.csv' # data file of training samples
            gindex='gindex'  # Unique id for merging the outputs of multiple models
            stratif='jd'  # Stratifying factor
            feasList = ['lat', 'lon', 'ele', 'prs', 'tem'] # Names of predictors
            target='pm25_avg_log' # the target variable
            bagpath='/testpath/baggingrnet'  # Bagging path
            mbag=multBagging(bagpath)   # Instance of bagging class,multBagging and initialize it
            mbag.getInputSample(inPath, feasList,stratif,gindex,target) #Read the data samples
            #Set the models to be trained. The nodes may be changes to introduce randomness to reduce correlation between models.
            for i in range(80):
                name = str(i) # model name: must be unique, different from the names of other models.
                nodes = [156,128,96,64,32,12] # Length of the list determines the number of encoding layers and values in it is the number of ndoes.
                minibatch = 2560 # Size for mini batch
                isresidual = True # Whether to use residual connections, default: True
                nepoch = 100 # Number of training epochs
                sampling_fea = False # Whether to sample the features to introduce randomness
                noutput = 1 # Number of nodes for the output, default: 1
                mbag.addTask(noutput, sampling_fea, nepoch, name, nodes, minibatch, isresidual) # Add the tast of training a model to a hash table.

            mbag.startMProcess(10) # Start parallel training using 10 cores
          ```
          # Arguments
             baggingpath: the root path for multple models (model name as sub paths).
        """
    def __init__(self,baggingpath=None):
        print('initializing ... ')
        self.tasks={}
        self.baggingpath=baggingpath if baggingpath is not None else '/tmp'

    def addTask(self,name,noutput=1,sampling_fea=False,nepoch=20,nodes=[128,96,64,32,16],
                minibatch=1280,isresidual=True,islog=True):
        """
         Function to add a modeling duty to the tasks dictionary of this class, model name is the unique identifier
           :param name: Model name, should be unique, different from the names of the other models;
           :param noutput: Number of output nodes, default 1;
           :param sampling_fea: Whether to sample the predictors (features) by bootstrap, default: False;
           :param nepoch: Number of epochs, default: 20 ;
           :param nodes: list of the number of nodes for the encoding and coding layers, default: [128,96,64,32,16];
                         This topology is applicable for the test case. You may introduce small randomness to reduce
                         the correlation between models;
           :param minibatch: Size of a mini batch ;
           :param isresidual: Whether to use residual connections, default: True
           :param islog: whether to make the log transformation for the target variable, default: True.
        """
        if name in self.tasks.keys():
            print("Task:"+name + " already in tasks! please change the model name!")
            return
        nsz=self.Xn.shape[0]
        nfea=self.Xn.shape[1]
        trainIndex, testIndex =  train_test_split(range(nsz), stratify=self.stratify,test_size=0.189)
        trainIndex, validIndex = train_test_split(trainIndex,test_size=0.189)
        taskPath=self.baggingpath+'/m_'+name
        feaIndex=np.array([i for i in range(nfea)])
        if sampling_fea:
            feaIndex=np.unique(np.random.choice(range(nfea),nfea))
        if os.path.exists(taskPath) and os.path.isdir(taskPath):
            shutil.rmtree(taskPath)
        os.makedirs(taskPath, 0o777)
        aTask={'name':name,'nepoch':nepoch,'noutput':noutput,'nodes':nodes,'trainIndex':trainIndex,'validIndex':validIndex,
               'isresidual':isresidual,'testIndex':testIndex,'feaIndex':feaIndex,'minibatch':minibatch,'taskPath':taskPath,
               'islog':islog}
        taskFl=taskPath+"/taskdict.pkl"
        with open(taskFl, "wb") as f:
            pickle.dump(aTask, f,pickle.HIGHEST_PROTOCOL)
        self.tasks[name]=aTask

    def removeTask(self,name):
        """
         Function to remove a modeling task from the tasks dictionary
           :param name: unique name for the model to be removed ;
        """
        if name in self.tasks.keys():
            try:
                del self.tasks[name]
            except KeyError:
                pass


    def getInputSample(self,input, feasList,stratify,gindex,target):
        """
         Function to obtain one decoding or encoding building unit (consisting of multiple convolutions)
           :param input: Path of the CSV data file (with header available) or the dataframe object;
           :param feasList: List of the names of predictors to be used in the models ;
           :param stratify: Name of stratifying factor (string);
           :param gindex: Name of unique identifier for each record (item), used later for aggregating;
           :param target: Name of the target variable (dependent variable) (string).
        """
        if type(input)==str and input!='':
            sampledt = pd.read_csv(input)
        elif type(input)==pd.DataFrame:
            sampledt=input
        else:
            print("Please enter the data file path or original Data Frame of the input! ")
            return
        print(sampledt.shape)
        self.gindex=sampledt[gindex]
        self.stratify=sampledt[stratify] if stratify is not None else None
        self.tcols =feasList
        X = sampledt[self.tcols]
        y = sampledt[target]
        if type(target)==str:
            y = y.reshape((y.shape[0], 1))
        self.scX = preprocessing.StandardScaler().fit(X)
        self.scy = preprocessing.StandardScaler().fit(y)
        self.Xn = self.scX.transform(X)
        self.yn = self.scy.transform(y)
        tfl=self.baggingpath+"/wholesc.pkl"
        with open(tfl, "wb") as f:
            pickle.dump(self.scX, f,pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.scy, f)
        tfl=self.baggingpath+"/wholeXyn.pkl"
        with open(tfl, "wb") as f:
            pickle.dump(self.Xn, f,pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.yn, f)

    def getTrainHistPlot(self,history, metric, tPath):
        """
         Function to make the plot of learning curve, just used internally.
           :param history: Training history data table ;
           :param metric: The metric (e.g., loss, R2, or RMSE) to be draw ;
           :param tPath: The output path of the plot;
        """
        plt.plot(history.history[metric])
        plt.plot(history.history['val_' + metric])
        plt.title('model ' + metric)
        plt.ylabel(metric)
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig(tPath)
        plt.close()

    def subTrain(self, perm,istart, iend):
        """
         Function to initiate a process to train the models
           :param perm: Global manager to store the output generated in this process  ;
           :param istart: Staring index of the models for this process ;
           :param iend:  Ending index of the models for this process ;
        """
        p = multiprocessing.current_process()
        print("Starting process "+p.name+", pid="+str(p.pid)+" ... ...")
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = ''
        klist = list(self.tasks.keys())
        klist.sort()
        for i in range(istart, iend):
            key=klist[i]
            print(i, key)
            aTask=self.tasks[key]
            name=aTask['name']
            nodes=aTask['nodes']
            trainIndex = aTask['trainIndex']
            validIndex = aTask['validIndex']
            testIndex = aTask['testIndex']
            feaIndex = aTask['feaIndex']
            taskPath = aTask['taskPath']
            batch=aTask['minibatch']
            nepoch=aTask['nepoch']
            islog = aTask['islog']
            modelFl = taskPath+'/weights.hd5'
            checkpoint = ModelCheckpoint(modelFl, monitor='loss', verbose=0, save_best_only=True, mode='min',
                                         save_weights_only=True)
            reduceLROnPlat = ReduceLROnPlateau(monitor='loss', factor=0.01,
                                               patience=1, verbose=0, mode='min',
                                               min_delta=0.00003, cooldown=0, min_lr=1e-8)
            early = EarlyStopping(monitor='loss', mode="min", verbose=2,
                                  patience=50)
            modelCls = resAutoencoder(len(feaIndex),nodes,'relu',1,inresidual=aTask['isresidual'],outnres=None,
                                      dropout=0.02, defact='linear')
            model = modelCls.resAutoNet()
            model.compile(optimizer="adam", loss='mean_squared_error',
                          metrics=['mean_squared_error', r2K, r2KAuto])
            model_json = model.to_json()
            with open(taskPath + "/mframe.json", "w") as json_file:
                json_file.write(model_json)
            fhist = model.fit(self.Xn[trainIndex,:][:,feaIndex], self.yn[trainIndex,:], batch_size=batch, epochs=nepoch, verbose=0,
                              shuffle=True,callbacks=[early, checkpoint, reduceLROnPlat],
                              validation_data=(self.Xn[validIndex,:][:,feaIndex], self.yn[validIndex,:]))
            y_test_pred = model.predict(self.Xn[testIndex,:][:,feaIndex])
            obs = self.scy.inverse_transform(self.yn[testIndex, :])
            pre = self.scy.inverse_transform(y_test_pred[:, :])
            if islog:
                obs = np.exp(obs)
                pre = np.exp(pre)
            testDf=pd.DataFrame({'obs':obs.reshape(obs.shape[0]),'pre':pre.reshape(pre.shape[0])},
                                index=self.gindex[testIndex])
            tPath = taskPath+'/preds_' + name + '.csv'
            testDf.to_csv(tPath,index_label="index")
            r2 = r2np(obs, pre)
            rmse = rmse2np(obs, pre)
            print("indepdendent test:r2-", r2, "rmse:", rmse)
            #datafl = self.outpath + '/res_'+atask['name']+'.npz'
            ares=pd.DataFrame({'name':name,'max_reg_r2':max(fhist.history['r2KAuto']),'min_reg_rmse':min(fhist.history['loss']),
                    'max_val_r2':max(fhist.history['val_r2KAuto']),'min_val_rmse':min(fhist.history['val_loss']),
                    'testr2':r2,'testrmse':rmse},index=[0])
            perm.append(ares)
            tPath = taskPath+'/d_' + name + '_metric.csv'
            ares.to_csv(tPath)
            tPath = taskPath+'/d_' + name + '_trainhist.csv'
            pd.DataFrame(fhist.history).to_csv(tPath)
            tPath =taskPath+'/d_' + name + ".loss.png"
            self.getTrainHistPlot(fhist, "loss", tPath)
            tPath = taskPath+'/d_' + name + ".r2.png"
            self.getTrainHistPlot(fhist, "r2KAuto", tPath)
        print("Done with " + p.name + ", pid=" + str(p.pid) + "!")


    def startMProcess(self, ncore):
        """
         Function to initiate parallel training of multiple models
           :param ncore: Number of cores to be used for parallel training.
           :return: ALl the results saved in the path of the bagging path initiatized when generating this class instance.
        """
        n = len(self.tasks)
        nTime = int(math.ceil(n / ncore))
        print(str(ncore) + " cores for " + str(n) + " duties; each core has about " + str(nTime) + " duties")
        manager = Manager()
        perm= manager.list()
        for t in range(0, nTime):
            istart = t * ncore
            iend = (t + 1) * ncore
            if t == (nTime - 1):
                iend = n
            processes = []
            for k in range(istart, iend):
                p = Process(name=str(t), target=self.subTrain, args=(perm,k, k + 1,))
                p.daemon = True
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
        allres=pd.concat(perm, axis=0)
        tfl=self.baggingpath+'/allresult.csv'
        allres.to_csv(tfl,index_label='index')
        tfl = self.baggingpath + "/tasks.pkl"
        with open(tfl, "wb") as handle:
            pickle.dump(self.tasks, handle, pickle.HIGHEST_PROTOCOL)

