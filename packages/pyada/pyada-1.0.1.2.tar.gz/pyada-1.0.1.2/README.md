## Anomaly detection algorithms.

**Requirement**

1. Compiler with C++11 support (gcc.4.9 or more)
2. Cython 0.23 or more
3. Numpy

**Install package**

Installing to the python library directory.

``python setup.py install``

From pypi

`pip install pyada` 

**Example**
```python
import numpy as np 
import sklearn.metrics as mt 
import pyad  
#%%
# data 
N, D = 400, 5
w = np.random.randn(N, D)
w_score = w.copy()

# Train anomlay detector
# LODA
loda = pyad.Loda()
loda.train(w)
# IForest
iforest = pyad.IsolationForest()
iforest.train(w)

# Add anomalies 
w_score[:3,2:5] = np.random.randn(3, 3)*5
w_score[3:6,1:3] = np.random.randn(3, 2)*-5
label = np.zeros(N)
label[:6] = 1.0 # label as anomalies 

# score 
loda_score = loda.score(w_score)
iforest_score = iforest.score(w_score)

# Computer AUC metrics using sklearn package.
print("AUC(loda): {}, AUC(iForest): {}".format(mt.roc_auc_score(label, loda_score), 
mt.roc_auc_score(label, iforest_score)))
```
### cite 
```
@article{dietterich2018anomaly,
  title={Anomaly Detection in the Presence of Missing Values},
  author={Dietterich, Thomas G and Zemicheal, Tadesse},
  journal={arXiv preprint arXiv:1809.01605},
  year={2018}
}
```


### Status
[![Build Status](https://travis-ci.com/tadeze/pyad.svg?token=4ykfwWQySq2ndZvpPqdz&branch=master)](https://travis-ci.com/tadeze/pyad)


  
  
