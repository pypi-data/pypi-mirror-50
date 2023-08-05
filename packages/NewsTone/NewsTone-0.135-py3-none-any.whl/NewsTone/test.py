from __future__ import print_function, division
import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import balanced_accuracy_score
#import config
#from utils import softmax, Logger
import joblib
#from CNN_Model import CNN
import os


def test():
    # random seed / cuda setting
    output = 'result'
    use_cuda = torch.cuda.is_available()
    print('use_cuda = {}\n'.format(use_cuda))
    
    ###Data Loading
    
    filename = 'data/y_test(news_tone).sav'
    y_test = joblib.load(filename)
    y_test = y_test + 1
    
    filename = 'data/x_test(news_tone).sav'
    x_test = joblib.load(filename)
    
    x_test = np.array(x_test, dtype=float)
    y_test = np.array(y_test, dtype=float)
    
    print('--------------Data Loading Done------------')
    
    ### Evaluate
    
    # Load saved model
    if use_cuda:
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    model = CNN(config.embedding_dim, config.num_filters, kernel_size=config.kernel_sizes, stride=1)
    model.load_state_dict(torch.load('model/trained_model(news_tone).pth'))
    model.to(device)
    model.eval()

    # test
    dataset_test = TensorDataset(torch.from_numpy(x_test), torch.from_numpy(y_test))
    test_loader = DataLoader(dataset_test, batch_size=config.batch_size, shuffle=False, num_workers=0, pin_memory=False)
    total_pred = np.array([])
    for i, (inputs, labels) in enumerate(test_loader):
        if use_cuda:
            inputs = inputs.float().cuda()
        else:
            inputs = inputs.float()#.cuda()
        preds, _, = model(inputs)
        preds = preds.cpu()
        tmp = softmax(preds)
        tmp = tmp.detach().numpy()
        total_pred = np.append(total_pred, tmp)
    total_pred = total_pred.reshape((-1, config.output_size))

    ### performance
    '''성능 평가'''
    total_pred = np.argmax(total_pred, axis=1)
    eval_acc = (total_pred == y_test).sum().item() / len(y_test)
    result = confusion_matrix(y_test, total_pred)
    f1_result_none = f1_score(y_test, total_pred, average=None)
    f1_result_macro = f1_score(y_test, total_pred, average='macro')
    bcr = balanced_accuracy_score(y_test, total_pred)
    
    # save result in txt
    '''결과를 result 폴더 안의 result.txt에 저장'''
    logger = Logger(os.path.join(output, 'result.txt'))
    logger.write('acc: %.2f, f1 macro result: %.2f, bcr : %.2f' % (eval_acc, f1_result_macro,bcr))
    