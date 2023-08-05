import torch.nn as nn
#import config
import torch

###
'''프로젝트에 사용된 모델'''
class CNN(nn.Module) :
    def __init__(self, embedding_dim=100, num_filters=100, kernel_size=[3,4,5],stride=1):
        super(CNN, self).__init__()
        self.embedding_dim = embedding_dim

        conv_output_size1 = int((config.sentence_len - kernel_size[0]) / stride) + 1  # first conv layer output size
        conv_output_size2 = int((config.sentence_len - kernel_size[1]) / stride) + 1  # first conv layer output size
        conv_output_size3 = int((config.sentence_len - kernel_size[2]) / stride) + 1  # first conv layer output size

        # three convolution & pooling layers
        self.conv1 = nn.Conv2d(1, 100, kernel_size=(kernel_size[0], self.embedding_dim), stride=stride,padding=0)
        self.pool1 = nn.MaxPool2d((conv_output_size1, 1))  # Max-over-time pooling
        self.conv2 = nn.Conv2d(1, 100, kernel_size=(kernel_size[1], self.embedding_dim), stride=stride,padding=0)
        self.pool2 = nn.MaxPool2d((conv_output_size2, 1))  # Max-over-time pooling
        self.conv3 = nn.Conv2d(1, 100, kernel_size=(kernel_size[2], self.embedding_dim), stride=stride,padding=0)
        self.pool3 = nn.MaxPool2d((conv_output_size3, 1))  # Max-over-time pooling

        self.relu = nn.ReLU()
        self.dense = nn.Linear(num_filters * len(config.kernel_sizes),config.output_size)

    def forward(self, x):
        x = x.view(x.size(0), 1, -1, self.embedding_dim)  # resize to fit into convolutional layer
        x1_pre = self.relu(self.conv1(x))
        x2_pre = self.relu(self.conv2(x))
        x3_pre = self.relu(self.conv3(x))

        x1 = self.pool1(x1_pre)
        x2 = self.pool2(x2_pre)
        x3 = self.pool3(x3_pre)
        x_pre = torch.cat((x1_pre,x2_pre,x3_pre),dim = 2)
        x = torch.cat((x1, x2, x3), dim=1)  # concatenate three convolutional outputs
        x = x.view(x.size(0), -1)  # resize to fit into final dense layer
        x = self.dense(x)
        return x, x_pre
