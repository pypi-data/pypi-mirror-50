import re
import pickle
import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from konlpy.tag import Kkma
from tqdm import tqdm  # pip install tqdm

#from utils import pad_sentences, pad_sentences2
from sklearn.model_selection import train_test_split
import joblib
import os

def get_columns(df):
    '''xlsx 파일에서 필요한 컬럼만 가져오는 함수
    Args:
        - df : DataFrame
    Return:
        - df : [내용, 평가]로 이루어진 DataFrame '''
    return df[['내용', '평가']]


def correct_label(df):
    '''Label이 잘못된 부분을 수정하는 함수
    Args: 
        - df : Dataframe [내용, 평가]
    Return:
        - df : Label이 수정된 DataFrame'''
    
    correct_label_dict = {
        '긍정': '옹호',
        '긍정/보도자료': '옹호',
        '보도자료.옹호': '옹호',
        '중입': '중립',
        ' 중립': '중립',
        '옹호 ': '옹호',
        '증립': '중립',
        '주읿': '중립', 
        '중힙': '중립',
        '옹로': '옹호',
        '엉호': '옹호',
        '중랍': '중립',
        '융호': '옹호',
        '부부정': '부정',
        '옹ㅎ': '옹호',
        '부정 ': '부정',
        '웅호': '옹호',
        '올호': '옹호',
        '중립ㅂ': '중립',
        '부넝': '부정',
        '옹호옹호': '옹호',
        ' 부정': '부정',
        '부정정': '부정',
        '온호': '옹호',
        '즁립': '중립',
        '부덩': '부정',
        '부저ㅏㅇ': '부정',
        '옹ㅇ호': '옹호',
        '뷰종': '부정',
        '증ㄹ;ㅂ': '중립',
        'ㅈ우': '중립',
        '중리': '중립',
        '엉허': '옹호',
        '붱': '부정',
        '오옿': '옹호',
        '중': '중립',
        '즁랍': '중립',
        '즁': '중립',
        '증': '중립',
        '중ㅂ': '중립',
        '부': '부정',
        '부저': '부정',
        '부장': '부정', }

    df['평가'] = df['평가'].replace(correct_label_dict)
    # 옹호, 중립, 평가 데이터 만 들고오기
    df = df.query("(평가 == '옹호') | (평가 == '부정') | (평가 == '중립')")
    
    return df


def clean_text(text):
    '''기사 내용 전처리 함수
    Args:
        - text: str 형태의 텍스트
    Return:
        - text: 전처리된 텍스트'''
    # Common
    # E-mail 제거#
    text = re.sub('([\w\d.]+@[\w\d.]+)', '', text)
    text = re.sub('([\w\d.]+@)', '', text)
    # 괄호 안 제거#
    text = re.sub("<[\w\s\d‘’=/·~:&,`]+>", "", text)
    text = re.sub("\([\w\s\d‘’=/·~:&,`]+\)", "", text)
    text = re.sub("\[[\w\s\d‘’=/·~:&,`]+\]", "", text)
    text = re.sub("【[\w\s\d‘’=/·~:&,`]+】", "", text)
    # 전화번호 제거#
    text = re.sub("(\d{2,3})-(\d{3,4}-\d{4})", "", text)  # 전화번호
    text = re.sub("(\d{3,4}-\d{4})", "", text)  # 전화번호
    # 홈페이지 주소 제거#
    text = re.sub('(www.\w.+)', '', text)
    text = re.sub('(.\w+.com)', '', text)
    text = re.sub('(.\w+.co.kr)', '', text)
    text = re.sub('(.\w+.go.kr)', '', text)
    # 기자 이름 제거#
    text = re.sub("/\w+[=·\w@]+\w+\s[=·\w@]+", "", text)
    text = re.sub("\w{2,4}\s기자", "", text)
    # 한자 제거#
    text = re.sub('[\u2E80-\u2EFF\u3400-\u4DBF\u4E00-\u9FBF\uF900]+', '', text)
    # 특수기호 제거#
    text = re.sub("[◇#/▶▲◆■●△①②③★○◎▽=▷☞◀ⓒ□?㈜♠☎]", "", text)
    # 따옴표 제거#
    text = re.sub("[\"\'”“‘’]", "", text)
    # 2안_숫자제거#
    # text = regex.sub('[0-9]+',"",text)
    return text


def label_encoder(df):
    '''Label Encodingto
    Args:
        - df: DataFrame
    Return:
        - df: DataFrame
            - 옹호 = 1, 부정 = -1, 중립 = 0'''
    df['평가'].replace('옹호', 1, inplace=True)
    df['평가'].replace('부정', -1, inplace=True)
    df['평가'].replace('중립', 0, inplace=True)
    return df
    
def make_path(file):
    curpath = os.getcwd()

    data_path = file.split('/')
    del data_path[-1]
    for i in data_path:    
        curpath = os.path.join(curpath, i)
        if not os.path.exists(curpath):
            os.mkdir(curpath)
    
def is_csv(file):
    if file.split('.')[-1] == 'csv':
        return True
    else:
        return False
    
def refine_text(file, refine_data):
    ###########################
    # Step1 : xlsx 파일 전처리 #
    ###########################
    ###change to cython or pypy later
    
    if is_csv(file):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file, header=0)
    df = get_columns(df)  # 필요한 컬럼만 가져오기
    df = correct_label(df)  # 잘못된 Label 수정
    df = df.dropna()  # NA 제거
    df = df.drop_duplicates(subset='내용')  # 중복 기사 제거
    df['내용'] = df['내용'].apply(clean_text)  # 기사 내용 전처리
    df['내용'] = df['내용'].replace('', np.nan)
    df['내용'] = df['내용'].replace(' ', np.nan)
    df['내용'] = df['내용'].replace('  ', np.nan)
    df = df.dropna()

    df = label_encoder(df)  # Label encoding

    # 전처리한 Trainset csv 파일로 저장하기
    if not os.path.exists('./data'):
        os.mkdir('./data')
    df.to_csv(refine_data, index=False)
    return refine_data
    
def tokenize(refine_data, pretrained_file, tokenized_text):
 ######################################################
    # Step2 : Text-CNN 모델의 Input에 맞도록 텍스트 전처리 #
    ######################################################
    if is_csv(refine_data):
        df = pd.read_csv(refine_data)
    else:
        df = pd.read_excel(refine_data, header=0)
        
    

    kkma = Kkma(max_heap_size=4096)  # Kkma(꼬꼬마) 형태소 분석기

    word2vec_path = pretrained_file
    w2v_model = Word2Vec.load(word2vec_path)  # Pre-Trained Word2Vec 로드

    w2v_words = w2v_model.wv.index2word
    corpus = np.array(df['내용'].tolist())

    texts_in_w2v = []
    null_indices = []
    
    w2vtext_append = texts_in_w2v.append
    null_append = null_indices.append
    
    for idx, text in enumerate(tqdm(corpus)):
        text = [f'{word}_{pos}' for word, pos in kkma.pos(text)]
        text = [word for word in text if word in w2v_words]
        if text:
            w2vtext_append(text)
        elif not text:
            null_append(idx)

    df = df.drop(df.index[null_indices])  # 텍스트 전처리 후 Null 값 제거
    
    # 전처리한 Trainset csv 파일로 다시 저장하기
    df.to_csv(refine_data, index=False)
    
    with open(tokenized_text, 'wb') as fp:
        pickle.dump(texts_in_w2v, fp)
        
    del texts_in_w2v
    del df
    print('Data refine Done')
    return tokenized_text
    

def refine(file, pretrained_file = './data/ko_w2v_100d_min50_2nd_sg(news_tone)', refine_data = './data/total_labeled_article.csv', 
                tokenized_text = './data/total_tokenized_corpus_okt_within_w2v.txt'):
                
    make_path(refine_data)
    make_path(tokenized_text)
    refine_text(file, refine_data)
    tokenize(refine_data, pretrained_file, tokenized_text)
   
    
    
def split(tokenized_text = 'data/total_tokenized_corpus_kkma_within_w2v.txt', pretrained_file = 'data/ko_w2v_100d_min50_2nd_sg(news_tone)',
           refine_data = './data/total_labeled_article.csv' ):
    # Make save folder
    dirname = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    '''for performance'''
    dirname = os.path.join(os.getcwd(), 'result')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    '''for trained model'''
    dirname = os.path.join(os.getcwd(), 'model')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    
    # Tokenizing sentence
    with open(tokenized_text, 'rb') as f:
        data_sentence = np.array(pickle.load(f))
    # Embedding
    embedding = Word2Vec.load((pretrained_file))
    
    # 없는 단어는 제외
    '''For Classification'''
    final_data_setence = []
    for i in tqdm(range(len(data_sentence))) :
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
    for i in tqdm(range(len(data_sentence))) :
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
    y = (pd.read_csv(refine_data)['평가'])
    
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


if  __name__ == "__main__":
    ###########################
    # Step1 : xlsx 파일 전처리 #
    ###########################
    refine('./data/total_raw_news.xlsx')
