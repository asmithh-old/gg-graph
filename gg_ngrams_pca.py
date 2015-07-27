import csv, ast, numpy as np, itertools, matplotlib.pyplot as plt, re, scipy
from scipy.sparse import dok_matrix
with open('gg_ngrams_data.csv') as f:
    content = f.readlines()
    f.close()
bigrams = ast.literal_eval(content[1])
huge_matrix_str = content[0]
A_dok = scipy.sparse.dok_matrix((269, 130638))
A_dok_tr = scipy.sparse.dok_matrix((130638, 269))
print len(huge_matrix_str)
start = 1
end = 1
zeros = 0
row_num = 0
find_vectors = []
#number of bigrams is 130638
#number of columns is 269
x_avg = np.zeros(130638)
while end < len(huge_matrix_str):
    if huge_matrix_str[end] == ']':
        #start:end+1
        z = ast.literal_eval(huge_matrix_str[start:end+1])
        for j in range(len(z)):
            x_avg[j] += float(z[j])
            if z[j] != 0:
                A_dok[(row_num, j)] = z[j]
                A_dok_tr[(j, row_num)] = z[j]
        find_vectors.append((start, end+1))
        start = end + 3
        end = start + 1
        row_num += 1
    elif huge_matrix_str[end] == '0':
        zeros += 1
        end += 1
    else:
        end += 1

x_avg = x_avg/float(130638)
print x_avg

#X_bar = scipy.sparse.dok_matrix([x_avg for i in range(269)])
#print X_bar.shape

#print len(find_vectors), 'cols'
#X_centered = scipy.sparse.dok_matrix(A_dok - X_bar)
cov = 1.0/float(269) * A_dok_tr * (A_dok)
print len(A_dok.keys())

# cov = scipy.sparse.dok_matrix(130638)
# for t in range(130638):
#     for u in range(130638):
#         if t >= u:
#             cov[t,u] =
#         else:
#             pass



















# print len(A[0])
# i = 0
# hist = {}
# while i < len(bigrams):
#     num_b = 0.0
#     b = bigrams[i]
#     for row in A:
#         num_b += row[i]
#     if num_b in hist:
#         hist[num_b] += 1
#     else:
#         hist[num_b] = 1
#     if num_b <20 or num_b>100:
#         del(bigrams[i])
#         for row in A:
#             del(row[i])
#
#     i += 1
#
# print len(A)
# print len(A[0])
# A = np.array(A)
# # b = np.array(ast.literal_eval(content[0]))
# # print b.shape
#
# Xbar = []
# for i in range(len(A[0])):
#     Xbar.append(float(np.sum([j[i] for j in A]))/float(len(A[0])))
# X = dok_matrix((len(A), len(A[0])))
# for i in range(len(A)):
#     for j in range(len(A[0])):
#         X[i,j] = A[i][j]-Xbar[j]
# cov = (1.0/float(len(A))) * X.transpose().dot(X)
# print np.shape(cov)
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
