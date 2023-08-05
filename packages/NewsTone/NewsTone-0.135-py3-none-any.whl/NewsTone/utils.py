import torch
import tqdm
import numpy as np
import os

# function
def softmax(z):
    return (torch.exp(z.t()) / torch.sum(torch.exp(z), dim=1)).t()

def pad_sentences(sentences, sequence_length = 500):
    padded_sentences = []
    for i in tqdm.tqdm(range(len(sentences))):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        if num_padding > 0 :
            padd = np.zeros((num_padding,100))
            new_sentence = np.vstack((sentence, padd))
        else :
            new_sentence = sentence[:500]
        padded_sentences.append(new_sentence)
    return padded_sentences


def pad_sentences2(sentences, sequence_length = 500):
    padded_sentences = []
    for i in tqdm.tqdm(range(len(sentences))):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        if num_padding > 0 :
            padd = ['0'] * num_padding
            new_sentence = list(sentence) + padd
            new_sentence = np.array(new_sentence)
        else :
            new_sentence = sentence[:500]
        padded_sentences.append(new_sentence)
    return padded_sentences

class Logger(object):
    def __init__(self, output_name):
        dirname = os.path.dirname(output_name)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        self.log_file = open(output_name, 'w')
        self.infos = {}

    def write(self, msg):
        self.log_file.write(msg + '\n')
        self.log_file.flush()
        print(msg)