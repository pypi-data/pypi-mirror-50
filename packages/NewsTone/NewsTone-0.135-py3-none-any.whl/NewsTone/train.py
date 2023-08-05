from __future__ import print_function, division
import time
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
#import config
import joblib
#from CNN_Model import CNN

def train():
    # random seed / cuda setting
    np.random.seed(0)
    torch.manual_seed(0)
    
    use_cuda = torch.cuda.is_available()
    print('use_cuda = {}\n'.format(use_cuda))
    
    ###Data Loading
    '''학습용 input / target Data 불러오기 '''
    
    filename = 'data/y_train.sav'
    y_train = joblib.load(filename)
    y_train = y_train + 1
    
    filename = 'data/x_train.sav'
    x_train = joblib.load(filename)
    
    x_train = np.array(x_train, dtype=float)
    y_train = np.array(y_train, dtype=float)
        
    y_train_zero = np.where(y_train == 0)[0]
    y_train_one = np.where(y_train == 1)[0]
    y_train_two = np.where(y_train == 2)[0]

    print('--------------Data Loading Done------------')

    # Training
    '''모델 학습 실시 '''
    

    model = CNN(config.embedding_dim, config.num_filters,kernel_size = config.kernel_sizes, stride=1)
    model = model.cuda()
    parameters = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = torch.optim.Adam(parameters, lr=0.002)
    loss_fn = nn.CrossEntropyLoss()
    
    for epoch in range(10) :
        tic = time.time()
        model.train()
        for batch_ in range(int(len(y_train)/ config.batch_size)) :
            tmp_zero = np.random.choice((y_train_zero), int(config.batch_size/config.output_size), replace=False)
            tmp_two = np.random.choice((y_train_two), int(config.batch_size/config.output_size), replace=False)
            tmp_one = np.random.choice((y_train_one), int(config.batch_size/config.output_size), replace=False)

            inputs = np.vstack((x_train[tmp_zero], x_train[tmp_two], x_train[tmp_one]))
            labels = np.hstack((y_train[tmp_zero], y_train[tmp_two], y_train[tmp_one]))

            inputs = Variable(torch.from_numpy(inputs))
            labels = Variable(torch.from_numpy(labels))
            if use_cuda:
                inputs, labels = inputs.float().cuda(), labels.cuda()
            preds,_= model(inputs)
            labels = labels.long().cuda()

            loss = loss_fn(preds, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print('{} epoch_{}'.format(epoch,loss))

    # Save trained model
    '''학습된 모델 저장'''
    
    torch.save(model.state_dict(),'model/trained_model.pth')
    

    print('----Trained Model Saved----')