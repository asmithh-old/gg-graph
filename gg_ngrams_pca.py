import csv, ast, numpy as np, itertools, matplotlib.pyplot as plt
from scipy.sparse import dok_matrix
with open('gg_ngrams_data_2.csv') as f:
    content = f.readlines()
    f.close()
bigrams = ast.literal_eval(content[1])
A = ast.literal_eval(content[0])
print len(A[0])
i = 0
hist = {}
while i < len(bigrams):
    num_b = 0.0
    b = bigrams[i]
    for row in A:
        num_b += row[i]
    if num_b in hist:
        hist[num_b] += 1
    else:
        hist[num_b] = 1
    if num_b <20 or num_b>100:
        del(bigrams[i])
        for row in A:
            del(row[i])

    i += 1

print len(A)
print len(A[0])
A = np.array(A)
# b = np.array(ast.literal_eval(content[0]))
# print b.shape

Xbar = []
for i in range(len(A[0])):
    Xbar.append(float(np.sum([j[i] for j in A]))/float(len(A[0])))
X = dok_matrix((len(A), len(A[0])))
for i in range(len(A)):
    for j in range(len(A[0])):
        X[i,j] = A[i][j]-Xbar[j]
cov = (1.0/float(len(A))) * X.transpose().dot(X)
print np.shape(cov)
# def predictive_of_bigram(bigram):
# #    given a bigram, what bigrams are more likely to appear in text containing that bigram
# #    than in text not containing that bigram? (is this actually useful???)
#     bg_index = bigrams.index(bigram)
#     bg = np.zeros(len(bigrams))
#     not_bg = np.zeros(len(bigrams))
#     bg_count = 0
#     not_bg_count = 0
#     for i in A:
#         if np.sum(i) > 0:
#             if i[bg_index] != 0:
#                 bg += np.array(i).astype(np.float32)/float(np.sum(i))
#                 bg_count += 1
#             else:
#                 not_bg += np.array(i).astype(np.float32)/float(np.sum(i))
#                 not_bg_count += 1
#     bg = bg/float(bg_count)
#     not_bg = not_bg/float(not_bg_count)
#     pred = []
#     for i in range(len(bigrams)):
#         if bg[i] > 5.0 * not_bg[i]:
#             pred.append(bigrams[i])
#     return pred
# zq = predictive_of_bigram(('Zoe', 'Quinn'))
# print
# print
# print
# bw = predictive_of_bigram(('Brianna', 'Wu'))
# anita = predictive_of_bigram(('Anita', 'Sarkeesian'))
# zq_bw = [bg for bg in zq if bg in bw and bg in anita]
# print zq_bw
# print
# print
# print
# aah = predictive_of_bigram(('gaming', 'journalism'))
# print aah


# mu = [float(np.sum(i))/float(len(b)) for i in np.transpose(b)]
# cov = np.zeros([len(np.transpose(b)),len(np.transpose(b))])
# for b_k in b:
#     cov += np.outer(b_k-mu, b_k-mu)
# print cov.shape
# eig_val_sc, eig_vec_sc = np.linalg.eig(cov)
# print eig_val_sc[0:5]
# for x in eig_vec_sc[0:4]:
#     where = 0
#     for i in x:
#         if i != 0:
#             print bigrams[where],
#         where += 1
#     print
#     print
#     print
#     print
#     print
