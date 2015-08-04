import csv, ast, numpy as np, itertools,  re, scipy
from scipy.sparse import dok_matrix
with open('gg_ngrams_data_mutually_linked.csv') as f:
    content = f.readlines()
    f.close()

##TODO: figure out how to find eigenvectors of very large matrix.
##TODO: make new set of articles that is top set of articles.
##output bigrams, stories as vectors, and matching story ids to vectors.
##(when do clustering, want to cluster articles, not just language, so need to know which article is which.)

#number of bigrams (dimensionality of dataset) is num_bigrams
#number of columns (number of data points) is num_stories

bigrams = ast.literal_eval(content[1])
huge_matrix_str = content[0]
num_stories = 250
num_bigrams = len(bigrams)
A_dok = scipy.sparse.dok_matrix((num_stories, num_bigrams))
A_dok_tr = scipy.sparse.dok_matrix((num_bigrams, num_stories))
print len(huge_matrix_str)
start = 1
end = 1
zeros = 0
row_num = 0
find_vectors = []

x_avg = np.zeros(num_bigrams)
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

x_avg = x_avg/float(num_bigrams)
print x_avg

#X_bar = scipy.sparse.dok_matrix([x_avg for i in range(num_stories)])
#print X_bar.shape

#print len(find_vectors), 'cols'
#X_centered = scipy.sparse.dok_matrix(A_dok - X_bar)
#cov = 1.0/float(num_stories) * A_dok_tr * (A_dok)
#print len(A_dok.keys())
print 'making cov'
cov = scipy.sparse.dok_matrix((num_bigrams,num_bigrams))
for t in range(num_bigrams):
    print float(t)/float(num_bigrams)
    for u in range(num_bigrams):
        if t >= u:
            cov_entry = float((A_dok_tr.getrow(t).todense()-x_avg[t]*np.ones(num_stories)).dot(np.transpose(A_dok_tr.getrow(u).todense()-x_avg[u]*np.ones(num_stories)))[0,0])
            if cov_entry < 1.0:
                pass
            else:
                cov[t,u] = 1.0/float(num_stories) * cov_entry
                cov[u,t] = 1.0/float(num_stories) * cov_entry
        else:
            pass

with open('gg-ngrams-cov.csv', 'w') as f:
    f.write(str(cov))
    f.close()

















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
