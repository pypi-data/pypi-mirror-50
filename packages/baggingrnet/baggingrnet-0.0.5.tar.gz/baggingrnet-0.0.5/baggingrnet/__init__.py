# -*- coding: utf-8 -*-
""" Library of Library for Bagging of Deep Residual Neural Networks

This package provides the class of bagging of residual Autoencoder-based
Residual Deep Network with two sets of test datasets. Currently this
library just provides the support for Keras and may extend to other
software of deep learning later.

Major modules:
    model: including the major classes of bagging and base model of
           auto-encoder-based residual deep network, mainly for
           multilayer perceptron (MLP).
           major bagging class: multBagging;
           base model class: resAutoencoder
    util: metric functions including r2 and rmse, also provided in C++
          to support fast calculation.
    data: test data embedded in the package. We provide two datasets,
          one is the simulated dataset and the other is incomplete
          real dataset of PM2.5 with their covariates (with Gaussian noise).
          This data is the 2015 data for the Jing-Jing-Ji area of China.

Github source: https://github.com/lspatial/
Author: Lianfa Li
Date: 2019-08-01

"""
from baggingrnet.data.data import data
from baggingrnet.data.simulatedata import simData
from baggingrnet import model
from baggingrnet import util

__version__ = '0.0.5'

