import re
import pickle
import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from konlpy.tag import Kkma
from tqdm import tqdm  # pip install tqdm

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

def data_refine(file, pretrained_file = './data/ko_w2v_100d_min50_2nd_sg(news_tone)', refine_text = './data/total_labeled_article.csv', 
                tokenized_text = './data/total_tokenized_corpus_okt_within_w2v.txt'):
                
               
    ###########################
    # Step1 : xlsx 파일 전처리 #
    ###########################
    ###change to cython or pypy later
    
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
    df.to_csv(refine_text, index=False)

    ######################################################
    # Step2 : Text-CNN 모델의 Input에 맞도록 텍스트 전처리 #
    ######################################################
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
    # 전처리한 Trainset csv 파일로 저장하기
    df.to_csv(refine_text, index=False)
    
    with open(tokenized_text, 'wb') as fp:
        pickle.dump(texts_in_w2v, fp)
        
    del texts_in_w2v
    del df
    print('Data refine Done')


if  __name__ == "__main__":
    ###########################
    # Step1 : xlsx 파일 전처리 #
    ###########################
    data_refine('./data/total_raw_news.xlsx')
