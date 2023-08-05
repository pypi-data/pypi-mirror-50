from __future__ import print_function, division
import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
import config
from CNN_Model import CNN
from sklearn.externals import joblib
from tqdm import tqdm

# random seed / cuda setting
np.random.seed(0)
torch.manual_seed(0)

use_cuda = torch.cuda.is_available()
print('use_cuda = {}\n'.format(use_cuda))

###Data Loading

y_total = (pd.read_csv('./data/total_labeled_article.csv')['평가'])
y_total = y_total + 1

filename = 'data/total_data.sav'
x_total = joblib.load(filename)

filename = 'data/total_word_data.sav'
word_total = joblib.load(filename)

x_total = np.array(x_total, dtype=float)
y_total = np.array(y_total, dtype=float)

print('--------------Data Loading Done------------')

### Evaluate

# Load saved model

device = torch.device('cuda')
model = CNN(config.embedding_dim, config.num_filters, kernel_size=config.kernel_sizes, stride=1)
model.load_state_dict(torch.load('model/trained_model.pth'))
model.to(device)
model.eval()


dataset_total = TensorDataset(torch.from_numpy(x_total), torch.from_numpy(y_total))
total_loader = DataLoader(dataset_total, batch_size=config.batch_size, shuffle=False, num_workers=0, pin_memory=False)
param =list(model.parameters())[6]
param = param.cpu().detach().numpy()
final_score = []
total_featuremap = np.array([])
for i, (inputs, labels) in tqdm(enumerate(total_loader)):
    inputs = inputs.float().cuda()
    _, out_h = model(inputs)
    out_h = out_h.cpu()
    out_h = out_h.detach().numpy()

    for cam in range((out_h.shape[0])):
        f1 = out_h[cam, :, :498]
        f2 = out_h[cam, :, 498:498 + 497]
        f3 = out_h[cam, :, 498 + 497:]
        f1 = np.squeeze(f1, axis=2)
        f2 = np.squeeze(f2, axis=2)
        f3 = np.squeeze(f3, axis=2)
        f1 = np.pad(f1[:, :, ], pad_width=((0, 0), (2, 2)), mode='constant', constant_values=0)
        f2 = np.pad(f2[:, :, ], pad_width=((0, 0), (3, 3)), mode='constant', constant_values=0)
        f3 = np.pad(f3[:, :, ], pad_width=((0, 0), (4, 4)), mode='constant', constant_values=0)

        f1 = f1.transpose()
        f2 = f2.transpose()
        f3 = f3.transpose()

        mean_f1 = []
        for f1_ in range(500):
            feature = f1[3 * f1_: 3 * (f1_ + 1)]
            class_weight = param[int(labels[cam])][:100]
            mean_f1.append(np.mean(np.dot(feature, class_weight)))

        mean_f2 = []
        for f2_ in range(500):
            feature = f2[4 * f2_: 4 * (f2_ + 1)]
            class_weight = param[int(labels[cam])][100:200]
            mean_f2.append(np.mean(np.dot(feature, class_weight)))

        mean_f3 = []
        for f3_ in range(500):
            feature = f3[5 * f3_: 5 * (f3_ + 1)]
            class_weight = param[int(labels[cam])][200:300]
            mean_f3.append(np.mean(np.dot(feature, class_weight)))

        final_score.append(np.sum([mean_f1, mean_f2, mean_f3], axis=0))

# Save localization score

filename = 'result/localization_score.sav'
joblib.dump(final_score, filename=filename)


# 점수 기준 상위 30개 단어
top_visualization = []
for word_ in tqdm(range(len(x_total))):
    tmp_word = list(word_total[word_])
    tmp_value = list(final_score[word_])
    top_rank = sorted(tmp_value,reverse=True)[:30]
    top_word = [tmp_word[tmp_value.index(v)] for i, v in enumerate(top_rank)]
    top_visualization.append(top_word)

#최종 결과 저장

pd.DataFrame(top_visualization).to_csv('result/total_visualization.csv', index=False, header=False)
