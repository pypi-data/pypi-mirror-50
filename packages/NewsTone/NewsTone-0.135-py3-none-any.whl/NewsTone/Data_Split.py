import gensim
import tqdm
import pickle
import numpy as np
from utils import pad_sentences, pad_sentences2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import os
#########################
####Preprocessing
#########################

# Make save folder
'''for performance'''
dirname = os.path.join(os.getcwd(), 'result')
if not os.path.exists(dirname):
    os.mkdir(dirname)

'''for trained model'''
dirname = os.path.join(os.getcwd(), 'model')
if not os.path.exists(dirname):
    os.mkdir(dirname)

# Tokenizing sentence
with open('data/total_tokenized_corpus_kkma_within_w2v.txt', 'rb') as f:
    data_sentence = np.array(pickle.load(f))
# Embedding
embedding = gensim.models.Word2Vec.load(('data/ko_w2v_100d_min50_2nd_sg'))

# 없는 단어는 제외
'''For Classification'''
final_data_setence = []
for i in tqdm.tqdm(range(len(data_sentence))) :
    tmp_sentence = []
    not_lists = []
    for j in range(len(data_sentence[i])) :
        tmp = data_sentence[i][j]
        try :
            tmp_sentence.append(embedding[tmp])
        except  :
            pass
    final_data_setence.append(np.array(tmp_sentence))

'''For Visualization '''
final_data_setence2 = []
for i in tqdm.tqdm(range(len(data_sentence))) :
    tmp_sentence = []
    not_lists = []
    for j in range(len(data_sentence[i])) :
        tmp = data_sentence[i][j]
        try :
            if embedding[tmp].shape[0] == 100 :
                tmp_sentence.append(tmp)
        except  :
            pass
    final_data_setence2.append(np.array(tmp_sentence))


# Sentence padding
'''각 문장의 길이를 500으로 통일'''
final_data_setence3 = pad_sentences(final_data_setence)
final_data_setence4 = pad_sentences2(final_data_setence2)

''''''
filename = 'data/total_data.sav'
joblib.dump(final_data_setence3, filename=filename)

filename = 'data/total_word_data.sav'
joblib.dump(final_data_setence4, filename=filename)

print('total_for_visualization_done')

# target data loading
'''평가 데이터'''
y = (pd.read_csv('./data/total_labeled_article.csv')['평가'])

# Data Split
x_train, x_test, y_train, y_test = train_test_split(final_data_setence3, y , test_size=0.3, random_state=220)

del data_sentence
del final_data_setence
del final_data_setence2
del final_data_setence3
del final_data_setence4

filename = 'data/x_train.sav'
joblib.dump(x_train, filename=filename)
del x_train
print('input_train_done')

filename = 'data/y_train.sav'
joblib.dump(y_train, filename=filename)

print('target_train_done')
del y_train

filename = 'data/x_test.sav'
joblib.dump(x_test, filename=filename)

print('input_test_done')
del x_test

filename = 'data/y_test.sav'
joblib.dump(y_test, filename=filename)

print('target_test_done')
del y_test


print('---Data Split Done---')